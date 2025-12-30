# 🔐 Sistema de Permissões do Bot

## Estrutura de Permissões

### ⚙️ Comandos Exclusivos do Fundador (Owner-Only)
**Requer:** Ser o dono do bot no Discord
**Decorator:** `@commands.is_owner()`

| Comando | Descrição | Arquivo |
|---------|-----------|---------|
| `!addxp <usuário> <quantidade>` | Adiciona XP a um usuário | niveis.py |
| `!resetperfil <usuário>` | Reseta completamente o perfil de um usuário | niveis.py |
| `!addmoedas <usuário> <quantidade>` | Adiciona moedas a um usuário | niveis.py |
| `!removermoedas <usuário> <quantidade>` | Remove moedas de um usuário | niveis.py |
| `!setmoedas <usuário> <quantidade>` | Define o saldo de moedas de um usuário | niveis.py |

### 🛡️ Comandos de Administrador
**Requer:** Permissão de Administrador no servidor
**Decorator:** `@commands.has_permissions(administrator=True)`

| Comando | Descrição | Arquivo |
|---------|-----------|---------|
| `!setupmute` | Configura o cargo de Mutado | Moderacao.py |

### 👮 Comandos de Moderação
**Requer:** Cargo autorizado (Moderador, Admin, etc.)
**Verificação:** `tem_cargo_autorizado(membro)`

| Comando | Descrição | Arquivo |
|---------|-----------|---------|
| `!warn <usuário> <motivo>` | Adverte um usuário | Moderacao.py |
| `!verwarns <usuário>` | Ver advertências de um usuário | Moderacao.py |
| `!clearwarns <usuário>` | Limpa todas as advertências | Moderacao.py |
| `!unwarn <usuário> <índice>` | Remove advertência específica | Moderacao.py |
| `!warnslist` | Lista todos com advertências | Moderacao.py |
| `!mute <usuário> <tempo> <motivo>` | Muta temporariamente | Moderacao.py |
| `!unmute <usuário>` | Remove mute | Moderacao.py |
| `!limpar <quantidade>` | Limpa mensagens do canal | Moderacao.py |
| `!ban <usuário> <motivo>` | Bane do servidor | Moderacao.py |
| `!kick <usuário> <motivo>` | Expulsa do servidor | Moderacao.py |

### 👥 Comandos Públicos
**Requer:** Nenhuma permissão especial
**Acessível:** Todos os membros

#### Sistema de Níveis e Economia
| Comando | Descrição | Arquivo |
|---------|-----------|---------|
| `!perfil [usuário]` | Ver perfil e XP | niveis.py |
| `!rank [página]` | Top 10 do servidor | niveis.py |
| `!saldo [usuário]` | Ver saldo de moedas | niveis.py |
| `!pagar <usuário> <quantidade>` | Transferir moedas | niveis.py |
| `!ranking [página]` | Ranking de moedas | niveis.py |
| `!loja [categoria]` | Ver itens da loja | niveis.py |
| `!comprar <id>` | Comprar item | niveis.py |
| `!inventario [usuário]` | Ver inventário | niveis.py |

#### Utilidades e Diversão
| Comando | Descrição | Arquivo |
|---------|-----------|---------|
| `!coinflip` | Cara ou coroa | Util.py |
| `!dado [lados]` | Rola um dado | Util.py |
| `!escolher <opção1> <opção2> ...` | Escolhe aleatoriamente | Util.py |
| `!say <mensagem>` | Bot repete mensagem | Util.py |
| `!embed <título> \| <descrição>` | Cria embed | Util.py |
| `!votacao <título> \| <opções>` | Cria votação | Util.py |
| `!sorteio <tempo> <prêmio>` | Cria sorteio | Util.py |

#### Informações
| Comando | Descrição | Arquivo |
|---------|-----------|---------|
| `!ping` | Latência do bot | info.py |
| `!serverinfo` | Informações do servidor | info.py |
| `!userinfo [usuário]` | Informações do usuário | info.py |
| `!avatar [usuário]` | Avatar do usuário | info.py |
| `!help [comando]` | Ajuda sobre comandos | info.py |

## 🔄 Mudanças Recentes

### Implementadas em $(date +%Y-%m-%d)

#### ✅ Comandos Migrados para Owner-Only
- `!addxp` - Antes: Administrator → Agora: **Owner**
- `!resetperfil` - Antes: Administrator → Agora: **Owner**

#### ✨ Novos Comandos Owner-Only
- `!addmoedas` - Gerenciamento direto de moedas
- `!removermoedas` - Remoção de moedas
- `!setmoedas` - Definir saldo exato

#### 🗑️ Comandos Desabilitados
- `!8ball` - Removido (comando de diversão pouco usado)
  - *Para reativar: descomentar em Util.py*

## 📝 Configuração de Cargos Moderadores

Em [config.py](../config.py):
```python
ROLES_MODERACAO = ["Moderador", "Admin", "Staff"]
```

## 🚨 Mensagens de Erro

### Owner-Only Commands
```
🚫 Apenas o fundador do bot pode usar este comando!
```

### Administrator Commands
```
🚫 Você não tem permissão de administrador!
```

### Moderação Commands
```
🚫 Você não tem permissão de moderação!
```

## 🔍 Como Verificar Permissões

### Verificar se é Owner
O bot verifica automaticamente se o ID do usuário corresponde ao dono configurado no Discord.

### Verificar se é Administrador
```python
@commands.has_permissions(administrator=True)
```

### Verificar se tem Cargo de Moderação
```python
tem_cargo_autorizado(membro)  # Verifica se possui algum cargo em ROLES_MODERACAO
```

## 🛠️ Desenvolvimento

### Adicionar Novo Comando Owner-Only
```python
@commands.command(name="meucomando")
@commands.is_owner()
async def meu_comando(self, ctx):
    # seu código aqui
    pass

@meu_comando.error
async def meu_comando_error(self, ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("🚫 Apenas o fundador do bot pode usar este comando!")
```

### Adicionar Novo Comando de Moderação
```python
@commands.command(name="meucomando")
async def meu_comando(self, ctx):
    if not tem_cargo_autorizado(ctx.author):
        await ctx.send("🚫 Você não tem permissão de moderação!")
        return
    # seu código aqui
```

---
**Atualizado:** $(date +%Y-%m-%d)  
**Versão:** 1.0  
**Segurança:** Alta
