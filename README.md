# Bot Telegram - Deployment no Railway

Este é o bot Telegram otimizado para rodar 24/7 no Railway.app.

## 📋 Arquivos Inclusos

- **bot.py** - Bot principal com Telethon + Flask API
- **requirements.txt** - Dependências Python
- **Procfile** - Configuração para Railway
- **runtime.txt** - Versão do Python
- **userbot_server.py** - Servidor alternativo (opcional)

## 🚀 Como Fazer Deploy

### 1️⃣ Fazer Upload para GitHub

1. Acesse seu repositório: https://github.com/ClaytonCLG/Bot_telegram
2. Clique em **Add file** → **Upload files**
3. Arraste todos esses arquivos para o GitHub
4. Commit com mensagem: `"Deploy bot para Railway"`

### 2️⃣ Conectar ao Railway

1. Acesse https://railway.app
2. Clique em **New Project** → **Deploy from GitHub**
3. Selecione o repositório `ClaytonCLG/Bot_telegram`
4. Railway detectará automaticamente o `Procfile`

### 3️⃣ Configurar Variáveis de Ambiente

No painel do Railway, vá para **Variables** e adicione:

```
TELEGRAM_API_ID=seu_api_id
TELEGRAM_API_HASH=seu_api_hash
SESSION_STRING=sua_session_string
TARGET_GROUP_ID=id_do_grupo_bonaparte
RECIPIENT_CHAT_ID=id_da_dionara
PORT=8080
```

**Como obter cada uma:**

- **TELEGRAM_API_ID** e **TELEGRAM_API_HASH**: https://my.telegram.org/apps
- **SESSION_STRING**: Já foi exportada (você tem)
- **TARGET_GROUP_ID**: ID do grupo GRUPO_BONAPARTE
- **RECIPIENT_CHAT_ID**: ID da Dionara (geralmente negativo para grupos)
- **PORT**: Deixe como 8080 (Railway atribui automaticamente)

### 4️⃣ Fazer Deploy

1. Clique em **Deploy** no painel do Railway
2. Aguarde 2-3 minutos
3. Verifique os logs para confirmar conexão

## 📡 Endpoints da API

Após deploy, você pode acessar:

- **Health Check**: `GET /api/health`
- **Status do Bot**: `GET /api/bot/status`
- **Iniciar Bot**: `POST /api/bot/start`
- **Parar Bot**: `POST /api/bot/stop`
- **Histórico de Tarefas**: `GET /api/tasks`
- **Baixar Imagem**: `GET /api/image?path=/caminho/da/imagem`

## ✅ Verificar se está Funcionando

```bash
curl https://seu-app-railway.up.railway.app/api/health
```

Deve retornar: `{"status": "ok", "timestamp": "..."}`

## 🔧 Troubleshooting

**Bot não conecta?**
- Verifique SESSION_STRING (não pode estar expirada)
- Confirme TELEGRAM_API_ID e TELEGRAM_API_HASH

**Não recebe mensagens?**
- Verifique TARGET_GROUP_ID (deve ser negativo: -100123456789)
- Confirme que o bot está no grupo

**Erro de permissão?**
- SESSION_STRING pode estar expirada
- Gere uma nova sessão localmente e atualize

## 📱 Mobile App

A aplicação mobile (Expo/React Native) já está configurada para se conectar a este bot.
Atualize a URL do servidor nas configurações do app para: `https://seu-app-railway.up.railway.app`

---

**Pronto! 🎉 O bot agora rodará 24/7 no Railway!**
