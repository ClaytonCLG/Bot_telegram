import os
import re
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from flask import Flask, jsonify, request
from PIL import Image, ImageDraw, ImageFont
import json

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente IMEDIATAMENTE após criar o logger
from dotenv import load_dotenv
load_dotenv(override=True)  # override=True para sobrescrever variáveis globais

TELEGRAM_API_ID = int(os.getenv('TELEGRAM_API_ID'))
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE')
TARGET_GROUP_ID = int(os.getenv('TARGET_GROUP_ID'))
RECIPIENT_CHAT_ID = int(os.getenv('RECIPIENT_CHAT_ID'))
PORT = int(os.getenv('PORT', 5001))

logger.info(f"Configuração carregada - PORT: {PORT}")

# Cliente Telegram
client = TelegramClient('session', TELEGRAM_API_ID, TELEGRAM_API_HASH)

# Status do bot
bot_status = {
    "active": False,
    "last_task": None,
    "tasks_processed": 0,
    "connected": False
}

# Histórico de tarefas
tasks_history = []

# Rastreamento de tarefas e prints
# Estrutura: {task_num: {"detected_at": timestamp, "prints_count": 0, "third_print": None}}
task_tracking = {}

# Flask app
app = Flask(__name__)

# Event handler para novas mensagens (será registrado dinamicamente)
async def my_event_handler(event):
    if not bot_status["active"]:
        return

    # Capturar o texto da mensagem
    message_text = event.message.text or ""
    has_photo = event.message.photo is not None
    
    # Verificar se é mensagem de TAREFA (tem o padrão TAREFA XX no texto)
    match = re.search(r'(?i)TAREFA\s*([0-9]{1,3})', message_text)
    
    if match:
        # ===== NOVA TAREFA DETECTADA =====
        task_num = match.group(1)
        logger.info(f"✅ TAREFA DETECTADA: {task_num}")
        
        # Inicializar rastreamento — ignora qualquer foto que veio JUNTO com a mensagem da tarefa
        task_tracking[task_num] = {
            "detected_at": datetime.now(),
            "prints_count": 0,
            "third_print": None,
            "third_print_caption": None,
            "task_message_id": event.message.id  # ID da mensagem da tarefa para ignorar
        }
        logger.info(f"🎯 Aguardando prints para tarefa {task_num}...")
        return  # Sai aqui — não processa foto da mensagem de tarefa
    
    # Verificar se é um print (foto enviada por alguém no grupo)
    if has_photo:
        # Ignorar se não há tarefas pendentes
        if not task_tracking:
            return
        
        logger.info(f"📸 Print recebido (legenda: '{message_text[:30]}')")
        
        # Procurar pela tarefa mais recente pendente
        for task_num in sorted(task_tracking.keys(), key=lambda x: int(x), reverse=True):
            task_info = task_tracking[task_num]
            
            # Só processar se ainda não enviou o 3º print
            if task_info["third_print"] is None:
                task_info["prints_count"] += 1
                logger.info(f"📊 Tarefa {task_num}: Print #{task_info['prints_count']}")
                
                # Se for o 3º print, capturar e enviar!
                if task_info["prints_count"] == 3:
                    logger.info(f"🎉 3º PRINT DA TAREFA {task_num} — ENVIANDO PARA DIONARA!")
                    try:
                        # Baixar a foto
                        photo_path = await client.download_media(event.message.photo)
                        logger.info(f"✅ Foto baixada: {photo_path}")
                        
                        # Usar a legenda original da pessoa
                        caption = message_text.strip() if message_text.strip() else f"Tarefa {task_num}"
                        
                        # Marcar como processado
                        task_info["third_print"] = photo_path
                        task_info["third_print_caption"] = caption
                        
                        # Enviar para Dionara (download + reenvio, NÃO forward)
                        await client.send_file(RECIPIENT_CHAT_ID, photo_path, caption=caption)
                        logger.info(f"✅ Enviado para Dionara — Tarefa {task_num} | Legenda: {caption}")
                        
                        # Salvar no histórico
                        task_info_dict = {
                            "id": task_num,
                            "status": "Enviado",
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "caption": caption,
                            "image_path": photo_path
                        }
                        tasks_history.append(task_info_dict)
                        bot_status["last_task"] = task_info_dict
                        bot_status["tasks_processed"] += 1
                        
                    except Exception as e:
                        logger.error(f"❌ Erro ao enviar print da tarefa {task_num}: {e}")
                        import traceback
                        logger.error(traceback.format_exc())
                
                break  # Só processa a tarefa mais recente

# Rotas da API
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    bot_status["active"] = True
    logger.info("Bot iniciado")
    return jsonify({"message": "Bot iniciado", "status": bot_status})

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    bot_status["active"] = False
    logger.info("Bot parado")
    return jsonify({"message": "Bot parado", "status": bot_status})

@app.route('/api/bot/status', methods=['GET'])
def get_status():
    return jsonify(bot_status)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks_history})

@app.route('/api/image', methods=['GET'])
def get_image():
    import os
    from flask import send_file
    
    image_path = request.args.get('path')
    if not image_path:
        return jsonify({"error": "Caminho da imagem não fornecido"}), 400
    
    # Validar caminho para evitar path traversal
    if '..' in image_path or not os.path.exists(image_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    
    try:
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        logger.error(f"Erro ao servir imagem: {e}")
        return jsonify({"error": "Erro ao servir imagem"}), 500

async def connect_and_run():
    """Conecta ao Telegram e mantém a conexão ativa com reconexão rápida."""
    while True:
        try:
            logger.info("🔌 Conectando ao Telegram...")
            await client.start(phone=TELEGRAM_PHONE)
            bot_status["connected"] = True
            logger.info(f"✅ Cliente Telegram conectado como {TELEGRAM_PHONE}")
            
            # Registrar event handler
            client.remove_event_handler(my_event_handler)
            client.add_event_handler(my_event_handler, events.NewMessage(chats=[TARGET_GROUP_ID]))
            logger.info("✅ Event handler registrado!")
            logger.info("🟢 Aguardando mensagens...")
            
            # Loop de keep-alive: verifica conexão a cada 30 segundos
            while True:
                await asyncio.sleep(30)
                if not client.is_connected():
                    logger.warning("⚠️ Conexão perdida! Reconectando...")
                    bot_status["connected"] = False
                    break
                # Ping para manter conexão viva
                try:
                    await client.get_me()
                except Exception as e:
                    logger.warning(f"⚠️ Erro no keep-alive: {e}. Reconectando...")
                    bot_status["connected"] = False
                    break
                    
        except SessionPasswordNeededError:
            logger.error("❌ Senha de 2FA necessária! Parando.")
            break
        except Exception as e:
            logger.error(f"❌ Erro na conexão: {e}")
            bot_status["connected"] = False
        
        # Aguardar 5 segundos antes de reconectar
        logger.info("⏳ Aguardando 5s para reconectar...")
        await asyncio.sleep(5)
        
        # Desconectar antes de reconectar
        try:
            await client.disconnect()
        except:
            pass

async def main():
    await connect_and_run()

if __name__ == '__main__':
    # Iniciar cliente Telegram em thread separada
    import threading
    
    def run_telegram():
        asyncio.run(main())
    
    telegram_thread = threading.Thread(target=run_telegram, daemon=True)
    telegram_thread.start()
    
    # Aguardar conexão
    import time
    time.sleep(3)
    
    # Iniciar Flask
    app.run(host='0.0.0.0', port=PORT, debug=False)
