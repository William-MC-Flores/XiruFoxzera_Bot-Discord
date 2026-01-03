"""
Bot Discord Principal
Bot de moderação e utilidades para servidor Discord
"""
import os
import sys
import discord
from discord.ext import commands
from keep_alive import keep_alive
import asyncio
import traceback
from dotenv import load_dotenv
from config import GUILD_ID, STATUS_ROTACAO, STATUS_INTERVALO

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ============================================
# SISTEMA DE ROTAÇÃO DE STATUS
# ============================================
async def rotacionar_status():
    """Rotaciona o status do bot entre diferentes atividades"""
    atividades = []
    
    for status in STATUS_ROTACAO:
        if status["tipo"] == "game":
            atividades.append(discord.Game(status["texto"]))
        elif status["tipo"] == "watching":
            atividades.append(discord.Activity(type=discord.ActivityType.watching, name=status["texto"]))
        elif status["tipo"] == "listening":
            atividades.append(discord.Activity(type=discord.ActivityType.listening, name=status["texto"]))
    
    while True:
        for atividade in atividades:
            try:
                await bot.change_presence(activity=atividade)
                await asyncio.sleep(STATUS_INTERVALO)
            except Exception as e:
                print(f"❌ Erro ao atualizar status: {e}")
                await asyncio.sleep(STATUS_INTERVALO)

# ============================================
# TRATAMENTO DE ERROS GLOBAL
# ============================================
@bot.event
async def on_command_error(ctx, error):
    """Trata erros de comandos globalmente"""
    
    # Ignora erros de comandos não encontrados
    if isinstance(error, commands.CommandNotFound):
        return
    
    # Tratamento de erros específicos
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
    
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argumento faltando: `{error.param.name}`. Use `!ajuda` para mais informações.")
    
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argumento inválido. Verifique o comando e tente novamente.")
    
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Membro não encontrado. Verifique se mencionou corretamente.")
    
    elif isinstance(error, commands.CommandOnCooldown):
        tempo = round(error.retry_after)
        await ctx.send(f"⏱️ Comando em cooldown. Tente novamente em {tempo} segundos.")
    
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ O bot não tem permissões suficientes para executar este comando.")
    
    elif isinstance(error, discord.Forbidden):
        await ctx.send("❌ Sem permissão para executar esta ação.")
    
    else:
        # Log de erro detalhado para erros não tratados
        print(f"❌ Erro não tratado no comando {ctx.command}:")
        print(f"   Usuário: {ctx.author} (ID: {ctx.author.id})")
        print(f"   Canal: {ctx.channel} (ID: {ctx.channel.id})")
        print(f"   Mensagem: {ctx.message.content}")
        traceback.print_exception(type(error), error, error.__traceback__)
        
        await ctx.send("❌ Ocorreu um erro inesperado. O erro foi registrado para análise.")

# ============================================
# EVENTOS DO BOT
# ============================================
@bot.event
async def on_ready():
    """Evento disparado quando o bot está pronto"""
    print("=" * 50)
    print("🔁 BOT INICIALIZADO")
    print("=" * 50)
    
    try:
        # Sincroniza comandos slash com o servidor
        guild = discord.Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild)
        print(f'✅ Bot: {bot.user.name} (ID: {bot.user.id})')
        print(f'🔧 Comandos sincronizados com servidor ID: {guild.id}')
        print(f'📦 Total de comandos prefix: {len(bot.commands)}')
        print(f'📦 Total de comandos slash: {len(bot.tree.get_commands())}')
        print(f'🏠 Conectado a {len(bot.guilds)} servidor(es)')
        print("=" * 50)
        
        # Inicia a rotação de status
        bot.loop.create_task(rotacionar_status())
        
    except Exception as e:
        print(f"❌ Erro durante inicialização: {e}")
        traceback.print_exc()

@bot.event
async def on_disconnect():
    """Evento disparado quando o bot desconecta"""
    print("⚠️ Bot desconectado!")

@bot.event
async def on_resumed():
    """Evento disparado quando o bot reconecta"""
    print("✅ Conexão restabelecida!")

# ============================================
# CARREGAMENTO DE COGS
# ============================================
async def load_cogs():
    """Carrega todos os cogs (módulos) automaticamente"""
    print("\n📂 Carregando módulos (cogs)...")
    
    cogs_carregados = 0
    cogs_com_erro = 0
    
    for filename in os.listdir('./Python'):
        if filename.endswith('.py') and filename not in ['logger.py', '__init__.py']:
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'  ✔️ {filename[:-3]}')
                cogs_carregados += 1
            except Exception as e:
                print(f'  ❌ {filename[:-3]}: {e}')
                cogs_com_erro += 1
    
    print(f"\n📊 Resumo: {cogs_carregados} carregados, {cogs_com_erro} com erro\n")

@bot.event
async def setup_hook():
    """Hook executado antes do bot conectar"""
    await load_cogs()

# ============================================
# COMANDOS ADMINISTRATIVOS
# ============================================
@bot.command(name="reload", hidden=True)
@commands.is_owner()
async def reload_cog(ctx, cog_name: str):
    """Recarrega um cog específico (apenas owner)"""
    try:
        await bot.reload_extension(f'cogs.{cog_name}')
        await ctx.send(f"✅ Módulo `{cog_name}` recarregado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao recarregar `{cog_name}`: {e}")

@bot.command(name="shutdown", hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    """Desliga o bot (apenas owner)"""
    await ctx.send("👋 Desligando o bot...")
    await bot.close()

# ============================================
# INICIALIZAÇÃO
# ============================================
if __name__ == "__main__":
    # Verifica se o token está configurado
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ ERRO: Token do Discord não encontrado!")
        print("   Configure a variável de ambiente DISCORD_TOKEN")
        sys.exit(1)
    
    # Inicia o keep-alive (para Replit)
    try:
        keep_alive()
    except Exception as e:
        print(f"⚠️ Aviso: Keep-alive não iniciado: {e}")
    
    # Inicia o bot
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("❌ ERRO: Token inválido!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        traceback.print_exc()
        sys.exit(1)