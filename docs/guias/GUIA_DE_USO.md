# 🚀 Guia de Uso - Bot Discord

## 📋 Início Rápido

### Para Usuários

#### 🎮 Ganhando XP e Moedas

**XP:**
- Envie mensagens no servidor: **+10 XP por mensagem**
- Limite anti-spam: **50 XP por minuto**
- Suba de nível automaticamente

**Moedas:**
- Envie mensagens: **+1 moeda por mensagem**
- Suba de nível: **+10 moedas por nível**

#### 👤 Perfil Personalizado

**Ver seu perfil:**
```
!perfil
!perfil @usuário
```

**Customizar cor e título:**
```
!customizar cor #FF5733
!customizar titulo 🎮 Gamer Pro
!customizar limpar
```

⚠️ **Banners só podem ser comprados na loja!**

#### 🛍️ Loja Virtual

**Ver categorias:**
```
!loja
```

**Ver itens de uma categoria:**
```
!loja banner    → Banners de perfil
!loja cor       → Cores personalizadas
!loja titulo    → Títulos especiais
!loja badge     → Badges exclusivas
!loja cargo     → Cargos especiais
!loja boost     → Boosts temporários
!loja todos     → Todos os itens
```

**Comprar item:**
```
!comprar 5
```

**Ver inventário:**
```
!inventario
!inventario @usuário
```

**Aplicar item comprado:**
```
!usaritem 3
```

#### 🏆 Conquistas

**Ver suas conquistas:**
```
!conquistas
!conquistas @usuário
```

**Conquistas disponíveis:**
- 📝 **Primeira Mensagem** - Envie sua primeira mensagem
- 💬 **Conversador** - Envie 100 mensagens
- 🗣️ **Falador** - Envie 1000 mensagens
- 🎤 **Ativo** - Fique 10 horas em canais de voz
- 👑 **Veterano do Servidor** - Complete 1 ano no servidor
- 🌱 **Novato** - Alcance nível 1
- 🔰 **Iniciante** - Alcance nível 5
- ⭐ **Experiente** - Alcance nível 10
- 🏆 **Veterano** - Alcance nível 20
- 👑 **Lenda** - Alcance nível 50
- 💎 **Colecionador de XP** - Acumule 10.000 XP
- 💠 **Mestre do XP** - Acumule 100.000 XP

#### 💰 Economia

**Ver saldo:**
```
!saldo
!saldo @usuário
```

**Transferir moedas:**
```
!pagar @usuário 100
```

**Ver ranking:**
```
!ranking
!ranking 2    (página 2)
```

#### ✏️ Editar Perfil

**Editar bio:**
```
!editarperfil bio Olá! Sou um gamer apaixonado por RPGs
```

**Editar status:**
```
!editarperfil status Online agora!
```

---

### Para Administradores

#### 👑 Comandos Owner

**Adicionar XP:**
```
!addxp @usuário 500
```

**Resetar perfil:**
```
!resetperfil @usuário
```

**Adicionar moedas:**
```
!addmoedas @usuário 1000
```

**Remover moedas:**
```
!removermoedas @usuário 500
```

**Definir moedas:**
```
!setmoedas @usuário 5000
```

#### 🛡️ Comandos Admin

**Dar moedas (limite 10k):**
```
!darmoedas @usuário 5000
```

#### 🖼️ Gerenciar Banners

**Adicionar novo banner:**

1. Adicione a imagem em `images/banners/novobannehtml`
   - Dimensão recomendada: 1920x480px
   - Formatos: PNG ou JPG

2. Adicione à loja no SQLite:
```sql
INSERT INTO loja (nome_item, preco, tipo_item, descricao, arquivo)
VALUES ('Banner Novo', 400, 'banner', 'Descrição incrível', 'banners/novo.png');
```

3. Pronto! Os usuários já podem comprar

**Remover banner:**
```sql
DELETE FROM loja WHERE id = 10;
```

**Tornar item indisponível:**
```sql
UPDATE loja SET disponivel = 0 WHERE id = 10;
```

---

## 🎨 Exemplos de Uso

### Exemplo 1: Personalizar Perfil Completo

```
# 1. Ganhe moedas enviando mensagens
(envie várias mensagens)

# 2. Verifique seu saldo
!saldo

# 3. Compre uma cor
!loja cor
!comprar 6    (Cor Vermelho Fogo)

# 4. Aplique a cor
!usaritem 6

# 5. Compre um título
!loja titulo
!comprar 11   (Título Lendário)

# 6. Aplique o título
!usaritem 11

# 7. Compre um banner
!loja banner
!comprar 1    (Banner Espaço)

# 8. Aplique o banner
!usaritem 1

# 9. Veja o resultado
!perfil
```

### Exemplo 2: Transfer de Moedas

```
# Ver seu saldo
!saldo
# Moedas: 500

# Transferir para amigo
!pagar @Amigo 100

# Verificar saldo do amigo
!saldo @Amigo
# Moedas: 100
```

### Exemplo 3: Desbloquear Conquistas

```
# Envie 1000 mensagens
(participe do servidor ativamente)

# Conquista desbloqueada automaticamente!
🏆 Conquista Desbloqueada!
@Você desbloqueou uma conquista!
🗣️ Falador
Enviou 1000 mensagens

# Veja suas conquistas
!conquistas
```

---

## ❓ FAQ

### Como ganho mais moedas rapidamente?
- Envie mensagens (1 moeda cada)
- Suba de nível (10 moedas por nível)
- Peça transferência de amigos

### Posso usar qualquer imagem como banner?
**NÃO.** Por segurança, apenas banners pré-aprovados da loja podem ser usados. Isso evita conteúdo inapropriado.

### Como funciona o sistema de XP?
- **+10 XP por mensagem**
- **Limite:** 50 XP por minuto (anti-spam)
- **Nível:** Calculado pela fórmula `floor(sqrt(xp / 100))`

### O que acontece se eu resetar meu perfil?
**CUIDADO!** Resetar o perfil:
- ❌ Remove todo XP
- ❌ Remove todas moedas
- ❌ Remove conquistas
- ❌ Reseta nível para 0
- ✅ Mantém itens do inventário

### Quanto tempo leva para desbloquear "Ativo"?
A conquista "Ativo" requer **10 horas** em canais de voz. O bot rastreia automaticamente seu tempo.

### Posso vender itens do inventário?
Não implementado ainda. Por enquanto, itens comprados são permanentes.

---

## 🐛 Solução de Problemas

### Bot não responde aos comandos
1. Verifique se o bot está online
2. Confirme que tem permissão para usar comandos
3. Teste com `!ajuda`

### !perfil não mostra o banner
1. Verifique se você comprou e aplicou o banner (`!usaritem`)
2. Confirme que o arquivo existe em `images/banners/`
3. Entre em contato com um admin

### Não ganhei XP pela mensagem
- Limite de 50 XP/minuto pode ter sido atingido
- Aguarde 1 minuto e tente novamente
- Bots não ganham XP

### Conquista não foi desbloqueada
- Verifique os requisitos com `!conquistas`
- Algumas conquistas levam tempo (Veterano = 1 ano)
- Entre em contato se achar que é um bug

---

## 📞 Suporte

Para dúvidas ou problemas:
- Use `!ajuda` para ver todos os comandos
- Leia a documentação em `/docs/`
- Entre em contato com administradores do servidor

---

**Última atualização:** 31/12/2025  
**Versão do bot:** 2.1.0
