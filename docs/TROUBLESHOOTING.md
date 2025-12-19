# 🔧 Guia de Solução de Problemas

## ✅ Status Atual
- **Sintaxe:** ✅ Todos os arquivos OK
- **Estrutura:** ✅ Projeto organizado
- **Configuração:** ✅ config.py pronto

---

## 🚨 Problemas Comuns e Soluções

### 1️⃣ Erro: "Não foi possível resolver a importação discord"

**Causa:** Discord.py não está instalado no ambiente local (VSCode)

**Solução:**
```bash
pip install discord.py flask
# ou
pip install -r requirements.txt
```

**Nota:** No Replit, isso é instalado automaticamente. Este erro no VSCode é apenas visual.

---

### 2️⃣ Erro: "discord.LoginFailure" ou "Improper token"

**Causa:** Token do Discord inválido ou não configurado

**Solução:**
1. Vá para [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecione seu bot
3. Vá em "Bot" → "Reset Token"
4. Configure a variável de ambiente:
   ```bash
   export DISCORD_TOKEN="seu_token_aqui"
   ```
   Ou no Replit: Secrets → `DISCORD_TOKEN`

---

### 3️⃣ Erro: "403 Forbidden" ao tentar executar comando

**Causa:** Bot não tem permissões necessárias

**Solução:**
1. Vá no Discord Developer Portal
2. OAuth2 → URL Generator
3. Selecione:
   - **Scopes:** `bot`, `applications.commands`
   - **Bot Permissions:**
     - Administrator (recomendado para desenvolvimento)
     - Ou permissões específicas:
       - Manage Roles
       - Manage Channels
       - Kick Members
       - Ban Members
       - Manage Messages
       - Read Message History
       - Add Reactions
       - View Audit Log
4. Use o link gerado para re-convidar o bot

---

### 4️⃣ Erro: "Canal de logs não encontrado"

**Causa:** IDs no config.py não correspondem ao seu servidor

**Solução:**
1. Ative o Modo Desenvolvedor no Discord:
   - Configurações → Avançado → Modo Desenvolvedor
2. Clique com botão direito nos canais → "Copiar ID"
3. Edite `config.py`:
   ```python
   CANAIS = {
       "boas_vindas": SEU_ID_AQUI,
       "saidas": SEU_ID_AQUI,
       "logs": SEU_ID_AQUI
   }
   ```

---

### 5️⃣ Erro: "Cargo 'Mutado' não encontrado"

**Causa:** Cargo ainda não foi criado

**Solução:**
Execute no Discord:
```
!setupmute
```
Isso criará o cargo e configurará as permissões automaticamente.

---

### 6️⃣ Warns não estão sendo salvos

**Causa:** Problemas de permissão no arquivo warns.json

**Solução:**
```bash
chmod 666 warns.json
# ou remova e deixe o bot recriar
rm warns.json
```

---

### 7️⃣ Bot não responde a comandos

**Possíveis causas e soluções:**

**A) Prefixo incorreto**
- Use `!` antes dos comandos
- Exemplo: `!ajuda`

**B) Bot offline**
- Verifique se o bot está online no Discord
- Execute: `python3 main.py`

**C) Comandos não sincronizados**
- O bot sincroniza automaticamente ao iniciar
- Aguarde alguns segundos após o bot ficar online

**D) Intents não habilitados**
- Vá no Discord Developer Portal
- Bot → Privileged Gateway Intents
- Ative todas as opções:
  - Presence Intent
  - Server Members Intent
  - Message Content Intent

---

### 8️⃣ Erro: "ModuleNotFoundError: No module named 'Python'"

**Causa:** Executando de diretório incorreto

**Solução:**
```bash
cd /caminho/para/Xiru-aftonzera
python3 main.py
```

---

### 9️⃣ Sistema de cadastro não funciona

**Causa:** ID da mensagem incorreto ou mensagem não existe

**Solução:**
1. Crie uma nova mensagem de cadastro:
   ```
   !criar_mensagem_cadastro
   ```
2. Copie o ID da mensagem
3. Atualize em `config.py`:
   ```python
   MENSAGEM_CADASTRO_ID = ID_DA_MENSAGEM
   ```
4. Adicione as reações:
   ```
   !add_reacoes
   ```

---

### 🔟 Erro: "Address already in use" (Keep-alive)

**Causa:** Porta 8080 já está em uso

**Solução:**
1. Edite `config.py`:
   ```python
   KEEP_ALIVE_PORT = 8081  # ou outra porta disponível
   ```
2. Ou mate o processo na porta:
   ```bash
   lsof -ti:8080 | xargs kill -9
   ```

---

## 🧪 Testando o Bot Localmente

### Verificação Rápida:
```bash
python3 scripts/verificar.py
# ou
scripts/dev.sh status
```

### Execução:
```bash
python3 main.py
```

### Logs Esperados:
```
==================================================
🔁 BOT INICIALIZADO
==================================================

📂 Carregando módulos (cogs)...
  ✔️ boasvindas
  ✔️ cadastro
  ✔️ info
  ✔️ interacoes
  ✔️ Logs
  ✔️ Moderacao
  ✔️ Util

📊 Resumo: 7 carregados, 0 com erro

✅ Keep-alive ativo na porta 8080
==================================================
🔁 BOT INICIALIZADO
==================================================
✅ Bot: NomeDoBot (ID: 123...)
🔧 Comandos sincronizados com servidor ID: 1377...
📦 Total de comandos prefix: 30+
🏠 Conectado a 1 servidor(es)
==================================================
```

---

## 📊 Comandos de Debug

### Verificar status do bot:
```
!ping
```

### Ver informações do bot:
```
!botinfo
```

### Recarregar um módulo (owner only):
```
!reload nome_do_modulo
```

### Ver logs do sistema:
No canal configurado em `CANAIS["logs"]`

---

## 🆘 Se Nada Funcionar

1. **Verifique o script de verificação:**
   ```bash
   python3 scripts/verificar.py
   ```

2. **Verifique os logs do terminal**

3. **Teste com bot mínimo:**
   ```python
   import discord
   import os
   
   bot = discord.Client(intents=discord.Intents.all())
   
   @bot.event
   async def on_ready():
       print(f'Bot conectado: {bot.user}')
   
   bot.run(os.getenv("DISCORD_TOKEN"))
   ```

4. **Abra uma issue com:**
   - Log de erro completo
   - Versão do Python: `python3 --version`
   - Versão do discord.py: `pip show discord.py`

---

## 📚 Recursos Úteis

- [Documentação Discord.py](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord.py Server](https://discord.gg/dpy)

---

## ✅ Checklist de Deploy

- [ ] Discord.py instalado
- [ ] DISCORD_TOKEN configurado
- [ ] IDs em config.py atualizados
- [ ] Bot convidado com permissões corretas
- [ ] Intents habilitados no Portal
- [ ] `!setupmute` executado
- [ ] Mensagem de cadastro criada
- [ ] Canais de logs existem
- [ ] Bot aparece online no Discord
- [ ] Comando `!ping` funciona

---

**Última atualização:** Dezembro 2025
