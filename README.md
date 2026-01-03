# 🧉 Xiru Aftonzera Bot

<div align="center">

![Discord](https://img.shields.io/badge/Discord-Bot-7289DA?style=for-the-badge&logo=discord&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Ativo-success?style=for-the-badge)

**Bot completo de moderação, economia e gamificação para servidores Discord**

[Documentação](#-documentação) • [Instalação](#-instalação) • [Comandos](#-comandos) • [Contribuir](CONTRIBUTING.md)

</div>

---

## ✨ Características

### 🛡️ Moderação
- Sistema de **warns** com punições automáticas
- **Anti-spam** inteligente
- Comandos de **mute**, **kick** e **ban**
- **Logs** completos de auditoria
- **Bulk delete** de mensagens

### 🎮 Gamificação
- Sistema de **XP e níveis**
- **12 conquistas** desbloqueáveis
- **Ranking** de usuários
- Rastreamento de **tempo em voz**
- Contador de **mensagens**

### 💰 Economia
- Sistema de **moedas**
- **Loja virtual** com 31 itens
- **Banners**, cores e títulos personalizados
- **Daily rewards** e trabalho
- **Inventário** de itens

### 🎨 Personalização
- **Perfis customizáveis** com banners locais
- **5 cores** de perfil
- **11 banners** (Gaucho themed)
- **Títulos** e **badges** exclusivos
- Bio e status personalizados

### 🤖 Automação
- **Boas-vindas** automáticas
- **Auto-roles** via reação
- **30+ respostas** automáticas
- Sistema de **backup** automático
- **Keep-alive** para uptime 24/7

---

## 🚀 Instalação

### ☁️ Discloud (Recomendado)

1. **Configure o token:**
   ```bash
   echo "DISCORD_TOKEN=seu_token_aqui" > .env
   ```

2. **Faça upload:**
   - Acesse [Discloud](https://discloud.app)
   - Upload o projeto completo
   - ✅ Pronto! Bot online 24/7

### 🔄 Replit

1. Adicione `DISCORD_TOKEN` nos **Secrets**
2. Clique em **Run**
3. ✅ Bot rodando!

### 💻 Local

```bash
# Clone o repositório
git clone <seu-repo>
cd XiruAftonzera_Bot-Discord

# Instale dependências
pip install -r requirements.txt

# Configure .env
echo "DISCORD_TOKEN=seu_token_aqui" > .env

# Execute
python3 main.py
```

---

## 📚 Documentação

### �� Guias
- [Guia de Uso](docs/guias/GUIA_DE_USO.md) - Como usar o bot
- [Banners](docs/guias/GUIA_RAPIDO_BANNERS.md) - Sistema de banners
- [XP e Níveis](docs/guias/GUIA_RAPIDO_XP.md) - Como funciona o XP

### 🔧 Técnica
- [Estrutura](docs/ESTRUTURA.md) - Organização do projeto
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Solução de problemas
- [Status](docs/STATUS.md) - Estado do projeto

### 👨‍💻 Desenvolvimento
- [Contributing](CONTRIBUTING.md) - Como contribuir
- [Revisão de Código](docs/desenvolvimento/REVISAO_CODIGO.md)
- [Organização](docs/ORGANIZACAO.md)

---

## 🎯 Comandos

### 🛡️ Moderação
\`\`\`
!warn @usuário [motivo]     # Advertir usuário
!verwarns @usuário          # Ver advertências
!mute @usuário [tempo]      # Silenciar usuário
!kick @usuário [motivo]     # Expulsar usuário
!ban @usuário [motivo]      # Banir usuário
!limpar [quantidade]        # Deletar mensagens
\`\`\`

### ⭐ Níveis e XP
\`\`\`
!perfil [@usuário]          # Ver perfil
!ranking [página]           # Ranking de XP
!top                        # Top 10
!conquistas [@usuário]      # Ver conquistas
\`\`\`

### 💰 Economia
\`\`\`
!moedas [@usuário]          # Ver moedas
!daily                      # Recompensa diária
!trabalhar                  # Ganhar moedas
!loja [categoria]           # Ver loja
!comprar <ID>               # Comprar item
!inventario [@usuário]      # Ver inventário
!usaritem <ID>              # Usar/equipar item
\`\`\`

### 🎨 Personalização
\`\`\`
!customizar cor #HEXCODE    # Mudar cor do perfil
!customizar titulo <texto>  # Definir título
!editarperfil bio <texto>   # Definir bio
!editarperfil status <texto># Definir status
\`\`\`

### 🛠️ Utilitários
\`\`\`
!ajuda [categoria]          # Central de ajuda
!ping                       # Latência do bot
!servidor                   # Info do servidor
!avatar [@usuário]          # Avatar de usuário
!votacao <pergunta>         # Criar votação
!sorteio <tempo> <premio>   # Criar sorteio
\`\`\`

**Ver todos:** \`!ajuda\`

---

## 🏆 Conquistas

Sistema com **12 conquistas** baseadas em:
- 💬 **Mensagens** (100, 1000, 5000)
- ⭐ **Níveis** (5, 10, 20)
- 💎 **XP** (1000, 5000, 10000)
- 🎤 **Tempo em voz** (10 horas)
- 🎂 **Tempo no servidor** (1 ano)
- 🛒 **Compras** (primeira, 10 itens)

---

## 🏪 Loja Virtual

### 31 Itens Disponíveis

- **11 Banners** (5 genéricos + 6 Gaucho themed)
- **5 Cores** de perfil
- **5 Badges** exclusivos
- **4 Cargos** especiais
- **3 Títulos** personalizados
- **3 Boosts** temporários

**Preços:** 100 - 800 moedas

---

## 📊 Estatísticas

- 📝 **~4,162** linhas de código
- 🤖 **48+** comandos
- 🎯 **12** conquistas
- 🛒 **31** itens na loja
- 🗂️ **5** tabelas no banco
- 🧩 **9** módulos (cogs)

---

## 🛠️ Tecnologias

- **[Python 3.10+](https://python.org)**
- **[discord.py 2.3.2+](https://discordpy.readthedocs.io)**
- **[SQLite3](https://sqlite.org)** - Banco de dados
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Variáveis de ambiente

---

## 📁 Estrutura

\`\`\`
XiruAftonzera_Bot-Discord/
├── cogs/              # Módulos do bot
├── data/              # Banco de dados
├── images/            # Assets (banners)
├── docs/              # Documentação
│   ├── guias/
│   ├── desenvolvimento/
│   └── changelog/
├── scripts/           # Scripts utilitários
├── main.py            # Arquivo principal
└── config.py          # Configurações
\`\`\`

**[Ver estrutura completa](docs/ESTRUTURA.md)**

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja o [Guia de Contribuição](CONTRIBUTING.md).

### Como ajudar:
- 🐛 Reportar bugs
- ✨ Sugerir features
- 📝 Melhorar documentação
- 💻 Contribuir com código

---

## 📜 Licença

Este projeto foi criado para uso privado. Sinta-se livre para usar como referência.

---

## 📞 Suporte

- 📖 [Documentação](docs/README.md)
- 🔧 [Troubleshooting](docs/TROUBLESHOOTING.md)
- 💬 Abra uma **Issue** para bugs ou dúvidas

---

<div align="center">

**Feito com 💚 para a comunidade Gaucha** 🧉

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2+-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

</div>
