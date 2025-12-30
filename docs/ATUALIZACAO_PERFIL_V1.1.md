# 🎉 Atualização do Sistema de Perfil - v1.1

## ✨ Novas Funcionalidades Implementadas

### 1. **Sistema de Conquistas** 🏆

Usuários agora podem desbloquear conquistas ao atingir marcos específicos!

**Conquistas Disponíveis:**
- ✨ **Primeira Mensagem** - Enviou a primeira mensagem
- 💬 **Conversador** - Enviou 100 mensagens  
- 🗣️ **Tagarela** - Enviou 1000 mensagens
- 🌱 **Novato** - Alcançou o nível 1
- 🔰 **Iniciante** - Alcançou o nível 5
- ⭐ **Experiente** - Alcançou o nível 10
- 🏆 **Veterano** - Alcançou o nível 20
- 👑 **Lenda** - Alcançou o nível 50
- 💎 **Colecionador de XP** - Acumulou 10.000 XP
- 💠 **Mestre do XP** - Acumulou 100.000 XP

**Como Funciona:**
- Conquistas são desbloqueadas automaticamente
- Notificação no canal quando desbloquear
- Aparecem no perfil do usuário
- Armazenadas permanentemente no banco de dados

### 2. **Perfil Personalizado** 📝

Agora você pode personalizar seu perfil com:

**Bio Personalizada:**
- Máximo 200 caracteres
- Aparece no topo do perfil
- Comando: `!editarperfil bio <texto>`

**Status Personalizado:**
- Máximo 50 caracteres
- Exibido como subtítulo do perfil
- Comando: `!editarperfil status <texto>`

**Exemplo:**
```
!editarperfil bio Gamer nas horas vagas, programador o dia todo!
!editarperfil status Jogando Minecraft 🎮
```

### 3. **Data de Criação do Perfil** 📅

O perfil agora mostra:
- Data em que o usuário entrou no sistema
- Exibição em formato Discord (timestamp)
- Rastreamento de última atualização

### 4. **Perfil Expandido** 📊

O comando `!perfil` agora mostra:
- ⭐ Nível, XP e progresso (já existia)
- 💬 Status personalizado
- 📝 Bio personalizada  
- 🏆 Conquistas desbloqueadas (últimas 5)
- 📅 Data de criação do perfil
- Contador total de conquistas

## 🎮 Novos Comandos

### `!editarperfil`
Personaliza informações do seu perfil.

**Uso:**
```
!editarperfil                    # Mostra ajuda
!editarperfil bio <texto>        # Define bio (máx 200 chars)
!editarperfil status <texto>     # Define status (máx 50 chars)
!editarperfil limpar             # Remove bio e status
```

**Aliases:** `!editprofile`, `!setbio`

**Exemplos:**
```
!editarperfil bio Amo programar e jogar!
!editarperfil status Codando no VS Code 💻
!editarperfil limpar
```

### `!conquistas`
Mostra todas as conquistas desbloqueadas.

**Uso:**
```
!conquistas              # Suas conquistas
!conquistas @usuário     # Conquistas de outro usuário
```

**Aliases:** `!achievements`, `!badges`

**Informações Exibidas:**
- Total de conquistas desbloqueadas
- Lista completa com emoji, nome e descrição
- Data de desbloqueio de cada conquista

## 🗄️ Atualizações no Banco de Dados

### Novas Colunas na Tabela `usuarios`:
```sql
bio TEXT DEFAULT ''
status_personalizado TEXT DEFAULT ''
data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### Nova Tabela `conquistas`:
```sql
CREATE TABLE conquistas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    descricao TEXT NOT NULL,
    emoji TEXT NOT NULL,
    requisito_tipo TEXT NOT NULL,
    requisito_valor INTEGER NOT NULL
)
```

### Nova Tabela `usuarios_conquistas`:
```sql
CREATE TABLE usuarios_conquistas (
    id_discord INTEGER,
    conquista_id INTEGER,
    data_desbloqueio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_discord, conquista_id),
    FOREIGN KEY (id_discord) REFERENCES usuarios(id_discord),
    FOREIGN KEY (conquista_id) REFERENCES conquistas(id)
)
```

## 📸 Exemplo Visual do Novo Perfil

```
📊 Perfil de NomeUsuario
💬 Jogando Minecraft 🎮

