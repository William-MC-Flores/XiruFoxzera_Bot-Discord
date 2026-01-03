# 📁 Estrutura do Projeto

Documentação completa da organização do **Xiru Aftonzera Bot**.

## 🌳 Árvore de Diretórios

```
XiruAftonzera_Bot-Discord/
│
├── 📁 cogs/                    # Módulos do bot (Cogs)
│   ├── boasvindas.py           # Sistema de boas-vindas
│   ├── cadastro.py             # Auto-roles via reação
│   ├── info.py                 # Sistema de ajuda
│   ├── interacoes.py           # Respostas automáticas
│   ├── logger.py               # Logger centralizado
│   ├── Logs.py                 # Sistema de auditoria
│   ├── Moderacao.py            # Moderação completa
│   ├── niveis.py               # XP, economia e conquistas
│   └── Util.py                 # Comandos utilitários
│
├── 📁 data/                    # Dados persistentes
│   ├── niveis.db               # Banco de dados SQLite
│   └── warns.json              # Advertências
│
├── 📁 images/                  # Assets visuais
│   └── banners/                # Banners de perfil
│       ├── Cavalo_Crioulo.png
│       ├── Costelão.png
│       ├── Gauchada.png
│       ├── Laçador.png
│       ├── Proziada.png
│       └── Rio_Grandence.png
│
├── 📁 backups/                 # Backups automáticos
│   └── niveis_backup_*.db      # Snapshots do banco
│
├── 📁 docs/                    # Documentação
│   ├── 📁 guias/               # Guias de uso
│   │   ├── GUIA_DE_USO.md
│   │   ├── GUIA_RAPIDO_BANNERS.md
│   │   ├── GUIA_RAPIDO_XP.md
│   │   └── ATUALIZACAO_PERFIL_V1.1.md
│   │
│   ├── 📁 desenvolvimento/     # Documentação técnica
│   │   ├── ANALISE_PROJETO.md
│   │   ├── BACKUP_SISTEMA.md
│   │   ├── BANNERS.md
│   │   ├── BANCO_DADOS_CONFIRMACAO.md
│   │   ├── CHANGELOG_PERMISSOES.md
│   │   ├── IMPLEMENTACOES.md
│   │   ├── PERMISSOES.md
│   │   ├── RANKING_CONFIRMACAO.md
│   │   ├── RESUMO_FINAL_COMANDOS.md
│   │   └── REVISAO_CODIGO.md
│   │
│   ├── 📁 changelog/           # Histórico de versões
│   │
│   ├── README.md               # Índice da documentação
│   ├── STATUS.md               # Status do projeto
│   ├── TROUBLESHOOTING.md      # Solução de problemas
│   ├── ORGANIZACAO.md          # Organização do código
│   └── ESTRUTURA.md            # Este arquivo
│
├── 📁 scripts/                 # Scripts utilitários
│   ├── backup_database.py      # Sistema de backup
│   ├── auto_backup.sh          # Backup rápido
│   ├── dev.sh                  # Ambiente de desenvolvimento
│   └── verificar.py            # Verificação de integridade
│
├── 📄 main.py                  # Arquivo principal do bot
├── 📄 config.py                # Configurações centralizadas
├── 📄 keep_alive.py            # Keep-alive para Replit
│
├── 📄 .env                     # Variáveis de ambiente (SECRET)
├── 📄 .gitignore               # Arquivos ignorados pelo Git
├── 📄 .editorconfig            # Configuração de editor
│
├── 📄 requirements.txt         # Dependências Python
├── 📄 pyproject.toml           # Configuração do projeto
├── 📄 uv.lock                  # Lock de dependências
│
├── 📄 discloud.config          # Config para Discloud
├── 📄 README.md                # Documentação principal
└── 📄 CONTRIBUTING.md          # Guia de contribuição
```

---

## 📦 Módulos (Cogs)

### boasvindas.py
**Responsabilidade:** Mensagens de boas-vindas e despedidas
- `on_member_join` - Mensagem ao entrar
- `on_member_remove` - Mensagem ao sair
- `on_member_ban` - Notificação de banimento

### cadastro.py
**Responsabilidade:** Sistema de auto-roles
- `on_raw_reaction_add` - Adiciona cargo ao reagir
- `on_raw_reaction_remove` - Remove cargo ao remover reação

### info.py
**Responsabilidade:** Sistema de ajuda
- `!ajuda` - Central de ajuda com categorias

### interacoes.py
**Responsabilidade:** Respostas automáticas
- 30+ respostas pré-configuradas
- Detecção de palavras-chave

### Logs.py
**Responsabilidade:** Auditoria de eventos
- Logs de entrada/saída
- Logs de mensagens editadas/deletadas
- Logs de comandos executados
- Logs de mudanças em membros/canais

### Moderacao.py
**Responsabilidade:** Sistema completo de moderação
**Comandos:**
- `!warn`, `!verwarns`, `!clearwarns`, `!unwarn`
- `!mute`, `!unmute`, `!setupmute`
- `!kick`, `!ban`
- `!limpar` (bulk delete)
- Anti-spam automático

### niveis.py
**Responsabilidade:** XP, Economia e Conquistas
**Comandos:**
- XP: `!perfil`, `!ranking`, `!setxp`, `!setnivel`
- Economia: `!moedas`, `!daily`, `!trabalhar`, `!loja`, `!comprar`
- Customização: `!customizar`, `!usaritem`, `!inventario`
- Conquistas: `!conquistas`

### Util.py
**Responsabilidade:** Comandos utilitários
**Comandos:**
- Info: `!ping`, `!servidor`, `!avatar`, `!userinfo`, `!botinfo`
- Diversão: `!say`, `!coinflip`, `!dado`, `!8ball`
- Ferramentas: `!votacao`, `!embed`, `!sorteio`

---

## 💾 Banco de Dados

### niveis.db (SQLite3)

**Tabelas:**
1. `usuarios` - Dados de usuários (XP, moedas, perfil)
2. `conquistas` - Conquistas disponíveis
3. `usuarios_conquistas` - Relação usuário-conquistas
4. `loja` - Itens disponíveis para compra
5. `inventario` - Itens de cada usuário

**Proteção:**
- ✅ Excluído do Git (`.gitignore`)
- ✅ Backup automático via `scripts/backup_database.py`

---

## 📝 Configuração

### config.py
Configurações centralizadas:
- IDs de canais
- IDs de cargos de moderação
- Configurações de warns
- Configurações de anti-spam
- Cooldowns de comandos

### .env
Variáveis secretas:
```
DISCORD_TOKEN=seu_token_aqui
```

---

## 🔄 Fluxo de Desenvolvimento

1. **Desenvolvimento Local**
   ```bash
   python3 main.py
   ```

2. **Testes**
   ```bash
   python3 -m py_compile cogs/*.py
   ```

3. **Deploy**
   - Fazer backup: `python scripts/backup_database.py backup`
   - Commit: `git add . && git commit -m "feat: ..."`
   - Push: `git push origin main`
   - Deploy Discloud: Upload automático

---

## 📊 Métricas do Projeto

- **Linhas de código:** ~4,162
- **Módulos (Cogs):** 9
- **Comandos:** 48+
- **Eventos:** 15+
- **Conquistas:** 12
- **Itens na loja:** 31

---

**Última atualização:** 03/01/2026
