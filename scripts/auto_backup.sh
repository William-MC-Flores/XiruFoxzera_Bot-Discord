#!/bin/bash
# Script de backup automático
# Executa backup do banco de dados antes de operações críticas

echo "🔄 Iniciando backup automático..."

# Vai para o diretório do projeto
cd "$(dirname "$0")/.."

# Executa o backup
python3 scripts/backup_database.py backup

if [ $? -eq 0 ]; then
    echo "✅ Backup concluído com sucesso!"
    exit 0
else
    echo "❌ Falha no backup!"
    exit 1
fi
