# 🎯 Guia Rápido - Banners e Backup

## 🖼️ Novos Banners Gaúchos Adicionados

✅ **11 banners** agora disponíveis na loja!

### Banners Temáticos Gaúchos (NOVOS):
- 🐴 **Banner Cavalo Crioulo** - 500 moedas
- 🥩 **Banner Costelão** - 600 moedas  
- 🎉 **Banner Gauchada** - 450 moedas
- 🤠 **Banner Laçador** - 550 moedas
- 🎊 **Banner Proziada** - 500 moedas
- 🏞️ **Banner Rio Grandence** - 480 moedas

### Banners Originais:
- 🌳 Banner Floresta - 250 moedas
- 🌊 Banner Oceano - 280 moedas
- 🌌 Banner Espaço - 300 moedas
- ⛰️ Banner Montanhas - 320 moedas
- 🏙️ Banner Cidade - 350 moedas

## 💰 Como Comprar e Usar

```
# 1. Ver banners disponíveis
!loja banner

# 2. Comprar um banner (exemplo: ID 163)
!comprar 163

# 3. Aplicar ao perfil
!usaritem 163

# 4. Ver resultado
!perfil
```

## 🔒 Sistema de Backup (IMPORTANTE!)

### Antes de Fazer Deploy/Commit:

```bash
# Criar backup dos dados
python scripts/backup_database.py backup

# Verificar backup criado
python scripts/backup_database.py list
```

### Fazer Commit SEM Perder Dados:

```bash
# O banco está protegido no .gitignore
# Apenas código será commitado

git add .
git commit -m "Sua mensagem"
git push
```

### Se Perder Dados (Emergência):

```bash
# 1. Listar backups
python scripts/backup_database.py list

# 2. Restaurar último backup
python scripts/backup_database.py restore niveis_backup_YYYYMMDD_HHMMSS.db
```

## 📁 Arquivos Importantes

```
✅ VERSIONADO (vai pro Git):
- Python/*.py (código)
- images/banners/*.png (imagens)
- scripts/*.py (scripts)
- README.md, docs/

❌ NÃO VERSIONADO (protegido):
- data/niveis.db (banco de dados)
- backups/ (backups)
- config.py (configurações)
- .env (tokens)
```

## 🎮 Testando Localmente

```bash
# 1. Criar backup
./scripts/auto_backup.sh

# 2. Iniciar bot
python main.py

# 3. Testar comandos no Discord:
!loja banner
!comprar 163
!usaritem 163
!perfil
```

## ⚠️ Checklist Antes de Deploy

- [ ] Backup criado com `python scripts/backup_database.py backup`
- [ ] Verificar que `data/niveis.db` NÃO está em `git status`
- [ ] Imagens dos banners estão em `images/banners/`
- [ ] Commit apenas do código
- [ ] Deploy para Discloud

## 🆘 Problemas Comuns

**Banner não aparece no perfil:**
- Verifique se comprou o item: `!inventario`
- Aplique com: `!usaritem <ID>`
- Confirme que arquivo existe em `images/banners/`

**Dados perdidos após deploy:**
- Restaure backup: `python scripts/backup_database.py restore <arquivo>`
- Configure .gitignore corretamente (já feito!)

**Backup não funciona:**
- Verifique permissões: `chmod +x scripts/*.sh`
- Execute manualmente: `python scripts/backup_database.py backup`

---

**Total de itens na loja:** 31 itens  
**Banners disponíveis:** 11 banners  
**Sistema de backup:** ✅ Ativo