📝 Bio
Gamer nas horas vagas, programador o dia todo!

⭐ Nível          💎 XP Total       🎯 Próximo Nível
   15               22,500              16

📈 Progresso para o próximo nível
████████░░ 75.5%
1,900 / 2,500 XP (faltam 600 XP)

🏆 Conquistas (7)
👑 ⭐ 💎 🔰 🌱 💬 ✨ +2

📅 Membro desde
20 de dezembro de 2025

ID: 123456789 • Use !editarperfil para personalizar
```

## 🔔 Notificações

### Level Up (Atualizado):
```
🎉 Level Up!
Parabéns @usuário! Você subiu para o nível 10!

📊 Progresso
Nível anterior: 9
Nível atual: 10
XP total: 10,000
```

### Conquista Desbloqueada (NOVO):
```
🏆 Conquista Desbloqueada!
@usuário desbloqueou uma conquista!

⭐ Experiente
Alcançou o nível 10
```

## 🎯 Compatibilidade

✅ **Retroativo:** Usuários existentes terão os novos campos adicionados automaticamente
✅ **Migração Automática:** O sistema adiciona as colunas ao iniciar
✅ **Sem Perda de Dados:** XP e níveis existentes são preservados

## 🚀 Como Usar

### Para Usuários:

1. **Personalize seu perfil:**
   ```
   !editarperfil bio Sua bio aqui
   !editarperfil status Seu status aqui
   ```

2. **Veja seu perfil:**
   ```
   !perfil
   ```

3. **Confira suas conquistas:**
   ```
   !conquistas
   ```

4. **Acompanhe o ranking:**
   ```
   !ranking
   ```

### Para Administradores:

Todos os comandos admin continuam funcionando normalmente:
```
!addxp @usuário 1000
!resetperfil @usuário
```

## 📝 Changelog

**Versão 1.1 - 30/12/2025**

**Adicionado:**
- ✅ Sistema de conquistas com 10 conquistas padrão
- ✅ Bio personalizada (200 caracteres)
- ✅ Status personalizado (50 caracteres)
- ✅ Data de criação do perfil
- ✅ Comando `!editarperfil`
- ✅ Comando `!conquistas`
- ✅ Notificações de conquistas desbloqueadas
- ✅ Exibição de conquistas no perfil
- ✅ Rastreamento de última atualização

**Melhorado:**
- ✅ Comando `!perfil` com mais informações
- ✅ Sistema de banco de dados expandido
- ✅ Documentação atualizada

**Preservado:**
- ✅ Todos os comandos existentes funcionando
- ✅ XP e níveis de usuários existentes
- ✅ Sistema de ranking
- ✅ Cooldown de XP

## 🔮 Próximas Expansões Sugeridas

1. **Conquistas Secretas:** Conquistas ocultas até serem desbloqueadas
2. **Emblemas Raros:** Conquistas por eventos especiais
3. **Perfil Visual:** Card de perfil com imagem usando PIL
4. **Títulos:** Sistema de títulos baseado em conquistas
5. **Favoritos:** Marcar conquistas favoritas para exibir
6. **Estatísticas:** Gráficos de progressão ao longo do tempo

## ⚠️ Notas Importantes

- **Limites de Texto:** Bio (200) e Status (50) caracteres
- **Automático:** Conquistas são verificadas a cada ganho de XP
- **Permanente:** Dados são salvos automaticamente no SQLite
- **Seguro:** Validações de entrada em todos os comandos

---

**Desenvolvido por:** William MC Flores  
**Data:** 30 de Dezembro de 2025  
**Versão:** 1.1  
**Status:** ✅ Testado e Pronto para Produção
