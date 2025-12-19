#!/usr/bin/env python3
"""
Teste Simples de Conexão
Testa se o bot consegue conectar ao Discord
"""

import os
import sys
from pathlib import Path

# Define o diretório raiz do projeto
PROJETO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJETO_ROOT))

print("🔍 Testando conexão básica do bot...")
print("=" * 50)

# Verifica token
token = os.getenv("DISCORD_TOKEN")
if not token:
    print("❌ DISCORD_TOKEN não configurado!")
    print("\n📋 Configure a variável de ambiente:")
    print("   export DISCORD_TOKEN='seu_token_aqui'")
    print("\nOu no Replit: Secrets → DISCORD_TOKEN")
    sys.exit(1)

print(f"✅ Token encontrado (comprimento: {len(token)} caracteres)")

# Tenta importar discord.py
try:
    import discord
    print(f"✅ Discord.py versão: {discord.__version__}")
except ImportError:
    print("❌ Discord.py não instalado!")
    print("\n📋 Instale com:")
    print("   pip install discord.py")
    sys.exit(1)

# Teste de conexão
print("\n🔄 Tentando conectar ao Discord...")
print("   (Pressione Ctrl+C para cancelar)")
print("=" * 50)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("=" * 50)
    print(f"✅ CONECTADO COM SUCESSO!")
    print(f"   Bot: {client.user.name}")
    print(f"   ID: {client.user.id}")
    print(f"   Servidores: {len(client.guilds)}")
    print("=" * 50)
    print("\n✅ O bot está funcionando corretamente!")
    print("   Você pode parar o teste (Ctrl+C) e executar:")
    print("   python3 main.py")
    print("=" * 50)

@client.event
async def on_error(event, *args, **kwargs):
    print(f"❌ Erro: {event}")
    import traceback
    traceback.print_exc()

try:
    client.run(token)
except discord.LoginFailure:
    print("\n❌ ERRO: Token inválido!")
    print("   Verifique se o token está correto.")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
