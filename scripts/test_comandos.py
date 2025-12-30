#!/usr/bin/env python3
"""
Script para testar comandos do bot
Verifica se todos os comandos estão registrados e acessíveis
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import discord
from discord.ext import commands

# Cria um bot temporário para testes
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

async def testar_comandos():
    """Lista todos os comandos registrados"""
    # Carrega os cogs
    for filename in os.listdir('./Python'):
        if filename.endswith('.py') and filename not in ['logger.py', '__init__.py']:
            try:
                await bot.load_extension(f'Python.{filename[:-3]}')
            except Exception as e:
                print(f'❌ Erro ao carregar {filename}: {e}')
    
    print("🔍 Comandos Registrados no Bot:\n")
    
    # Agrupa comandos por cog
    comandos_por_cog = {}
    for comando in bot.commands:
        cog_name = comando.cog.qualified_name if comando.cog else "Sem Cog"
        if cog_name not in comandos_por_cog:
            comandos_por_cog[cog_name] = []
        comandos_por_cog[cog_name].append(comando)
    
    # Lista comandos por cog
    total = 0
    for cog_name in sorted(comandos_por_cog.keys()):
        comandos = comandos_por_cog[cog_name]
        print(f"📦 {cog_name} ({len(comandos)} comandos):")
        for cmd in sorted(comandos, key=lambda x: x.name):
            aliases = f" (aliases: {', '.join(cmd.aliases)})" if cmd.aliases else ""
            print(f"  • !{cmd.name}{aliases}")
            total += 1
        print()
    
    print(f"📊 Total: {total} comandos registrados\n")
    
    # Verifica comandos que podem estar quebrados
    print("🔍 Verificando Comandos Específicos:\n")
    
    comandos_testar = [
        'perfil', 'rank', 'ranking', 'saldo', 'pagar',
        'loja', 'comprar', 'inventario', 'conquistas',
        'addxp', 'resetperfil', 'addmoedas', 'removermoedas', 'setmoedas', 'darmoedas',
        'editarperfil', 'ajuda', 'help'
    ]
    
    for cmd_name in comandos_testar:
        cmd = bot.get_command(cmd_name)
        if cmd:
            # Verifica se tem callback
            if cmd.callback:
                status = "✅"
            else:
                status = "⚠️ Sem callback"
        else:
            status = "❌ NÃO ENCONTRADO"
        print(f"  {status} !{cmd_name}")
    
    print("\n" + "="*50)
    print("✅ Análise completa!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(testar_comandos())
