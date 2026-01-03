# 🚀 Guia Rápido - Sistema de XP

## ⚡ Início Rápido (5 minutos)

### 1. O sistema já está pronto!
O módulo `Python/niveis.py` será carregado automaticamente quando você iniciar o bot.

### 2. Iniciar o Bot
```bash
python3 main.py
```

Você verá na console:
```
✅ Banco de dados de níveis inicializado
✔️ niveis
```

### 3. Testar no Discord

**Ganhar XP:**
```
Apenas envie mensagens no servidor!
Cada mensagem = 10 XP (cooldown de 60s)
```

**Ver seu perfil:**
```
!perfil
```

**Ver ranking:**
```
!ranking
```

**Admin - Adicionar XP:**
```
!addxp @usuário 1000
```

## 📋 Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!perfil` | Ver seu perfil | `!perfil` ou `!perfil @usuário` |
| `!ranking` | Ver top 10 | `!ranking` ou `!ranking 2` |
| `!addxp` | Adicionar XP (admin) | `!addxp @usuário 500` |
| `!resetperfil` | Resetar perfil (admin) | `!resetperfil @usuário` |

**Aliases:**
- `!perfil` = `!profile`, `!nivel`, `!level`
- `!ranking` = `!rank`, `!leaderboard`, `!top`
- `!resetperfil` = `!resetxp`

## 🎯 Tabela de Progressão

| Nível | XP Total | Mensagens (aprox.) |
|-------|----------|-------------------|
| 1     | 100      | 10                |
| 2     | 400      | 40                |
| 3     | 900      | 90                |
| 5     | 2,500    | 250               |
| 10    | 10,000   | 1,000             |
| 20    | 40,000   | 4,000             |
| 50    | 250,000  | 25,000            |

*Considerando 10 XP por mensagem*

## ❓ FAQ

**Q: O bot não está dando XP?**
- Aguarde 60 segundos entre mensagens (cooldown)
- Não use comandos (começam com `!`)
- Verifique se não é bot

**Q: Como ver todos os comandos?**
```
!ajuda niveis
```

**Q: Posso mudar a quantidade de XP?**
Sim! Edite `Python/niveis.py` linha 147:
```python
resultado = await self._adicionar_xp(message.author, 10)  # Mude 10
```

**Q: Onde fica o banco de dados?**
`data/niveis.db` - é criado automaticamente

**Q: Como fazer backup?**
```bash
cp data/niveis.db data/niveis_backup_$(date +%Y%m%d).db
```

## 🎨 Personalização Rápida

### Mudar Cooldown (padrão: 60s)
Edite `Python/niveis.py` linha 19:
```python
self.cooldown_time = 30  # 30 segundos
```

### Mudar Cor do Embed de Level Up
Edite `Python/niveis.py` linha 154:
```python
color=discord.Color.gold()  # Troque para .blue(), .green(), etc.
```

### Adicionar Mensagem Personalizada
Edite `Python/niveis.py` linha 153:
```python
description=f"🎉 Parabéns {message.author.mention}! Você subiu para o **nível {resultado['nivel_novo']}**!"
# Personalize a mensagem aqui
```

## 📊 Monitoramento

### Ver usuários no banco
```bash
sqlite3 data/niveis.db "SELECT nome, xp, nivel FROM usuarios ORDER BY xp DESC LIMIT 10;"
```

### Contar usuários
```bash
sqlite3 data/niveis.db "SELECT COUNT(*) FROM usuarios;"
```

### Ver top 5
```bash
sqlite3 data/niveis.db "SELECT nome, nivel, xp FROM usuarios ORDER BY xp DESC LIMIT 5;"
```

## 🐛 Troubleshooting

### Resetar banco completamente
```bash
rm data/niveis.db
python3 main.py  # Recria automaticamente
```

### Verificar erros
```bash
python3 scripts/test_niveis.py
```

### Logs do bot
Procure por:
```
✅ Banco de dados de níveis inicializado
```

Se não aparecer, há um problema no carregamento do módulo.

## 🎁 Dicas

1. **Eventos de XP em dobro:**
   Edite temporariamente a linha 147 para dar 20 XP ao invés de 10

2. **Recompensar atividade:**
   Use `!addxp` para dar XP bônus em eventos especiais

3. **Criar cargos por nível:**
   Use um bot de auto-roles ou crie um sistema custom

4. **Backup automático:**
   Configure um cron job:
   ```bash
   0 3 * * * cp /caminho/data/niveis.db /caminho/backups/niveis_$(date +\%Y\%m\%d).db
   ```

## 📚 Documentação Completa

Para mais detalhes, veja:
- [`docs/SISTEMA_XP.md`](../docs/SISTEMA_XP.md) - Documentação completa
- [`docs/IMPLEMENTACAO_XP.md`](../docs/IMPLEMENTACAO_XP.md) - Detalhes de implementação

## ✅ Pronto!

Seu sistema de XP está funcionando! 🎉

Qualquer dúvida, consulte a documentação ou os logs do bot.

---
**Última atualização:** 24/12/2025
