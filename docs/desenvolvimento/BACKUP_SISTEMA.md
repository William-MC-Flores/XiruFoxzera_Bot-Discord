# 🔒 Sistema de Backup e Preservação de Dados

## ⚠️ Problema Identificado

Ao fazer commits e deploy para o Discloud, os dados do banco de dados `data/niveis.db` estavam sendo perdidos porque o arquivo era sobrescrito.

## ✅ Solução Implementada

### 1. **Proteção do Banco de Dados (.gitignore)**

O arquivo `.gitignore` foi atualizado para **NÃO** incluir o banco de dados no Git:

```gitignore
# Banco de dados (PROTEGIDO - mantém dados locais)
data/niveis.db
data/*.db
data/*.db-journal
data/*.db-wal
data/*.db-shm
```

Isso significa que:
- ✅ O banco de dados **NÃO** será sobrescrito ao fazer deploy
- ✅ Dados de usuários, conquistas e inventários são preservados
- ✅ Cada ambiente (local/produção) mantém seu próprio banco

### 2. **Sistema de Backup Automático**

Criado script Python completo para backups incrementais.

#### Comandos Disponíveis:

**Criar backup:**
```bash
python scripts/backup_database.py backup
# ou
./scripts/auto_backup.sh
```

**Listar backups:**
```bash
python scripts/backup_database.py list
```

**Restaurar backup:**
```bash
python scripts/backup_database.py restore niveis_backup_20260103_120000.db
```

#### Funcionalidades:

- 📦 Backups automáticos com timestamp
- 📊 Metadados JSON com estatísticas (usuários, conquistas, itens)
- 🗂️ Mantém últimos 30 backups (configurável)
- 🔄 Limpeza automática de backups antigos
- 💾 Backup de emergência antes de restaurar

### 3. **Estrutura de Arquivos**

```
projeto/
├── data/
│   └── niveis.db          # NÃO versionado (protegido)
├── backups/               # NÃO versionado
│   ├── niveis_backup_20260103_120000.db
│   ├── niveis_backup_20260103_120000_info.json
│   └── ...
├── scripts/
│   ├── backup_database.py # Sistema de backup
│   └── auto_backup.sh     # Script rápido
└── .gitignore             # Configurado para proteger dados
```

## 🚀 Workflow Recomendado

### Antes de Deploy:

```bash
# 1. Criar backup local
python scripts/backup_database.py backup

# 2. Verificar backup criado
python scripts/backup_database.py list

# 3. Fazer commit normalmente (banco não será incluído)
git add .
git commit -m "Atualização do código"
git push

# 4. Deploy para Discloud
# O banco de dados em produção será mantido!
```

### Após Deploy:

O banco de dados no Discloud **NÃO** será afetado porque:
- Está no `.gitignore`
- Apenas o código será atualizado
- Dados permanecem intactos

### Em Caso de Emergência:

**Se precisar restaurar dados:**

```bash
# 1. Listar backups disponíveis
python scripts/backup_database.py list

# 2. Restaurar backup específico
python scripts/backup_database.py restore niveis_backup_YYYYMMDD_HHMMSS.db
```

## 📋 Checklist de Segurança

Antes de cada deploy, execute:

- [ ] Criar backup: `./scripts/auto_backup.sh`
- [ ] Verificar .gitignore protege `data/*.db`
- [ ] Confirmar que banco NÃO está em `git status`
- [ ] Fazer commit apenas do código
- [ ] Deploy para Discloud

## 🔄 Backup Automático Periódico

Você pode agendar backups automáticos no cron (Linux):

```bash
# Editar crontab
crontab -e

# Adicionar linha para backup diário às 3h da manhã
0 3 * * * cd /caminho/do/projeto && ./scripts/auto_backup.sh
```

Ou no Windows (Task Scheduler):
- Criar tarefa agendada
- Executar: `python scripts/backup_database.py backup`
- Frequência: Diária

## 📊 Estatísticas do Backup

Cada backup inclui um arquivo `_info.json` com:

```json
{
  "timestamp": "20260103_120000",
  "date": "2026-01-03T12:00:00",
  "statistics": {
    "usuarios": 150,
    "itens_loja": 31,
    "conquistas": 12,
    "conquistas_desbloqueadas": 450,
    "itens_inventario": 89
  },
  "size_bytes": 49152
}
```

## ⚙️ Configurações

Edite `scripts/backup_database.py` para ajustar:

```python
MAX_BACKUPS = 30  # Quantos backups manter
BACKUP_DIR = "backups"  # Pasta de backups
DB_PATH = "data/niveis.db"  # Caminho do banco
```

## 🎯 Benefícios

✅ **Dados protegidos** contra perda acidental  
✅ **Deploy seguro** sem sobrescrever banco  
✅ **Histórico de backups** (últimos 30 dias)  
✅ **Fácil restauração** em caso de problemas  
✅ **Metadados detalhados** para auditoria  
✅ **Limpeza automática** de backups antigos  

## ❓ FAQ

**P: O banco será deletado ao fazer deploy?**  
R: Não! O `.gitignore` protege o arquivo.

**P: Como transferir dados entre ambientes?**  
R: Use os backups criados para copiar entre local/produção.

**P: Posso versionar o banco?**  
R: Não é recomendado. Use backups para histórico.

**P: E se eu quiser um banco "limpo" em produção?**  
R: Delete manualmente `data/niveis.db` no servidor e reinicie o bot.

## 🛡️ Segurança Adicional

Para proteção extra, considere:

1. **Backup na nuvem:**
   - Google Drive
   - Dropbox
   - AWS S3

2. **Backup automático antes do bot iniciar:**
   - Adicione no `main.py` antes de `bot.run()`

3. **Notificação de backup:**
   - Envie mensagem Discord quando backup é criado

---

**Última atualização:** 03/01/2026  
**Versão:** 2.2.0
