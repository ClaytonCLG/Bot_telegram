#!/bin/bash
set -e

echo "🚀 Iniciando Bot Telegram no Railway..."
echo "TELEGRAM_API_ID: $TELEGRAM_API_ID"
echo "TARGET_GROUP_ID: $TARGET_GROUP_ID"
echo "RECIPIENT_CHAT_ID: $RECIPIENT_CHAT_ID"
echo "PORT: $PORT"

# Instalar dependências
pip install -r requirements.txt

# Iniciar o bot
python bot.py
