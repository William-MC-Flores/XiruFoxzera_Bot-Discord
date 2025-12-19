# 🤖 Bot Discord - Xiru Aftonzera

Bot de moderação e utilidades para Discord, desenvolvido para gerenciar servidores com eficiência.

## 📋 Funcionalidades

### 🛡️ Moderação
- **Sistema de Warns**: Advertências com histórico completo
- **Mute Automático**: 3 warns = mute automático
- **Anti-Spam**: Detecta e pune spam automaticamente
- **Comandos de Moderação**: kick, ban, limpar mensagens
- **Logs Completos**: Registro de todas ações

### 👋 Boas-Vindas
- Mensagens personalizadas de boas-vindas
- Notificações de saída e banimento
- Sistema de cadastro com reações

### ⚙️ Utilitários
- Comandos de informação (avatar, userinfo, serverinfo)
- Comandos de diversão (dado, 8ball, coinflip)
- Sistema de votação interativa
- Sorteios automáticos

### 💬 Interações
- Respostas automáticas customizáveis
- Reações automáticas em mensagens

## 🚀 Instalação

### Requisitos
- Python 3.11+
- Discord.py 2.3.2+
- Flask 3.0.0+ (para Replit)

### Configuração

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd Xiru-aftonzera
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure o bot**
   - Edite `config.py` com seus IDs de servidor, canais, etc.
   - Configure a variável de ambiente `DISCORD_TOKEN` com o token do bot

4. **Execute o bot**
```bash
python main.py
```

## ⚙️ Configuração

### config.py
Edite o arquivo `config.py` para personalizar:
- ID do servidor
- IDs de canais (logs, boas-vindas, saídas)
- ID da mensagem de cadastro
- Cargos de moderação
- Configurações de warns e anti-spam
- Cooldowns dos comandos

### Variáveis de Ambiente (Replit)
```
DISCORD_TOKEN=seu_token_aqui
```

## 📝 Comandos Principais

### Moderação
- `!warn <usuário> [motivo]` - Adverte um usuário
- `!mute <usuário> [tempo] [motivo]` - Silencia um usuário
- `!kick <usuário> [motivo]` - Expulsa um usuário
- `!ban <usuário> [motivo]` - Bane um usuário
- `!limpar <quantidade>` - Apaga mensagens

### Informação
- `!ajuda` - Mostra todos os comandos
- `!userinfo [usuário]` - Informações do usuário
- `!serverinfo` - Informações do servidor

### Utilitários
- `!votacao [pergunta]` - Inicia uma votação
- `!sorteio [tempo] [prêmio]` - Faz um sorteio
- `!dado [lados]` - Rola um dado
- `!8ball <pergunta>` - Bola mágica

## 🔧 Estrutura do Projeto

```
Xiru-aftonzera/
├── main.py              # Arquivo principal
├── config.py            # Configurações centralizadas
├── keep_alive.py        # Sistema keep-alive (Replit)
├── requirements.txt     # Dependências Python
├── data/                # Dados persistentes
│   └── warns.json      # Histórico de advertências
├── docs/                # Documentação completa
│   ├── README.md       # Documentação detalhada
│   ├── STATUS.md       # Status do projeto
│   └── TROUBLESHOOTING.md  # Solução de problemas
├── scripts/             # Scripts de desenvolvimento
│   ├── dev.sh          # Helper de comandos
│   ├── verificar.py    # Verificador de estrutura
│   └── test_conexao.py # Teste de conexão
├── Python/              # Módulos (Cogs)
│   ├── boasvindas.py   # Sistema de boas-vindas
│   ├── cadastro.py     # Sistema de auto-roles
│   ├── info.py         # Comandos de ajuda
│   ├── interacoes.py   # Interações automáticas
│   ├── logger.py       # Sistema de logs
│   ├── Logs.py         # Eventos de auditoria
│   ├── Moderacao.py    # Sistema de moderação
│   └── Util.py         # Comandos utilitários
└── .gitignore          # Arquivos ignorados pelo Git
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

## 👨‍💻 Autor

**Will Flores**
- GitHub: [@WillFlores-Fox](https://github.com/WillFlores-Fox)

## 📞 Suporte

Para suporte ou dúvidas:
- Abra uma [Issue](https://github.com/WillFlores-Fox/Bot_Server/issues)
- Entre em contato através do Discord

## 🎯 Roadmap

- [ ] Implementar comandos slash (/)
- [ ] Sistema de economia (coins virtuais)
- [ ] Sistema de tickets
- [ ] Dashboard web
- [ ] Comandos de música
- [ ] Sistema de níveis/XP

---

⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!
