# ⭐ Sistema de Níveis e XP

Sistema completo de experiência, níveis e ranking para o Bot Xiru Foxzera.

## 📊 Como Funciona

### Ganho de XP
- **10 XP** por mensagem enviada
- **Cooldown**: 60 segundos entre ganhos (evita spam)
- **Mensagens ignoradas**: Comandos (começam com `!`) e mensagens de bots

### Cálculo de Nível
A fórmula para calcular o nível é:
```
Nível = floor(√(XP / 100))
```

**Exemplo de progressão:**
- Nível 1: 100 XP
- Nível 2: 400 XP
- Nível 3: 900 XP
- Nível 4: 1,600 XP
- Nível 5: 2,500 XP
- Nível 10: 10,000 XP
- Nível 20: 40,000 XP
- Nível 50: 250,000 XP

### Notificações
Quando um usuário sobe de nível, o bot envia automaticamente uma mensagem de parabéns no canal onde a mensagem foi enviada.

## 🎮 Comandos

### Para Todos os Usuários

#### `!perfil [@usuário]`
Mostra o perfil de XP e nível do usuário.

**Aliases:** `!profile`, `!nivel`, `!level`

**Uso:**
```
!perfil          # Mostra seu próprio perfil
!perfil @Usuário # Mostra perfil de outro usuário
```

**Informações exibidas:**
- Nível atual
- XP total acumulado
- Próximo nível
- Barra de progresso visual
- XP faltante para o próximo nível

#### `!ranking [página]`
Mostra o ranking dos 10 usuários com mais XP.

**Aliases:** `!rank`, `!leaderboard`, `!top`

**Uso:**
```
!ranking     # Mostra top 10
!ranking 2   # Mostra página 2 (posições 11-20)
```

**Características:**
- Top 3 ganham medalhas especiais (🥇🥈🥉)
- Mostra nome, nível e XP de cada usuário
- Paginação para ver além do top 10

### Para Administradores

#### `!addxp @usuário <quantidade>`
Adiciona XP manualmente a um usuário.

**Permissão necessária:** Administrador

**Uso:**
```
!addxp @Usuário 100   # Adiciona 100 XP
!addxp @Usuário 1000  # Adiciona 1000 XP
```

**Características:**
- Quantidade deve ser maior que zero
- Mostra se o usuário subiu de nível
- Exibe status atualizado do usuário

#### `!resetperfil @usuário`
Reseta completamente o XP e nível de um usuário.

**Alias:** `!resetxp`

**Permissão necessária:** Administrador

**Uso:**
```
!resetperfil @Usuário
```

**Atenção:** Esta ação é irreversível!

## 🗄️ Banco de Dados

### Estrutura
O sistema usa SQLite para armazenamento persistente local.

**Arquivo:** `data/niveis.db`

**Tabela `usuarios`:**
```sql
CREATE TABLE usuarios (
    id_discord INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    xp INTEGER DEFAULT 0,
    nivel INTEGER DEFAULT 0
)
```

### Funcionamento
- **Auto-criação**: Usuários são criados automaticamente ao enviar a primeira mensagem
- **Auto-atualização**: Nomes são atualizados automaticamente se mudarem
- **Persistência**: Dados são salvos imediatamente após cada ganho de XP

## 🎨 Recursos Visuais

### Embed de Level Up
Quando um usuário sobe de nível, recebe:
- Título "🎉 Level Up!"
- Menção do usuário
- Nível anterior vs. novo
- XP total acumulado
- Cor dourada no embed

### Embed de Perfil
- Thumbnail com avatar do usuário
- Cor personalizada do usuário
- Campos organizados com emojis
- Barra de progresso visual (10 blocos)
- Porcentagem de progresso
- ID do usuário no rodapé

### Embed de Ranking
- Cor dourada
- Medalhas para top 3 (🥇🥈🥉)
- Numeração para demais posições
- Informação de paginação no rodapé

## ⚙️ Configurações

### Cooldown de XP
**Padrão:** 60 segundos

Para alterar, edite no arquivo `Python/niveis.py`:
```python
self.cooldown_time = 60  # Segundos entre ganhos de XP
```

### Quantidade de XP por Mensagem
**Padrão:** 10 XP

Para alterar, edite no arquivo `Python/niveis.py`, linha:
```python
resultado = await self._adicionar_xp(message.author, 10)
```

### Fórmula de Nível
Para alterar a progressão, edite a função `_calcular_nivel`:
```python
def _calcular_nivel(self, xp: int) -> int:
    return math.floor(math.sqrt(xp / 100))
```

## 🔮 Expansões Futuras

O código foi estruturado para facilitar estas expansões:

### Sistema de Moedas
- Adicionar coluna `moedas` na tabela
- Ganhar moedas ao subir de nível
- Comando `!coins` ou `!moedas`

### Loja de Recompensas
- Comprar itens com XP ou moedas
- Cargos especiais
- Cores personalizadas
- Permissões temporárias

### Sistema de Conquistas
- Nova tabela `conquistas`
- Relacionamento com usuários
- Badges no perfil
- XP bônus por conquistas

### Multiplicadores de XP
- Eventos especiais (fim de semana, etc.)
- Boost por servidor boosted
- Bônus por cargos especiais
- Streak de mensagens diárias

### Personalização de Perfil
- Banners customizados
- Biografias
- Títulos e badges
- Cards de perfil com imagens

## 🐛 Troubleshooting

### Bot não está dando XP
1. Verifique se o arquivo `data/niveis.db` foi criado
2. Confira se você não está em cooldown (60s)
3. Certifique-se de que não está enviando comandos (`!`)
4. Verifique os logs do bot para erros

### Comando de ranking vazio
- O ranking só mostra usuários que já ganharam XP
- Envie algumas mensagens primeiro para aparecer

### Erro ao usar !addxp
- Certifique-se de ter permissão de Administrador
- Mencione o usuário corretamente com `@`
- Use um número positivo para a quantidade

### Banco de dados corrompido
Para resetar completamente:
```bash
rm data/niveis.db
# O bot recriará automaticamente ao iniciar
```

## 📝 Notas Técnicas

### Performance
- Queries SQL otimizadas com índice na PRIMARY KEY
- Cooldown em memória (não salvo no banco)
- Cálculos de nível em Python (não SQL)

### Segurança
- Proteção contra SQL injection (parametrized queries)
- Validação de tipos nos comandos
- Tratamento de erros robusto
- Permissões verificadas para comandos admin

### Compatibilidade
- Python 3.10+
- discord.py 2.3.2+
- SQLite3 (built-in)
- Funciona no Discloud e Replit

---

**Versão:** 1.0  
**Última atualização:** 24/12/2025  
**Autor:** William MC Flores
