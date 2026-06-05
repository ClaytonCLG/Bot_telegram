"""
Bot Telegram - Versão Railway
Monitora o grupo GRUPO_BONAPARTE, detecta tarefas e envia o 3º print para Dionara.
"""
import os
import re
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from flask import Flask, jsonify, request, send_file
import threading

# ─── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ─── Variáveis de Ambiente ───────────────────────────────────────────────────
logger.info("=" * 80)
logger.info("🤖 INICIANDO BOT TELEGRAM")
logger.info("=" * 80)

# Carregar variáveis com validação
TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID', '').strip()
TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH', '').strip()
SESSION_STRING = os.environ.get('SESSION_STRING', '').strip()
TARGET_GROUP_ID = os.environ.get('TARGET_GROUP_ID', '').strip()
RECIPIENT_CHAT_ID = os.environ.get('RECIPIENT_CHAT_ID', '').strip()
PORT = os.environ.get('PORT', '8080').strip()

# Log das variáveis
logger.info(f"📋 TELEGRAM_API_ID: {'✓' if TELEGRAM_API_ID else '✗ FALTANDO'}")
logger.info(f"📋 TELEGRAM_API_HASH: {'✓' if TELEGRAM_API_HASH else '✗ FALTANDO'}")
logger.info(f"📋 SESSION_STRING: {'✓' if SESSION_STRING else '✗ FALTANDO'} (len={len(SESSION_STRING)})")
logger.info(f"📋 TARGET_GROUP_ID: {TARGET_GROUP_ID if TARGET_GROUP_ID else '✗ FALTANDO'}")
logger.info(f"📋 RECIPIENT_CHAT_ID: {RECIPIENT_CHAT_ID if RECIPIENT_CHAT_ID else '✗ FALTANDO'}")
logger.info(f"📋 PORT: {PORT}")

# Validar variáveis obrigatórias
if not all([TELEGRAM_API_ID, TELEGRAM_API_HASH, SESSION_STRING, TARGET_GROUP_ID, RECIPIENT_CHAT_ID]):
    logger.error("❌ ERRO: Faltam variáveis de ambiente obrigatórias!")
    logger.error("Verifique se todas as variáveis estão configuradas no Railway!")

# Converter para tipos corretos
try:
    TELEGRAM_API_ID = int(TELEGRAM_API_ID) if TELEGRAM_API_ID else 0
    TARGET_GROUP_ID = int(TARGET_GROUP_ID) if TARGET_GROUP_ID else 0
    RECIPIENT_CHAT_ID = int(RECIPIENT_CHAT_ID) if RECIPIENT_CHAT_ID else 0
    PORT = int(PORT) if PORT else 8080
except ValueError as e:
    logger.error(f"❌ Erro ao converter variáveis: {e}")
    TELEGRAM_API_ID = 0
    TARGET_GROUP_ID = 0
    RECIPIENT_CHAT_ID = 0
    PORT = 8080

logger.info(f"✓ Iniciando bot — porta {PORT}")
logger.info("=" * 80)

# ─── Cliente Telegram ────────────────────────────────────────────────────────
client = None
try:
    logger.info("🔌 Inicializando TelegramClient...")
    client = TelegramClient(StringSession(SESSION_STRING), TELEGRAM_API_ID, TELEGRAM_API_HASH)
    logger.info('✓ TelegramClient inicializado com sucesso!')
except Exception as e:
    logger.error(f'❌ Erro ao inicializar TelegramClient: {e}')
    logger.error('Verifique se as variáveis de ambiente estão corretas!')
    logger.error(f'Traceback: {type(e).__name__}')
    client = None

# ─── Estado ──────────────────────────────────────────────────────────────────
bot_status = {
    "active": True,
    "connected": False,
    "last_task": None,
    "tasks_processed": 0,
}
tasks_history = []
task_tracking = {}

# ─── Flask ───────────────────────────────────────────────────────────────────
app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/api/bot/status')
def get_status():
    return jsonify(bot_status)

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    bot_status["active"] = True
    return jsonify({"message": "Bot iniciado", "status": bot_status})

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    bot_status["active"] = False
    return jsonify({"message": "Bot parado", "status": bot_status})

@app.route('/api/tasks')
def get_tasks():
    return jsonify({"tasks": tasks_history})

