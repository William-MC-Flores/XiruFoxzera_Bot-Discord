#!/bin/bash
# Script para baixar imagens de banner de exemplo

echo "🖼️ Configurando banners de exemplo..."

cd "$(dirname "$0")/../images/banners"

# Função para criar placeholder PNG
create_placeholder() {
    local filename=$1
    local text=$2
    local color=$3
    
    # Usa ImageMagick se disponível, senão cria arquivo vazio
    if command -v convert &> /dev/null; then
        convert -size 1920x480 xc:"$color" -pointsize 60 -fill white -gravity center \
                -annotate +0+0 "$text" "$filename"
        echo "✅ Criado: $filename"
    else
        # Cria arquivo vazio como placeholder
        touch "$filename"
        echo "⚠️ Placeholder criado: $filename (instale ImageMagick para gerar imagens reais)"
    fi
}

# Cria banners de exemplo
create_placeholder "espaco.png" "🌌 ESPAÇO" "#1a1a2e"
create_placeholder "floresta.png" "🌲 FLORESTA" "#2d4a2b"
create_placeholder "oceano.png" "🌊 OCEANO" "#1e3a5f"
create_placeholder "montanhas.png" "⛰️ MONTANHAS" "#4a5759"
create_placeholder "cidade.png" "🏙️ CIDADE" "#2c3e50"
create_placeholder "padrao.png" "Discord Bot" "#7289da"

echo ""
echo "✅ Banners configurados!"
echo ""
echo "💡 Dicas:"
echo "   - Substitua os arquivos em images/banners/ por suas próprias imagens"
echo "   - Dimensão recomendada: 1920x480px"
echo "   - Formatos: PNG ou JPG"
echo "   - Tamanho máximo: 5MB"
