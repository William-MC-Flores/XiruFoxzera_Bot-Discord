"""
Configurações centralizadas do bot Discord
Edite este arquivo para personalizar IDs de canais, cargos e outras configurações
"""

# ID do servidor principal
GUILD_ID = 1377748540318547989

# IDs de canais específicos
CANAIS = {
    "boas_vindas": 1377794646062792816,
    "saidas": 1394035471029502032,
    "logs": 1380610374641909920
}

# IDs de mensagens fixas
MENSAGEM_CADASTRO_ID = 1398764492208476242

# Cargos com permissões de moderação
ROLES_MODERACAO = ["Rei da cocada preta", "Admin", "Moderador"]

# Configurações do sistema de warns
WARNS_CONFIG = {
    "arquivo": "data/warns.json",
    "mute_automatico_em": 3,  # Número de warns para mute automático
    "cargo_mutado": "Mutado"
}

# Configurações do anti-spam
SPAM_CONFIG = {
    "max_mensagens": 5,  # Número máximo de mensagens
    "intervalo_segundos": 10,  # Intervalo de tempo em segundos
    "auto_warn": True  # Avisar automaticamente por spam
}

# Configurações de cooldowns (em segundos)
COOLDOWNS = {
    "say": 30,
    "sorteio": 60,
    "embed": 30,
    "votacao": 45
}

# Configurações do keep_alive (Replit)
KEEP_ALIVE_PORT = 8080

# Configurações de status do bot
STATUS_ROTACAO = [
    {"tipo": "game", "texto": "Mateando com a xiruzada🧉 /!ajuda/"},
    {"tipo": "watching", "texto": "o churras do Freddy🍖 /!ajuda/"},
    {"tipo": "listening", "texto": "uma milonga eletrônico🎶 /!ajuda/"},
    {"tipo": "game", "texto": "Caçando animatrônicos no galpão👻 /!ajuda/"},
    {"tipo": "watching", "texto": "o CTG ser invadido pelo Foxy🔪 /!ajuda/"},
    {"tipo": "game", "texto": "Jogando truco com os cabas🃏 /!ajuda/"}
]

# Intervalo de rotação de status (em segundos)
STATUS_INTERVALO = 30

# Mapeamento de emojis para cargos no sistema de cadastro
EMOJI_CARGO = {
    "👨‍💻": "👨‍💻 Programador",
    "🎮": "🎮 Gamer",
    "🎨": "🎨 Designer",
    "🎥": "🎥 Criador de Conteúdo",
    "🎸": "🎸 Músico",
    "🧪": "🧪 Curioso",
    "😎": "😎 Tô de boa",
    "🧱": "Minecraft",
    "🎯": "Roblox",
    "🤖": "R.E.P.O",
    "🃏": "Balatro",
    "📱": "📱 Mobile Gamer",
    "💻": "💻 PC Gamer",
    "🕹️": "🎮 Console Gamer",
    "📣": "📣 Anúncios",
    "🗓️": "🎮 Eventos",
    "🎁": "🎮 Jogos Promo",
    "🆕": "🆕 Novidades",
    "✅": "Concordo"
}