@app.route('/api/image')
def get_image():
    image_path = request.args.get('path', '')
    if not image_path or '..' in image_path or not os.path.exists(image_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    return send_file(image_path, mimetype='image/jpeg')

# ─── Event Handler ───────────────────────────────────────────────────────────
async def my_event_handler(event):
    if not bot_status["active"]:
        return

    message_text = event.message.text or ""
    has_photo = event.message.photo is not None

    # Detectar mensagem de TAREFA
    match = re.search(r'(?i)TAREFA\s*([0-9]{1,3})', message_text)

    if match:
        task_num = match.group(1)
        logger.info(f"✅ TAREFA DETECTADA: {task_num}")
        task_tracking[task_num] = {
            "detected_at": datetime.now(),
            "prints_count": 0,
            "third_print": None,
            "third_print_caption": None,
        }
        logger.info(f"🎯 Aguardando prints para tarefa {task_num}...")
        return

    # Processar print (foto enviada por alguém após a tarefa)
    if has_photo and task_tracking:
        logger.info(f"📸 Print recebido (legenda: '{message_text[:30]}')")

        for task_num in sorted(task_tracking.keys(), key=lambda x: int(x), reverse=True):
            task_info = task_tracking[task_num]

            if task_info["third_print"] is None:
                task_info["prints_count"] += 1
                logger.info(f"📊 Tarefa {task_num}: Print #{task_info['prints_count']}")

                if task_info["prints_count"] == 3:
                    logger.info(f"🎉 3º PRINT DA TAREFA {task_num} — ENVIANDO PARA DIONARA!")
                    try:
                        photo_path = await client.download_media(event.message.photo)
                        caption = message_text.strip() if message_text.strip() else f"Tarefa {task_num}"

                        task_info["third_print"] = photo_path
                        task_info["third_print_caption"] = caption

                        # Envia como nova mensagem
                        await client.send_file(RECIPIENT_CHAT_ID, photo_path, caption=caption)
                        logger.info(f"✅ Enviado para Dionara — Tarefa {task_num} | Legenda: {caption}")

                        entry = {
                            "id": task_num,
                            "status": "Enviado",
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "caption": caption,
                            "image_path": photo_path,
                        }
                        tasks_history.append(entry)
                        bot_status["last_task"] = entry
                        bot_status["tasks_processed"] += 1

                    except Exception as e:
                        import traceback
                        logger.error(f"❌ Erro ao enviar print da tarefa {task_num}: {e}")
                        logger.error(traceback.format_exc())

                break

# ─── Conexão com Reconexão Automática ────────────────────────────────────────
async def connect_and_run():
    if client is None:
        logger.error('❌ TelegramClient não foi inicializado!')
        return

    while True:
        try:
            logger.info("🔌 Conectando ao Telegram...")
            await client.connect()

            if not await client.is_user_authorized():
                logger.error("❌ Sessão inválida! Verifique SESSION_STRING.")
                break

            bot_status["connected"] = True
            logger.info("✅ Conectado ao Telegram!")

            # Registrar handler
            client.remove_event_handler(my_event_handler)
            client.add_event_handler(my_event_handler, events.NewMessage(chats=[TARGET_GROUP_ID]))
            logger.info("✅ Event handler registrado! 🟢 Aguardando mensagens...")

            # Keep-alive
            while True:
                await asyncio.sleep(30)
                if not client.is_connected():
                    logger.warning("⚠️ Conexão perdida! Reconectando em 5s...")
                    bot_status["connected"] = False
                    break
                try:
                    await client.get_me()
                except Exception as e:
                    logger.warning(f"⚠️ Keep-alive falhou: {e}. Reconectando...")
                    bot_status["connected"] = False
                    break

        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            bot_status["connected"] = False

        logger.info("⏳ Aguardando 5s para reconectar...")
        await asyncio.sleep(5)
        try:
            await client.disconnect()
        except:
            pass

# ─── Main ─────────────────────────────────────────────────────────────────────
def run_telegram():
    if client is None:
        logger.error('❌ Bot não pode iniciar: TelegramClient não foi inicializado!')
        logger.error('Verifique as variáveis de ambiente!')
        return
    asyncio.run(connect_and_run())

if __name__ == '__main__':
    # Inicia Telegram em thread separada
    t = threading.Thread(target=run_telegram, daemon=True)
    t.start()

    import time
    time.sleep(4)

    # Inicia Flask
    logger.info(f"🚀 Iniciando Flask na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False)
