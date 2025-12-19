"""
Sistema de Logging
Utilitário para enviar logs para canais específicos do Discord
"""
import discord
from datetime import datetime
from config import CANAIS

async def send_log(guild: discord.Guild, mensagem: str, embed: discord.Embed = None):
    """
    Envia uma mensagem de log para o canal configurado
    
    Args:
        guild: Servidor onde enviar o log
        mensagem: Mensagem de texto a ser enviada
        embed: Embed opcional para logs mais elaborados
    """
    canal_id = CANAIS.get("logs")

    if canal_id is None:
        print(f"[LOG] Canal de logs não configurado")
        return

    canal = guild.get_channel(canal_id)

    if not canal:
        print(f"[LOG] Canal de logs ID {canal_id} não encontrado em {guild.name}")
        return
    
    try:
        if embed:
            await canal.send(content=mensagem, embed=embed)
        else:
            await canal.send(mensagem)
    except discord.Forbidden:
        print(f"[LOG] Sem permissão para enviar logs em {guild.name}")
    except Exception as e:
        print(f"[LOG] Erro ao enviar log: {e}")

async def send_log_embed(guild: discord.Guild, titulo: str, descricao: str, cor: discord.Color = discord.Color.blue()):
    """
    Envia um log formatado como embed
    
    Args:
        guild: Servidor onde enviar o log
        titulo: Título do embed
        descricao: Descrição do embed
        cor: Cor do embed
    """
    embed = discord.Embed(
        title=titulo,
        description=descricao,
        color=cor,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text=f"Servidor: {guild.name}")
    
    await send_log(guild, None, embed)