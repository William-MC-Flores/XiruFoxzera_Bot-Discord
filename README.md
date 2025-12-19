# 🤖 Bot Discord - Xiru Aftonzera

Bot de moderação e utilidades para Discord com sistema completo de gerenciamento de servidor.

## 🚀 Início Rápido

### Replit
1. Configure `DISCORD_TOKEN` nos Secrets
2. Clique em **Run**
3. Pronto! ✅

### Local
```bash
pip install -r requirements.txt
export DISCORD_TOKEN="seu_token_aqui"
python3 main.py
```

## 📚 Documentação

- 📖 [Documentação Completa](docs/README.md)
- 🔧 [Solução de Problemas](docs/TROUBLESHOOTING.md)
- 📊 [Status do Projeto](docs/STATUS.md)
- 🗂️ [Estrutura e Organização](docs/ORGANIZACAO.md)

## 🛠️ Scripts Úteis

```bash
# Verificar projeto
./scripts/dev.sh verificar

# Testar conexão
./scripts/dev.sh testar

# Executar bot
./scripts/dev.sh executar
```

## 📁 Estrutura do Projeto

```
Xiru-aftonzera/
├── 📄 main.py              # Arquivo principal do bot
├── ⚙️ config.py            # Configurações centralizadas
├── 🔄 keep_alive.py        # Keep-alive para Replit
├── 📦 requirements.txt     # Dependências
├── 
├── 📂 Python/              # Módulos do bot (Cogs)
│   ├── boasvindas.py      # Sistema de boas-vindas
│   ├── cadastro.py        # Auto-roles por reação
│   ├── info.py            # Comandos de ajuda
│   ├── interacoes.py      # Interações automáticas
│   ├── logger.py          # Sistema de logging
│   ├── Logs.py            # Eventos de auditoria
│   ├── Moderacao.py       # Sistema de moderação
│   └── Util.py            # Comandos utilitários
│
├── 📂 docs/                # Documentação
│   ├── README.md          # Documentação completa
│   ├── STATUS.md          # Status do projeto
│   └── TROUBLESHOOTING.md # Solução de problemas
│
├── 📂 scripts/             # Scripts auxiliares
│   ├── verificar.py       # Verificação do projeto
│   ├── test_conexao.py    # Teste de conexão
│   └── dev.sh             # Script de desenvolvimento
│
├── 📂 data/                # Dados persistentes
│   └── warns.json         # Advertências dos usuários
│
└── 📂 backups/             # Backups automáticos
```

## ✨ Funcionalidades

- 🛡️ **Moderação Completa** - Warns, mutes, kicks, bans
- 🤖 **Anti-Spam Automático** - Detecta e pune spam
- 👋 **Boas-Vindas** - Mensagens automáticas personalizadas
- 🎭 **Auto-Roles** - Sistema de cargos por reação
- 📊 **Logs Completos** - Auditoria de todas ações
- 🎮 **Comandos Divertidos** - Jogos e interações
- ⚙️ **Altamente Configurável** - Tudo em config.py

## 📋 Comandos Principais

| Categoria | Comandos |
|-----------|----------|
| 🛡️ Moderação | `!warn`, `!mute`, `!kick`, `!ban`, `!limpar` |
| ℹ️ Informação | `!ajuda`, `!userinfo`, `!serverinfo` |
| 🎮 Diversão | `!coinflip`, `!dado`, `!8ball`, `!sorteio` |
| ⚙️ Utilitários | `!avatar`, `!ping`, `!votacao` |

Use `!ajuda` no Discord para ver todos os comandos!

## 🔧 Configuração

1. **Obter Token do Bot:**
   - Acesse [Discord Developer Portal](https://discord.com/developers/applications)
   - Crie um novo Application
   - Vá em Bot → Reset Token
   - Copie o token

2. **Configurar IDs:**
   - Edite `config.py` com IDs do seu servidor
   - Ative Modo Desenvolvedor no Discord
   - Clique direito → Copiar ID

3. **Convidar Bot:**
   - OAuth2 → URL Generator
   - Selecione: `bot`, `applications.commands`
   - Permissões: `Administrator`
   - Use o link gerado

4. **Ativar Intents:**
   - Bot → Privileged Gateway Intents
   - Ative **Message Content Intent** ⚠️ Obrigatório
   - Ative Server Members Intent
   - Ative Presence Intent

## 💡 Primeiros Comandos

Após o bot estar online:

```discord
!setupmute              # Configura sistema de mute
!criar_mensagem_cadastro # Cria mensagem de auto-roles
!add_reacoes            # Adiciona reações na mensagem
!ping                   # Testa funcionamento
```

## 🆘 Suporte

Problemas? Consulte a [documentação completa](docs/TROUBLESHOOTING.md) ou execute:

```bash
./scripts/dev.sh verificar
```

## 👨‍💻 Desenvolvimento

```bash
# Verificar estrutura
./scripts/dev.sh verificar

# Testar sintaxe
./scripts/dev.sh sintaxe

# Limpar cache
./scripts/dev.sh limpar

# Criar backup
./scripts/dev.sh backup
```

## 📊 Estatísticas

- **Linhas de código:** 1500+
- **Comandos:** 40+
- **Sistemas:** 7
- **Eventos monitorados:** 15+

## 📜 Licença

Este projeto é de código aberto para uso pessoal e educacional.

## 👤 Autor

**Will Flores**
- GitHub: [@WillFlores-Fox](https://github.com/WillFlores-Fox)

---

⭐ Se este projeto foi útil, considere dar uma estrela!

**Status:** ✅ Pronto para produção | **Versão:** 2.0
