# 🎨 Guia Completo de Customização

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Sistema de Loja](#sistema-de-loja)
- [Inventário e Equipagem](#inventário-e-equipagem)
- [Customização do Perfil](#customização-do-perfil)
- [Comandos Disponíveis](#comandos-disponíveis)
- [Exemplos Práticos](#exemplos-práticos)

---

## 🎯 Visão Geral

O sistema de customização permite que usuários personalizem seus perfis com:
- 🖼️ **6 Banners Gaucho** (450-600 moedas)
- 🎨 **5 Cores de perfil** (150-200 moedas)
- 👑 **3 Títulos especiais** (300-400 moedas)
- 🏅 **5 Badges exclusivas** (350-1000 moedas)
- ⚔️ **4 Cargos especiais** (1500-5000 moedas)
- ⚡ **3 Boosts temporários** (100-500 moedas)

**Total: 26 itens disponíveis**

---

## 🏪 Sistema de Loja

### Ver a Loja
```
!loja                 # Ver resumo de categorias
!loja banner          # Ver apenas banners
!loja cor             # Ver apenas cores
!loja titulo          # Ver apenas títulos
!loja badge           # Ver apenas badges
!loja cargo           # Ver apenas cargos
!loja boost           # Ver apenas boosts
!loja todos           # Ver todos os itens com IDs
```

### Comprar Itens
```
!comprar <ID>         # Comprar item pelo ID
```

**Exemplo:**
```
!loja banner
# Mostra:
# ✅ Banner Cavalo Crioulo (ID: 163) - 450 moedas
# ✅ Banner Costelão (ID: 164) - 500 moedas
# ...

!comprar 163          # Compra o Banner Cavalo Crioulo
```

### Verificar Saldo
```
!saldo                # Ver suas moedas
!saldo @usuário       # Ver moedas de outro usuário
```

---

## 🎒 Inventário e Equipagem

### Ver Inventário
```
!inventario           # Ver seus itens com IDs
!inv                  # Atalho
!inventário @usuário  # Ver inventário de outro usuário
```

**O que mostra:**
- ✅ Marca itens já equipados
- 📊 Total de itens e valor
- 🆔 **ID de cada item** para equipar
- 📦 Quantidade de cada item

### Equipar Itens
```
!usaritem <ID>        # Equipa item pelo ID
!equipar <ID>         # Atalho
!aplicar <ID>         # Atalho
```

**Exemplo:**
```
!inventario
# Mostra:
# 🖼️ Banner (2)
# ID 163 • Banner Cavalo Crioulo ✅
# ID 164 • Banner Costelão

!usaritem 164         # Troca para o Banner Costelão
```

### Ver Itens Equipados
```
!equipados            # Ver todos os itens ativos
!ativos               # Atalho
!equipados @usuário   # Ver itens de outro usuário
```

---

## 🎨 Customização do Perfil

### Customizar Manualmente
```
!customizar cor <código_hex>      # Mudar cor (grátis)
!customizar titulo <texto>        # Mudar título (grátis)
!customizar limpar                # Remover todas customizações
```

**Exemplos:**
```
!customizar cor #FF5733           # Cor vermelha
!customizar cor #00FF88           # Cor verde
!customizar titulo 🎮 Gamer Pro   # Adiciona título
!customizar limpar                # Remove tudo
```

### Editar Perfil
```
!editarperfil bio <texto>         # Define biografia (200 chars)
!editarperfil status <texto>      # Define status (50 chars)
!editarperfil limpar              # Remove bio e status
```

### Ver Perfil
```
!perfil               # Ver seu perfil completo
!perfil @usuário      # Ver perfil de outro usuário
!nivel                # Atalho
!profile              # Atalho em inglês
```

---

## 📝 Comandos Disponíveis

### Loja e Economia
| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!loja [categoria]` | Mostra a loja | `!loja banner` |
| `!comprar <ID>` | Compra um item | `!comprar 163` |
| `!saldo [@usuário]` | Mostra moedas | `!saldo` |
| `!pagar @usuário <valor>` | Transfere moedas | `!pagar @João 100` |

### Inventário e Equipagem
| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!inventario [@usuário]` | Ver inventário com IDs | `!inv` |
| `!usaritem <ID>` | Equipa item | `!usaritem 163` |
| `!equipados [@usuário]` | Ver itens equipados | `!equipados` |

### Customização
| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!customizar [opção] [valor]` | Customiza perfil | `!customizar cor #FF5733` |
| `!editarperfil [tipo] [texto]` | Edita bio/status | `!editarperfil bio Olá!` |
| `!perfil [@usuário]` | Ver perfil | `!perfil` |

---

## 💡 Exemplos Práticos

### Exemplo 1: Comprando e Equipando Banner
```bash
# 1. Ver banners disponíveis
!loja banner

# 2. Comprar banner (exemplo: Laçador)
!comprar 166

# 3. Ver inventário para confirmar
!inventario
# Mostra: ID 166 • Banner Laçador

# 4. Equipar o banner
!usaritem 166

# 5. Ver perfil atualizado
!perfil
```

### Exemplo 2: Customização Completa
```bash
# 1. Comprar itens
!comprar 163    # Banner Cavalo Crioulo
!comprar 203    # Cor Dourado
!comprar 211    # Título Lendário

# 2. Verificar inventário
!inventario

# 3. Equipar tudo
!usaritem 163   # Equipa banner
!usaritem 203   # Equipa cor
!usaritem 211   # Equipa título

# 4. Adicionar bio e status
!editarperfil bio "Amante da cultura gaúcha 🧉"
!editarperfil status "Tchê!"

# 5. Ver resultado final
!perfil
```

### Exemplo 3: Verificando Progresso
```bash
# Ver suas moedas
!saldo

# Ver itens equipados
!equipados

# Ver inventário completo
!inventario

# Ver conquistas
!conquistas

# Ver perfil completo
!perfil
```

---

## 🔧 Solução de Problemas

### Banner não aparece no perfil?

**Verificações:**
1. Confirme que comprou o banner: `!inventario`
2. Certifique-se de equipou: `!usaritem <ID>`
3. Verifique se está equipado: `!equipados`
4. Veja o perfil: `!perfil`

**Se ainda não funcionar:**
```bash
# 1. Execute diagnóstico
python3 scripts/diagnostico_customizacao.py

# 2. Verifique erros no console
# 3. Contate um administrador
```

### Não consigo encontrar o ID do item?

**Solução:**
```bash
# Use o inventário - ele mostra TODOS os IDs
!inventario

# Exemplo de saída:
# 🖼️ Banner (2)
# ID 163 • Banner Cavalo Crioulo ✅  <- Este é o ID!
# ID 164 • Banner Costelão
```

### Item não equipa?

**Verificações:**
1. Certifique-se que tem o item: `!inventario`
2. Use o ID correto (número que aparece no inventário)
3. Verifique tipo do item (banners, cores, títulos funcionam diferente)

---

## 📊 Estatísticas de Preços

### Banners (6 disponíveis)
- Banner Cavalo Crioulo: 450 moedas
- Banner Gauchada: 480 moedas
- Banner Costelão: 500 moedas
- Banner Rio Grandence: 520 moedas
- Banner Proziada: 550 moedas
- Banner Laçador: 600 moedas (mais caro)

### Cores (5 disponíveis)
- Vermelho Fogo, Azul Oceano, Verde Esmeralda, Roxo Real: 150 moedas
- Dourado: 200 moedas (premium)

### Títulos (3 disponíveis)
- Título Campeão: 300 moedas
- Título Mestre: 350 moedas
- Título Lendário: 400 moedas

### Badges (5 disponíveis)
- Badge Estrela: 350 moedas
- Badge VIP: 500 moedas
- Badge Coroa: 600 moedas
- Badge Desenvolvedor: 800 moedas
- Badge Diamante: 1000 moedas (mais cara)

---

## 🎯 Dicas

1. **Ganhe moedas:** +1 moeda por mensagem + 10 moedas por level up
2. **Economize:** Compre banners mais baratos primeiro
3. **Personalize:** Use `!customizar` para mudanças gratuitas (cor e título)
4. **Organize:** Use `!equipados` para ver o que está ativo
5. **Compartilhe:** Use `!perfil` para mostrar suas conquistas

---

## 🆘 Suporte

**Comandos de Ajuda:**
- `!ajuda` - Menu principal de ajuda
- `!ajuda economia` - Ajuda sobre loja e moedas
- `!ajuda niveis` - Ajuda sobre XP e níveis

**Administração:**
- `!addmoedas @usuário <valor>` - (Admin) Adicionar moedas
- `!addxp @usuário <valor>` - (Admin) Adicionar XP

---

## 📅 Atualizado em: 03/01/2026
**Versão do Sistema:** 2.1.0
