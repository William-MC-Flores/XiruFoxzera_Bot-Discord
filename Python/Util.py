"""
Comandos Utilitários
Comandos diversos para diversão e utilidade no servidor
"""
import discord
from discord.ext import commands
from discord.ui import View, Button
from discord.utils import utcnow
import platform
import asyncio
import random
from datetime import datetime
from Python.logger import send_log
from config import COOLDOWNS

class VotacaoView(View):
    """View interativa para sistema de votação"""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minutos de timeout
        self.votos_sim = 0
        self.votos_nao = 0
        self.votantes = set()

    @discord.ui.button(label="👍 Sim", style=discord.ButtonStyle.success, custom_id="sim")
    async def botao_sim(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id in self.votantes:
            await interaction.response.send_message("❌ Você já votou!", ephemeral=True)
            return
        
        self.votantes.add(interaction.user.id)
        self.votos_sim += 1
        await interaction.response.edit_message(embed=self._criar_embed())

    @discord.ui.button(label="👎 Não", style=discord.ButtonStyle.danger, custom_id="nao")
    async def botao_nao(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id in self.votantes:
            await interaction.response.send_message("❌ Você já votou!", ephemeral=True)
            return
        
        self.votantes.add(interaction.user.id)
        self.votos_nao += 1
        await interaction.response.edit_message(embed=self._criar_embed())

    def _criar_embed(self):
        total = self.votos_sim + self.votos_nao
        embed = discord.Embed(
            title="📊 Votação em Andamento",
            description=f"**Total de votos:** {total}",
            color=discord.Color.blue()
        )
        embed.add_field(name="👍 Sim", value=f"**{self.votos_sim}** votos", inline=True)
        embed.add_field(name="👎 Não", value=f"**{self.votos_nao}** votos", inline=True)
        return embed

class Utilitarios(commands.Cog):
    """Comandos utilitários e de diversão"""
    
    def __init__(self, bot):
        self.bot = bot
        print("  ⚙️ Comandos utilitários inicializados")

    # ============================================
    # COMANDOS DE INFORMAÇÃO
    # ============================================
    @commands.command(name="ping")
    async def ping(self, ctx):
        """Verifica a latência do bot"""
        latencia = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latência: **{latencia}ms**",
            color=discord.Color.green() if latencia < 200 else discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command(name="avatar", aliases=["av"])
    async def avatar(self, ctx, membro: discord.Member = None):
        """Mostra o avatar de um usuário"""
        membro = membro or ctx.author
        avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
        
        embed = discord.Embed(
            title=f"🖼️ Avatar de {membro.name}",
            color=discord.Color.blurple()
        )
        embed.set_image(url=avatar_url)
        embed.add_field(name="Download", value=f"[Clique aqui]({avatar_url})")
        
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases=["ui", "user"])
    async def userinfo(self, ctx, membro: discord.Member = None):
        """Mostra informações detalhadas sobre um usuário"""
        membro = membro or ctx.author
        
        # Calcula tempo no servidor
        tempo_servidor = None
        if membro.joined_at:
            delta = utcnow() - membro.joined_at
            dias = delta.days
            tempo_servidor = f"{dias} dia(s)"
        
        # Formata cargos
        cargos = ", ".join([role.mention for role in membro.roles[1:][:10]]) or "Nenhum"
        if len(membro.roles) > 11:
            cargos += f" ... (+{len(membro.roles) - 11} cargos)"
        
        # Cria embed
        embed = discord.Embed(
            title=f"👤 Informações de {membro.name}",
            color=membro.color if membro.color != discord.Color.default() else discord.Color.green()
        )
        
        avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        embed.add_field(name="🆔 ID", value=f"`{membro.id}`", inline=True)
        embed.add_field(name="💬 Nome", value=membro.name, inline=True)
        embed.add_field(name="🏷️ Apelido", value=membro.display_name, inline=True)
        
        embed.add_field(
            name="📅 Conta criada",
            value=membro.created_at.strftime('%d/%m/%Y às %H:%M'),
            inline=False
        )
        
        if membro.joined_at:
            embed.add_field(
                name="🚪 Entrou no servidor",
                value=f"{membro.joined_at.strftime('%d/%m/%Y às %H:%M')}\n({tempo_servidor})",
                inline=False
            )
        
        embed.add_field(name=f"📌 Cargos ({len(membro.roles)-1})", value=cargos, inline=False)
        
        # Status
        status_emoji = {
            discord.Status.online: "🟢 Online",
            discord.Status.idle: "🟡 Ausente",
            discord.Status.dnd: "🔴 Não perturbe",
            discord.Status.offline: "⚫ Offline"
        }
        embed.add_field(name="📊 Status", value=status_emoji.get(membro.status, "Desconhecido"), inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["si", "server"])
    async def serverinfo(self, ctx):
        """Mostra informações sobre o servidor"""
        guild = ctx.guild
        
        # Estatísticas de membros
        total_membros = guild.member_count
        bots = sum(1 for m in guild.members if m.bot)
        humanos = total_membros - bots
        
        # Estatísticas de canais
        canais_texto = len(guild.text_channels)
        canais_voz = len(guild.voice_channels)
        categorias = len(guild.categories)
        
        # Nível de boost
        boost_info = f"Nível {guild.premium_tier} ({guild.premium_subscription_count} boosts)"
        
        embed = discord.Embed(
            title=f"🏠 {guild.name}",
            description=guild.description or "Sem descrição",
            color=discord.Color.orange()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="🆔 ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="👑 Dono", value=guild.owner.mention, inline=True)
        embed.add_field(name="📅 Criado em", value=guild.created_at.strftime('%d/%m/%Y'), inline=True)
        
        embed.add_field(
            name=f"👥 Membros ({total_membros})",
            value=f"👤 Humanos: {humanos}\n🤖 Bots: {bots}",
            inline=True
        )
        
        embed.add_field(
            name=f"📁 Canais ({len(guild.channels)})",
            value=f"💬 Texto: {canais_texto}\n🔊 Voz: {canais_voz}\n📂 Categorias: {categorias}",
            inline=True
        )
        
        embed.add_field(name=f"📌 Cargos", value=len(guild.roles), inline=True)
        embed.add_field(name="🚀 Boost", value=boost_info, inline=True)
        embed.add_field(name="😊 Emojis", value=len(guild.emojis), inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name="botinfo", aliases=["bi"])
    async def botinfo(self, ctx):
        """Mostra informações sobre o bot"""
        latencia = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🤖 Informações do Bot",
            description="Bot de moderação e utilidades para Discord",
            color=discord.Color.purple()
        )
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        embed.add_field(name="📱 Latência", value=f"{latencia}ms", inline=True)
        embed.add_field(name="📦 Plataforma", value=platform.system(), inline=True)
        embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
        
        embed.add_field(name="💪 Criador", value="Will Flores", inline=True)
        embed.add_field(name="🏠 Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 Usuários", value=len(self.bot.users), inline=True)
        
        embed.add_field(name="📜 Comandos", value=len(self.bot.commands), inline=True)
        embed.add_field(name="📦 Módulos (Cogs)", value=len(self.bot.cogs), inline=True)
        
        await ctx.send(embed=embed)

    # ============================================
    # COMANDOS DE UTILIDADE
    # ============================================
    @commands.command(name="say", aliases=["falar"])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, COOLDOWNS["say"], commands.BucketType.user)
    async def say(self, ctx, *, mensagem: str):
        """Faz o bot repetir uma mensagem"""
        # Filtro básico de segurança
        palavras_proibidas = ["@everyone", "@here"]
        for palavra in palavras_proibidas:
            if palavra in mensagem.lower():
                await ctx.send("❌ Não é permitido mencionar everyone/here!")
                return
        
        await ctx.message.delete()
        await ctx.send(mensagem)
        
        await send_log(
            ctx.guild,
            f"📣 **Say usado**\n👤 Por: {ctx.author.mention}\n💬 Mensagem: `{mensagem[:100]}`"
        )

    @commands.command(name="embed", aliases=["emb"])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, COOLDOWNS["embed"], commands.BucketType.user)
    async def embed(self, ctx, titulo: str, *, descricao: str):
        """Cria uma mensagem embed personalizada"""
        embed = discord.Embed(
            title=titulo,
            description=descricao,
            color=discord.Color.random(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Criado por {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)
        await send_log(ctx.guild, f"🧱 **Embed criado** por {ctx.author.mention}: {titulo}")

    # ============================================
    # COMANDOS INTERATIVOS
    # ============================================
    @commands.command(name="votacao", aliases=["poll", "vote"])
    @commands.cooldown(1, COOLDOWNS["votacao"], commands.BucketType.channel)
    async def votacao(self, ctx, *, pergunta: str = "Votação"):
        """Inicia uma votação interativa com botões"""
        view = VotacaoView()
        
        embed = discord.Embed(
            title="📊 Votação",
            description=f"**Pergunta:** {pergunta}\n\nClique nos botões abaixo para votar!",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Votação iniciada por {ctx.author.name}")
        
        await ctx.send(embed=embed, view=view)
        await send_log(ctx.guild, f"📊 **Votação iniciada** por {ctx.author.mention}: {pergunta}")

    @commands.command(name="sorteio", aliases=["giveaway"])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, COOLDOWNS["sorteio"], commands.BucketType.channel)
    async def sorteio(self, ctx, tempo: int = 30, *, premio: str = "o sorteio"):
        """Inicia um sorteio (tempo em segundos)"""
        if tempo < 10:
            await ctx.send("❌ O tempo mínimo é 10 segundos.")
            return
        
        if tempo > 3600:
            await ctx.send("❌ O tempo máximo é 3600 segundos (1 hora).")
            return
        
        embed = discord.Embed(
            title="🎉 Sorteio Iniciado!",
            description=(
                f"**Prêmio:** {premio}\n\n"
                f"Reaja com 🎉 para participar!\n"
                f"⏱️ Tempo: **{tempo} segundos**"
            ),
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Sorteio por {ctx.author.name}")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")
        
        await asyncio.sleep(tempo)
        
        try:
            msg = await ctx.channel.fetch_message(msg.id)
            users = [u async for u in msg.reactions[0].users() if not u.bot]
            
            if not users:
                resultado_embed = discord.Embed(
                    title="❌ Sorteio Cancelado",
                    description="Ninguém participou do sorteio.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=resultado_embed)
            else:
                vencedor = random.choice(users)
                
                resultado_embed = discord.Embed(
                    title="🎉 Sorteio Finalizado!",
                    description=(
                        f"**Vencedor:** {vencedor.mention}\n"
                        f"**Prêmio:** {premio}\n\n"
                        f"Parabéns! 🎊"
                    ),
                    color=discord.Color.gold()
                )
                resultado_embed.set_footer(text=f"{len(users)} participante(s)")
                
                await ctx.send(embed=resultado_embed)
                await send_log(
                    ctx.guild,
                    f"🎁 **Sorteio finalizado**\n"
                    f"🎟️ Organizador: {ctx.author.mention}\n"
                    f"🏆 Vencedor: {vencedor.mention}\n"
                    f"🎁 Prêmio: {premio}"
                )
        except discord.NotFound:
            await ctx.send("❌ A mensagem do sorteio foi deletada.")

    # ============================================
    # COMANDOS DE DIVERSÃO
    # ============================================
    @commands.command(name="coinflip", aliases=["moeda", "cf"])
    async def coinflip(self, ctx):
        """Joga uma moeda (cara ou coroa)"""
        resultado = random.choice(["Cara", "Coroa"])
        emoji = "🪙" if resultado == "Cara" else "🎴"
        
        embed = discord.Embed(
            title="🪙 Cara ou Coroa",
            description=f"Resultado: **{emoji} {resultado}**",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(name="dado", aliases=["roll", "dice"])
    async def dado(self, ctx, lados: int = 6):
        """Rola um dado (padrão: 6 lados)"""
        if lados < 2:
            await ctx.send("❌ O dado precisa ter pelo menos 2 lados.")
            return
        
        if lados > 100:
            await ctx.send("❌ Máximo de 100 lados.")
            return
        
        numero = random.randint(1, lados)
        
        embed = discord.Embed(
            title=f"🎲 Dado de {lados} lados",
            description=f"Resultado: **{numero}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name="8ball", aliases=["bola8"])
    async def oito_ball(self, ctx, *, pergunta: str):
        """Faz uma pergunta à bola mágica"""
        respostas = [
            "✅ Sim",
            "❌ Não",
            "🤷 Talvez",
            "👍 Provavelmente",
            "💯 Com certeza",
            "🚫 Nunca",
            "🤔 Acho que sim",
            "⏰ Pergunte depois",
            "😕 Melhor não responder",
            "🎯 Sem dúvida",
            "❓ Não sei dizer",
            "🌟 É certo"
        ]
        
        resposta = random.choice(respostas)
        
        embed = discord.Embed(
            title="🎱 Bola Mágica",
            color=discord.Color.purple()
        )
        embed.add_field(name="Pergunta", value=pergunta, inline=False)
        embed.add_field(name="Resposta", value=resposta, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="escolher", aliases=["choose", "escolha"])
    async def escolher(self, ctx, *opcoes: str):
        """Escolhe aleatoriamente entre as opções fornecidas"""
        if len(opcoes) < 2:
            await ctx.send("❌ Forneça pelo menos 2 opções separadas por espaços.")
            return
        
        escolha = random.choice(opcoes)
        
        embed = discord.Embed(
            title="🎲 Escolha Aleatória",
            description=f"Eu escolho: **{escolha}**",
            color=discord.Color.random()
        )
        embed.set_footer(text=f"{len(opcoes)} opções disponíveis")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilitarios(bot))
