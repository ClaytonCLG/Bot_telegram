# 📖 Guia Completo de Deployment no Railway

## 🎯 Objetivo

Fazer o bot Telegram rodar **24/7** no Railway.app sem precisar de um computador ligado.

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ Conta no Railway.app (gratuita)
- ✅ SESSION_STRING do bot (já exportada)
- ✅ TELEGRAM_API_ID e TELEGRAM_API_HASH
- ✅ ID do grupo GRUPO_BONAPARTE
- ✅ ID da Dionara (para enviar os prints)

---

## 🚀 Passo a Passo

### PASSO 1: Fazer Upload para GitHub

1. Abra seu repositório: https://github.com/ClaytonCLG/Bot_telegram

2. Clique em **Add file** (botão verde no topo direito)

3. Selecione **Upload files**

4. Arraste estes arquivos para a área de upload:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `README.md`
   - `.env.example`
   - `.gitignore`

5. Escreva a mensagem de commit: `Deploy bot para Railway`

6. Clique em **Commit changes**

✅ **Pronto! Arquivos estão no GitHub**

---

### PASSO 2: Criar Conta no Railway (se não tiver)

1. Acesse https://railway.app
2. Clique em **Sign Up** (ou faça login se já tiver conta)
3. Conecte com sua conta do GitHub

✅ **Conta criada!**

---

### PASSO 3: Conectar GitHub ao Railway

1. No painel do Railway, clique em **New Project**

2. Selecione **Deploy from GitHub repo**

3. Autorize o Railway a acessar seu GitHub

4. Procure por `Bot_telegram` e clique para selecionar

5. Railway detectará automaticamente o `Procfile` e criará o projeto

✅ **Projeto criado no Railway!**

---

### PASSO 4: Configurar Variáveis de Ambiente

1. No painel do Railway, vá para a aba **Variables**

2. Clique em **New Variable** e adicione cada uma:

| Variável | Valor | Exemplo |
|----------|-------|---------|
| `TELEGRAM_API_ID` | Seu API ID | `12345678` |
| `TELEGRAM_API_HASH` | Seu API Hash | `abc123def456...` |
| `SESSION_STRING` | Sua StringSession | `1BVtsOIQBu...` |
| `TARGET_GROUP_ID` | ID do grupo Bonaparte | `-100123456789` |
| `RECIPIENT_CHAT_ID` | ID da Dionara | `987654321` |
| `PORT` | `8080` | `8080` |

**Como obter cada variável:**

#### TELEGRAM_API_ID e TELEGRAM_API_HASH
1. Acesse https://my.telegram.org/apps
2. Faça login com sua conta Telegram
3. Copie o **API ID** e **API Hash**

#### SESSION_STRING
- Você já tem! Foi exportada quando criamos o bot localmente.
- Procure no arquivo `session.txt` ou no terminal anterior.

#### TARGET_GROUP_ID
1. Abra o grupo GRUPO_BONAPARTE no Telegram
2. Clique no nome do grupo (topo)
3. Copie a URL: `https://t.me/c/123456789/...`
4. O ID é: `-100123456789` (adicione `-100` antes do número)

#### RECIPIENT_CHAT_ID
1. Abra o chat com Dionara
2. Clique no nome (topo)
3. Se for um usuário, copie o ID normalmente
4. Se for um grupo, adicione `-100` antes

✅ **Variáveis configuradas!**

---

### PASSO 5: Fazer o Deploy

1. Clique em **Deploy** no painel do Railway

2. Aguarde 2-3 minutos enquanto o Railway:
   - Clona o repositório
   - Instala dependências (`pip install -r requirements.txt`)
   - Inicia o bot

3. Verifique os **Logs** para confirmar:
   ```
   ✅ Conectado ao Telegram!
   ✅ Event handler registrado! 🟢 Aguardando mensagens...
   ```

✅ **Bot está rodando 24/7!**

---

## ✅ Verificar se Está Funcionando

### Teste 1: Health Check
```bash
curl https://seu-app-railway.up.railway.app/api/health
```
Deve retornar:
```json
{"status": "ok", "timestamp": "2026-06-04T21:00:00"}
```

### Teste 2: Status do Bot
```bash
curl https://seu-app-railway.up.railway.app/api/bot/status
```
Deve retornar:
```json
{
  "active": true,
  "connected": true,
  "last_task": null,
  "tasks_processed": 0
}
```

### Teste 3: Enviar Tarefa no Telegram
1. Vá para o grupo GRUPO_BONAPARTE
2. Envie uma mensagem: `TAREFA 01`
3. Envie 3 prints (imagens)
4. Verifique se o 3º print foi enviado para Dionara

✅ **Tudo funcionando!**

---

## 🔧 Troubleshooting

### ❌ "Bot não conecta ao Telegram"

**Solução:**
- Verifique se SESSION_STRING está correta
- Confirme TELEGRAM_API_ID e TELEGRAM_API_HASH
- Verifique os logs no Railway: `Logs` → procure por erros

### ❌ "Bot conecta mas não recebe mensagens"

**Solução:**
- Confirme que TARGET_GROUP_ID está correto (deve começar com `-100`)
- Verifique se o bot está no grupo GRUPO_BONAPARTE
- Confirme que a mensagem começa com `TAREFA` (case-insensitive)

### ❌ "Erro 'Arquivo não encontrado' ao baixar imagem"

**Solução:**
- Verifique o caminho da imagem em `/api/image?path=...`
- As imagens são salvas em `/tmp/` no Railway (podem ser limpas)

### ❌ "Railway desligou o app"

**Solução:**
- Railway oferece 500 horas/mês grátis (suficiente para 24/7)
- Se atingir o limite, upgrade para plano pago ou crie outra conta

---

## 📱 Conectar Mobile App

1. Abra o app mobile (Expo)
2. Vá para **Settings** → **Server URL**
3. Digite: `https://seu-app-railway.up.railway.app`
4. Salve e volte para **Tasks**
5. Você verá o histórico de tarefas capturadas

---

## 🎉 Pronto!

Seu bot agora está rodando 24/7 no Railway! 🚀

**Próximos passos:**
- Monitore os logs regularmente
- Atualize a URL do app mobile
- Teste com tarefas reais no grupo

---

## 📞 Suporte

Se algo não funcionar:
1. Verifique os **Logs** no painel do Railway
2. Confirme todas as variáveis de ambiente
3. Tente fazer um novo deploy clicando em **Redeploy**

**Boa sorte! 🎊**
