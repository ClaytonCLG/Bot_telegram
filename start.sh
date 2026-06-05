#!/bin/bash

# Carregar variáveis do .env se existir (Railway pode não passar automaticamente)
if [ -f .env ]; then
    echo "📋 Carregando variáveis do .env..."
    set -a
    source .env
    set +a
fi

echo "🚀 Iniciando Bot Telegram no Railway..."
echo "TELEGRAM_API_ID: ${TELEGRAM_API_ID:-VAZIO}"
echo "TELEGRAM_API_HASH: ${TELEGRAM_API_HASH:0:10}..."
echo "SESSION_STRING: ${SESSION_STRING:0:50}... (${#SESSION_STRING} chars)"
echo "TARGET_GROUP_ID: ${TARGET_GROUP_ID:-VAZIO}"
echo "RECIPIENT_CHAT_ID: ${RECIPIENT_CHAT_ID:-VAZIO}"
echo "PORT: ${PORT:-8080}"

# Instalar dependências
pip install -r requirements.txt

# Iniciar o bot
python3 bot.py
