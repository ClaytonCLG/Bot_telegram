# Bot Telegram - Deployment no Railway

Bot Telegram otimizado para rodar 24/7 no Railway.app com todas as variáveis já configuradas!

## 📦 Arquivos Inclusos

- `bot.py` - Bot principal (Telethon + Flask)
- `requirements.txt` - Dependências Python
- `Procfile` - Configuração para Railway
- `runtime.txt` - Versão Python
- `.env` - **Variáveis já configuradas!**
- `.gitignore` - Arquivo para ignorar no Git

## 🚀 Como Fazer Deploy

### Passo 1: Upload para GitHub

1. Acesse seu repositório: https://github.com/ClaytonCLG/Bot_telegram
2. Clique em **Add file** → **Upload files**
3. Arraste TODOS esses arquivos para o GitHub
4. Commit com mensagem: `"Deploy bot para Railway com variáveis configuradas"`

### Passo 2: Conectar ao Railway

1. Acesse https://railway.app
2. Clique em **New Project** → **Deploy from GitHub repo**
3. Selecione `ClaytonCLG/Bot_telegram`
4. Railway detectará o `Procfile` automaticamente

### Passo 3: Configurar Variáveis no Railway

⚠️ **IMPORTANTE:** As variáveis já estão no arquivo `.env`, mas o Railway NÃO lê `.env` automaticamente!

Você precisa adicionar manualmente no painel do Railway:

1. Vá para **Variables**
2. Clique em **New Variable** e adicione:

```
TELEGRAM_API_ID=36263007
TELEGRAM_API_HASH=9c9769a227e52ef9a197c43cd67f167f
SESSION_STRING=1AZWarzMBu15noJ--xOAuqqCcOSfYepW3U3nagr8HDIMGMk9fn0GypmP-YNyVgO88BZZZUQG0FQsIpxKeySkp9BQtLXaK0rqd5xj8QevvTPeO8JVAELxMPyULhYV0pBfVW6wzbSH58Gk8u7ZFYlAz-kY5q8sH4nXjfdBT68eL8U9wrVhIbpHu1Kb7h42cju1O9xVkaA8d6VKha3KnOknuYZ7UV_aRJGOeMz5sIMosuECBMBSp74YWDDeeQa4Ri1W73LPJPbT6etQLI-DsJ3H3Z5SrWryjhPyNTLzRGGBnuSmSH8jY5PXqR58jIs14j_26q697LtWOvBG_vo6mWCJnTbMTo3xxMsM=
TARGET_GROUP_ID=-1003957567812
RECIPIENT_CHAT_ID=7772844148
PORT=8080
```

3. Clique em **Deploy** ou **Redeploy**

### Passo 4: Verificar Deploy

Aguarde 2-3 minutos e verifique os logs. Deve aparecer:
```
✅ Conectado ao Telegram!
✅ Event handler registrado! 🟢 Aguardando mensagens...
```

## ✅ Testar

```bash
curl https://seu-app-railway.up.railway.app/api/health
```

Deve retornar:
```json
{"status": "ok", "timestamp": "..."}
```

## 🎉 Pronto!

Seu bot está rodando 24/7 no Railway! 🚀

---

**Desenvolvido com ❤️ para automação do Telegram**
