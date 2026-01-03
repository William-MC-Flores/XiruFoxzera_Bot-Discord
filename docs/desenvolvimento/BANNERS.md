# 🎨 Sistema de Banners e Personalização

## 📋 Visão Geral

O bot possui um sistema completo de personalização de perfis com **banners locais**, cores e títulos personalizados.

### ⚠️ IMPORTANTE: Banners APENAS Locais

**Usuários NÃO podem inserir links externos ou URLs de imagens.**

Todos os banners são arquivos locais armazenados na pasta `images/banners/` do projeto.

## 🗂️ Estrutura de Arquivos

```
images/
├── README.md
└── banners/
    ├── espaco.png      # Banner temático espacial
    ├── floresta.png    # Banner de floresta
    ├── oceano.png      # Banner oceano
    ├── montanhas.png   # Banner montanhas
    ├── cidade.png      # Banner urbano
    └── padrao.png      # Banner padrão
```

## 🛍️ Loja Virtual

Os banners são vendidos na loja:

```python
# Tabela loja
("Banner Espaço", 300, "banner", "Banner temático espacial", "banners/espaco.png")
("Banner Floresta", 250, "banner", "Banner de floresta", "banners/floresta.png")
```

**Campo `arquivo`** guarda o caminho relativo à pasta `images/`

## 💾 Banco de Dados

### Tabela `loja`
```sql
CREATE TABLE loja (
    id INTEGER PRIMARY KEY,
    nome_item TEXT,
    preco INTEGER,
    tipo_item TEXT,
    descricao TEXT,
    arquivo TEXT DEFAULT '',  -- ← Caminho do banner
    disponivel INTEGER DEFAULT 1
)
```

### Tabela `usuarios`
```sql
CREATE TABLE usuarios (
    ...
    banner_perfil TEXT DEFAULT '',  -- ← Armazena "banners/espaco.png"
    cor_perfil TEXT DEFAULT '#7289DA',
    titulo_perfil TEXT DEFAULT '',
    ...
)
```

## 🎮 Comandos

### Para Usuários

**!loja banner**
- Lista todos os banners disponíveis para compra

**!comprar <ID>**
- Compra um banner da loja

**!usaritem <ID>**
- Aplica o banner comprado ao perfil
- O bot lê o arquivo local e anexa ao embed

**!perfil [@usuário]**
- Mostra o perfil com o banner aplicado
- Banner é anexado como `discord.File()`

**!customizar**
- Menu de personalização
- **NÃO permite** inserir URLs de banners
- Apenas cores e títulos podem ser customizados manualmente

### Para Admins

**Adicionar novo banner:**

1. Coloque a imagem em `images/banners/novobannerhtml`
2. Execute no SQLite:
```sql
INSERT INTO loja (nome_item, preco, tipo_item, descricao, arquivo) 
VALUES ('Banner Novo', 400, 'banner', 'Descrição', 'banners/novo.png');
```

## 🔧 Implementação Técnica

### Como o banner é aplicado

```python
# 1. Usuário compra banner na loja
# O item é adicionado ao inventario

# 2. Usuário usa !usaritem <id>
cursor.execute('SELECT arquivo FROM loja WHERE id = ?', (id,))
arquivo = cursor.fetchone()[0]  # Ex: "banners/espaco.png"

cursor.execute('''
    UPDATE usuarios 
    SET banner_perfil = ? 
    WHERE id_discord = ?
''', (arquivo, user_id))

# 3. Ao mostrar !perfil
caminho_banner = f"images/{usuario['banner_perfil']}"
if os.path.exists(caminho_banner):
    arquivo_banner = discord.File(caminho_banner, filename="banner.png")
    embed.set_image(url="attachment://banner.png")
    await ctx.send(embed=embed, file=arquivo_banner)
```

### Validações

✅ **Apenas arquivos locais** - URLs externas são bloqueadas  
✅ **Verificação de existência** - `os.path.exists()` antes de enviar  
✅ **Integração com loja** - Banners devem ser comprados  
✅ **Rastreamento no inventário** - Sistema de posse de itens

## 🎨 Adicionar Imagens Reais

### Opção 1: Usar ImageMagick
```bash
cd images/banners
convert -size 1920x480 imagem.jpg -resize 1920x480^ -gravity center -extent 1920x480 espaco.png
```

### Opção 2: Substituir Manualmente
1. Crie/baixe imagens em 1920x480px
2. Salve em `images/banners/`
3. Mantenha os mesmos nomes dos arquivos

### Opção 3: Script Automatizado
```bash
./scripts/setup_banners.sh
```

## 📊 Tipos de Itens na Loja

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `banner` | Banners de perfil (arquivos locais) | Banner Espaço |
| `cor` | Cores de perfil (#HEX) | Cor Vermelho Fogo |
| `titulo` | Títulos especiais | Título Lendário |
| `badge` | Badges visuais | Badge VIP |
| `cargo` | Cargos Discord | Cargo Elite |
| `boost` | Multiplicadores temporários | Boost XP 24h |

## 🔒 Segurança

- ❌ Usuários **não podem** inserir URLs externas
- ❌ Usuários **não podem** fazer upload de imagens
- ✅ Apenas arquivos pré-aprovados na pasta `images/`
- ✅ Admins controlam quais banners estão disponíveis
- ✅ Validação de paths para prevenir directory traversal

## 📝 Notas Importantes

1. **Sempre use caminhos relativos** no campo `arquivo`
   - ✅ Correto: `"banners/espaco.png"`
   - ❌ Errado: `"/home/user/images/banners/espaco.png"`

2. **Tamanho das imagens**
   - Recomendado: 1920x480px
   - Máximo: 5MB
   - Formatos: PNG, JPG

3. **Performance**
   - Arquivos são lidos do disco a cada `!perfil`
   - Considere otimizar imagens (compressão)
   - Cache pode ser implementado futuramente

## 🚀 Expansões Futuras

- [ ] Sistema de upload para admins via Discord
- [ ] Banners animados (GIF)
- [ ] Preview de banners antes de comprar
- [ ] Banners sazonais/eventos
- [ ] Sistema de craft (combinar itens)
