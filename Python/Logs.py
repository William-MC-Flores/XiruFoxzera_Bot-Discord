"""
Sistema de Logs e Auditoria
Registra automaticamente eventos importantes do servidor
"""
import discord
from discord.ext import commands
from Python.logger import send_log

class Logs(commands.Cog):
    """Monitora e registra eventos do servidor"""
    
    def __init__(self, bot):
        self.bot = bot
        # Lista de comandos que não devem ser logados (muito frequentes ou sensíveis)
        self.comandos_ignorados = {
            "senha", "login", "ajuda", "privacy", "terms", "ping", 
            "avatar", "userinfo", "serverinfo", "botinfo", "say", 
            "coinflip", "dado", "8ball", "help"
        }
        print("  📊 Sistema de logs inicializado")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Registra quando um membro entra"""
        await send_log(
            member.guild, 
            f"📥 **Entrada:** {member.mention} ({member.name}#{member.discriminator}) | ID: {member.id}"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Registra quando um membro sai"""
        await send_log(
            member.guild, 
            f"📤 **Saída:** {member.mention} ({member.name}#{member.discriminator}) | ID: {member.id}"
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Registra mensagens deletadas"""
        if message.author.bot:
            return
        
        # Limita o tamanho do conteúdo logado
        conteudo = message.content[:500]
        if len(message.content) > 500:
            conteudo += "... (mensagem truncada)"
        
        # Adiciona informações de anexos
        anexos_info = ""
        if message.attachments:
            anexos_info = f"\n📎 Anexos: {len(message.attachments)}"
        
        await send_log(
            message.guild,
            f"🗑️ **Mensagem deletada**\n"
            f"👤 Autor: {message.author.mention}\n"
            f"📍 Canal: {message.channel.mention}\n"
            f"💬 Conteúdo: ```{conteudo}```{anexos_info}"
        )

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Registra banimentos"""
        await send_log(guild, f"🔨 **Banimento:** {user.mention} ({user.name}) | ID: {user.id}")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Registra desbanimentos"""
        await send_log(guild, f"♻️ **Desbanimento:** {user.mention} ({user.name}) | ID: {user.id}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Registra edições de mensagens"""
        if before.author.bot:
            return
        if before.content == after.content:
            return
        
        # Limita o tamanho do conteúdo
        antes = before.content[:300]
        depois = after.content[:300]
        
        if len(before.content) > 300:
            antes += "..."
        if len(after.content) > 300:
            depois += "..."
        
        mensagem = (
            f"✏️ **Mensagem editada**\n"
            f"👤 Autor: {before.author.mention}\n"
            f"📍 Canal: {before.channel.mention}\n"
            f"**Antes:** ```{antes}```\n"
            f"**Depois:** ```{depois}```"
        )
        await send_log(before.guild, mensagem)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Registra comandos usados (exceto os ignorados)"""
        if ctx.author.bot:
            return

        nome_comando = ctx.command.name if ctx.command else ""
        if nome_comando.lower() in self.comandos_ignorados:
            return

        mensagem = (
            f"📘 **Comando usado**\n"
            f"👤 Usuário: {ctx.author.mention}\n"
            f"💬 Comando: `{ctx.message.content}`\n"
            f"📍 Canal: {ctx.channel.mention}"
        )
        await send_log(ctx.guild, mensagem)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Registra mudanças de cargos"""
        if before.roles == after.roles:
            return

        # Identifica cargos removidos e adicionados
        removed_roles = [role for role in before.roles if role not in after.roles]
        added_roles = [role for role in after.roles if role not in before.roles]

        if added_roles:
            nomes = ", ".join([f"`{r.name}`" for r in added_roles])
            await send_log(
                after.guild, 
                f"✅ **Cargos adicionados**\n👤 Usuário: {after.mention}\n🎭 Cargos: {nomes}"
            )

        if removed_roles:
            nomes = ", ".join([f"`{r.name}`" for r in removed_roles])
            await send_log(
                after.guild, 
                f"❌ **Cargos removidos**\n👤 Usuário: {after.mention}\n🎭 Cargos: {nomes}"
            )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Registra criação de canais"""
        await send_log(
            channel.guild,
            f"➕ **Canal criado:** {channel.mention} ({channel.name}) | Tipo: {channel.type}"
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Registra deleção de canais"""
        await send_log(
            channel.guild,
            f"➖ **Canal deletado:** `{channel.name}` | Tipo: {channel.type}"
        )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Registra criação de cargos"""
        await send_log(role.guild, f"➕ **Cargo criado:** `{role.name}`")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Registra deleção de cargos"""
        await send_log(role.guild, f"➖ **Cargo deletado:** `{role.name}`")

async def setup(bot):
    await bot.add_cog(Logs(bot))