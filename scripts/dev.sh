#!/bin/bash
# Script auxiliar para desenvolvimento do bot

case "$1" in
    "verificar")
        echo "🔍 Verificando projeto..."
        cd "$(dirname "$0")/.." && python3 scripts/verificar.py
        ;;
    
    "testar")
        echo "🧪 Testando conexão..."
        cd "$(dirname "$0")/.." && python3 scripts/test_conexao.py
        ;;
    
    "executar"|"run")
        echo "🚀 Iniciando bot..."
        cd "$(dirname "$0")/.." && python3 main.py
        ;;
    
    "sintaxe")
        echo "🔍 Verificando sintaxe..."
        cd "$(dirname "$0")/.." && python3 -m py_compile main.py keep_alive.py config.py Python/*.py 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Sintaxe OK!"
        else
            echo "❌ Erros de sintaxe encontrados"
        fi
        ;;
    
    "limpar")
        echo "🧹 Limpando arquivos temporários..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -name "*.pyc" -delete 2>/dev/null
        find . -name "*.pyo" -delete 2>/dev/null
        find . -name "*.bak" -delete 2>/dev/null
        echo "✅ Limpeza concluída!"
        ;;
    
    "backup")
        echo "💾 Criando backup..."
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        BACKUP_NAME="backup_$TIMESTAMP.tar.gz"
        tar -czf "backups/$BACKUP_NAME" \
            --exclude="__pycache__" \
            --exclude="*.pyc" \
            --exclude="*.bak" \
            --exclude="backups" \
            *.py Python/*.py config.py warns.json *.md *.txt .gitignore 2>/dev/null
        echo "✅ Backup criado: backups/$BACKUP_NAME"
        ;;
    
    "dependencias"|"deps")
        echo "📦 Instalando dependências..."
        cd "$(dirname "$0")/.." && pip install -r requirements.txt
        echo "✅ Dependências instaladas!"
        ;;
    
    "status")
        echo "📊 Status do projeto:"
        echo "---"
        cd "$(dirname "$0")/.." && python3 scripts/verificar.py
        ;;
    
    "ajuda"|"help"|*)
        echo "🤖 Bot Discord - Comandos Disponíveis"
        echo "======================================"
        echo ""
        echo "  ./dev.sh verificar    - Verifica estrutura e sintaxe"
        echo "  ./dev.sh testar       - Testa conexão com Discord"
        echo "  ./dev.sh executar     - Inicia o bot"
        echo "  ./dev.sh sintaxe      - Verifica sintaxe Python"
        echo "  ./dev.sh limpar       - Remove arquivos temporários"
        echo "  ./dev.sh backup       - Cria backup do projeto"
        echo "  ./dev.sh dependencias - Instala dependências"
        echo "  ./dev.sh status       - Mostra status completo"
        echo "  ./dev.sh ajuda        - Mostra esta mensagem"
        echo ""
        echo "======================================"
        ;;
esac
