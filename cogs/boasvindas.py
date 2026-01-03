"""
Sistema de Boas-Vindas e Despedidas
Gerencia mensagens automáticas de entrada, saída e banimento
"""
import discord
from discord.ext import commands
from config import CANAIS

class BoasVindas(commands.Cog):
    """Sistema de boas-vindas e notificações de membros"""
    
    def __init__(self, bot):
        self.bot = bot
        print("  👋 Sistema de boas-vindas inicializado")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Envia mensagem de boas-vindas quando um membro entra"""
        
        canal = member.guild.get_channel(CANAIS["boas_vindas"])
        
        if not canal:
            print(f"⚠️ Canal de boas-vindas não encontrado (ID: {CANAIS['boas_vindas']})")
            return
        
        try:
            # Cria embed de boas-vindas
            embed = discord.Embed(
                title=f"👋 Seja bem-vindo(a), {member.name}!",
                description=(
                    f"Olá {member.mention}! 🥳\n\n"
                    "Seja muito bem-vindo(a) à nossa comunidade!\n"
                    "• Leia as **regras** do servidor\n"
                    "• Faça seu **cadastro** para pegar seus cargos\n"
                    "• Divirta-se e respeite os outros membros!\n\n"
                    f"Agora somos **{member.guild.member_count}** membros! 🎉"
                ),
                color=discord.Color.purple()
            )
            
            # Define avatar do membro
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text="Bot do servidor à disposição! 🤖")
            embed.timestamp = discord.utils.utcnow()
            
            await canal.send(embed=embed)
            
        except discord.Forbidden:
            print(f"❌ Sem permissão para enviar mensagem no canal de boas-vindas")
        except Exception as e:
            print(f"❌ Erro ao enviar boas-vindas: {e}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Notifica quando um membro é banido"""
        
        canal = guild.get_channel(CANAIS["saidas"])
        
        if not canal:
            print(f"⚠️ Canal de saídas não encontrado (ID: {CANAIS['saidas']})")
            return
        
        try:
            # Tenta buscar informações do audit log
            motivo = "Não especificado"
            moderador = "Desconhecido"
            
            try:
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                    if entry.target.id == user.id:
                        motivo = entry.reason or "Não especificado"
                        moderador = entry.user.mention
                        break
            except discord.Forbidden:
                pass  # Sem permissão para ver audit logs
            
            embed = discord.Embed(
                title=f"🔨 {user.name} foi banido!",
                description=(
                    f"**Usuário:** {user.mention} (ID: {user.id})\n"
                    f"**Moderador:** {moderador}\n"
                    f"**Motivo:** {motivo}\n\n"
                    "O usuário foi permanentemente banido do servidor."
                ),
                color=discord.Color.red()
            )
            
            avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text="Sistema de Moderação")
            embed.timestamp = discord.utils.utcnow()
            
            await canal.send(embed=embed)
            
        except discord.Forbidden:
            print(f"❌ Sem permissão para enviar mensagem no canal de saídas")
        except Exception as e:
            print(f"❌ Erro ao notificar banimento: {e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Notifica quando um membro sai ou é expulso"""
        
        canal = member.guild.get_channel(CANAIS["saidas"])
        
        if not canal:
            print(f"⚠️ Canal de saídas não encontrado (ID: {CANAIS['saidas']})")
            return
        
        try:
            # Verifica se foi kick através do audit log
            foi_kick = False
            motivo = None
            moderador = None
            
            try:
                async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
                    if entry.target.id == member.id:
                        foi_kick = True
                        motivo = entry.reason or "Não especificado"
                        moderador = entry.user.mention
                        break
            except discord.Forbidden:
                pass  # Sem permissão para ver audit logs
            
            if foi_kick:
                # Foi expulso
                embed = discord.Embed(
                    title=f"👢 {member.name} foi expulso",
                    description=(
                        f"**Usuário:** {member.mention} (ID: {member.id})\n"
                        f"**Moderador:** {moderador}\n"
                        f"**Motivo:** {motivo}\n\n"
                        "O usuário foi expulso do servidor."
                    ),
                    color=discord.Color.orange()
                )
            else:
                # Saiu voluntariamente
                embed = discord.Embed(
                    title=f"👋 {member.name} saiu do servidor",
                    description=(
                        f"**Usuário:** {member.mention} (ID: {member.id})\n\n"
                        f"O usuário saiu voluntariamente.\n"
                        f"Agora temos **{member.guild.member_count}** membros."
                    ),
                    color=discord.Color.light_gray()
                )
            
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text="Sentiremos sua falta! 😢" if not foi_kick else "Sistema de Moderação")
            embed.timestamp = discord.utils.utcnow()
            
            await canal.send(embed=embed)
            
        except discord.Forbidden:
            print(f"❌ Sem permissão para enviar mensagem no canal de saídas")
        except Exception as e:
            print(f"❌ Erro ao notificar saída: {e}")

    @commands.command(name="bemvindo", aliases=["welcome"])
    @commands.has_permissions(administrator=True)
    async def bemvindo_manual(self, ctx, member: discord.Member):
        """Envia mensagem de boas-vindas manualmente para um membro"""
        
        canal = ctx.guild.get_channel(CANAIS["boas_vindas"])
        
        if not canal:
            await ctx.send(f"❌ Canal de boas-vindas não configurado.")
            return
        
        embed = discord.Embed(
            title=f"👋 Bem-vindo(a), {member.name}!",
            description=f"Olá {member.mention}! Seja muito bem-vindo(a) à nossa comunidade! 🥳",
            color=discord.Color.purple()
        )
        
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        await canal.send(embed=embed)
        await ctx.send(f"✅ Mensagem de boas-vindas enviada para {member.mention}!")

async def setup(bot):
    await bot.add_cog(BoasVindas(bot))
