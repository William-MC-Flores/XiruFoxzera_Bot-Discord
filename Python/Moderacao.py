"""
Sistema de Moderação
Gerencia warns, mutes, kicks, bans e anti-spam
"""
import discord
from discord.ext import commands
import json
import os
import asyncio
from Python.logger import send_log
from collections import defaultdict, deque
from datetime import datetime, timedelta
from config import WARNS_CONFIG, SPAM_CONFIG, ROLES_MODERACAO

# Sistema de anti-spam
spam_tracker = defaultdict(lambda: deque(maxlen=SPAM_CONFIG["max_mensagens"]))

def load_warns():
    """Carrega o arquivo de advertências"""
    warns_path = WARNS_CONFIG["arquivo"]
    if os.path.exists(warns_path):
        try:
            with open(warns_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Erro ao ler warns.json, criando novo arquivo")
            return {}
    return {}

def save_warns(warns):
    """Salva as advertências no arquivo"""
    warns_path = WARNS_CONFIG["arquivo"]
    try:
        with open(warns_path, 'w', encoding='utf-8') as f:
            json.dump(warns, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Erro ao salvar warns: {e}")

def tem_cargo_autorizado(membro):
    """Verifica se o membro tem permissão de moderação"""
    return any(role.name in ROLES_MODERACAO for role in membro.roles)

class Moderacao(commands.Cog):
    """Sistema completo de moderação do servidor"""
    
    def __init__(self, bot):
        self.bot = bot
        self.warns = load_warns()
        self.spam_tracker = spam_tracker
        print("  🛡️ Sistema de moderação inicializado")

    # ============================================
    # SISTEMA ANTI-SPAM
    # ============================================
    @commands.Cog.listener()
    async def on_message(self, message):
        """Detecta e pune spam automaticamente"""
        if message.author.bot:
            return
        
        # Ignora moderadores
        if tem_cargo_autorizado(message.author):
            return

        agora = datetime.utcnow()
        self.spam_tracker[message.author.id].append(agora)

        if len(self.spam_tracker[message.author.id]) >= SPAM_CONFIG["max_mensagens"]:
            intervalo = agora - self.spam_tracker[message.author.id][0]
            
            if intervalo < timedelta(seconds=SPAM_CONFIG["intervalo_segundos"]):
                if SPAM_CONFIG["auto_warn"]:
                    user_id = str(message.author.id)
                    self.warns.setdefault(user_id, []).append({
                        "motivo": "Spam detectado automaticamente",
                        "data": agora.isoformat(),
                        "moderador": "Sistema Anti-Spam"
                    })
                    save_warns(self.warns)
                    
                    total_warns = len(self.warns[user_id])
                    
                    embed = discord.Embed(
                        title="⚠️ Advertência por Spam",
                        description=f"{message.author.mention} foi advertido automaticamente por spam.",
                        color=discord.Color.orange()
                    )
                    embed.add_field(name="Total de Advertências", value=f"{total_warns}", inline=True)
                    embed.add_field(name="Motivo", value="Spam detectado", inline=True)
                    
                    await message.channel.send(embed=embed, delete_after=10)
                    
                    await send_log(
                        message.guild,
                        f"⚠️ **Anti-Spam:** {message.author.mention} advertido (Total: {total_warns})"
                    )
                    
                    # Mute automático em 3 warns
                    if total_warns >= WARNS_CONFIG["mute_automatico_em"]:
                        await self._aplicar_mute_automatico(message.author, message.guild)
                
                # Limpa o tracker para evitar múltiplos warns seguidos
                self.spam_tracker[message.author.id].clear()

    async def _aplicar_mute_automatico(self, member, guild):
        """Aplica mute automático ao atingir o limite de warns"""
        role = discord.utils.get(guild.roles, name=WARNS_CONFIG["cargo_mutado"])
        
        if not role:
            print(f"⚠️ Cargo '{WARNS_CONFIG['cargo_mutado']}' não encontrado")
            return
        
        if role in member.roles:
            return  # Já está mutado
        
        try:
            await member.add_roles(role, reason=f"Mute automático - {WARNS_CONFIG['mute_automatico_em']} warns")
            await send_log(
                guild,
                f"🔇 **Mute Automático:** {member.mention} foi mutado por atingir {WARNS_CONFIG['mute_automatico_em']} advertências"
            )
        except discord.Forbidden:
            print(f"❌ Sem permissão para mutar {member.name}")

    # ============================================
    # VERIFICAÇÃO DE AUTORIZAÇÃO
    # ============================================
    async def checar_autorizacao(self, ctx):
        """Verifica se o autor do comando tem permissão"""
        if not tem_cargo_autorizado(ctx.author):
            await ctx.send("❌ Você não tem permissão para usar este comando.")
            return False
        return True

    # ============================================
    # COMANDOS DE WARNS
    # ============================================
    @commands.command(name="warn")
    async def warn(self, ctx, member: discord.Member, *, reason: str = "Sem motivo especificado"):
        """Adverte um usuário"""
        if not await self.checar_autorizacao(ctx):
            return
        
        if member.id == ctx.author.id:
            await ctx.send("❌ Você não pode advertir a si mesmo!")
            return
        
        if member.bot:
            await ctx.send("❌ Não é possível advertir bots.")
            return
        
        if tem_cargo_autorizado(member):
            await ctx.send("❌ Você não pode advertir outros moderadores.")
            return

        user_id = str(member.id)
        self.warns.setdefault(user_id, []).append({
            "motivo": reason,
            "data": datetime.utcnow().isoformat(),
            "moderador": f"{ctx.author.name}#{ctx.author.discriminator}"
        })
        save_warns(self.warns)

        total_warns = len(self.warns[user_id])

        embed = discord.Embed(
            title="⚠️ Advertência Aplicada",
            description=f"{member.mention} foi advertido.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Motivo", value=reason, inline=False)
        embed.add_field(name="Total de Warns", value=f"{total_warns}", inline=True)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        
        try:
            await member.send(
                f"⚠️ Você recebeu uma advertência no servidor **{ctx.guild.name}**.\n"
                f"**Motivo:** {reason}\n"
                f"**Total de advertências:** {total_warns}"
            )
        except discord.Forbidden:
            await ctx.send("⚠️ Não foi possível enviar DM ao usuário.")
        
        await send_log(
            ctx.guild,
            f"⚠️ **Warn aplicado**\n"
            f"👤 Usuário: {member.mention}\n"
            f"👮 Moderador: {ctx.author.mention}\n"
            f"📝 Motivo: {reason}\n"
            f"📊 Total: {total_warns}"
        )

        # Mute automático se atingir o limite
        if total_warns >= WARNS_CONFIG["mute_automatico_em"]:
            await self._aplicar_mute_automatico(member, ctx.guild)

    @commands.command(name="verwarns", aliases=["warns", "listwarns"])
    async def verwarns(self, ctx, member: discord.Member = None):
        """Visualiza as advertências de um usuário"""
        if not await self.checar_autorizacao(ctx):
            return
        
        member = member or ctx.author
        user_id = str(member.id)
        user_warns = self.warns.get(user_id, [])

        if not user_warns:
            await ctx.send(f"✅ {member.mention} não possui advertências.")
            return

        embed = discord.Embed(
            title=f"📋 Advertências de {member.name}",
            description=f"Total: **{len(user_warns)}** advertência(s)",
            color=discord.Color.orange()
        )
        
        for i, warn_data in enumerate(user_warns, 1):
            # Suporta formato antigo (string) e novo (dict)
            if isinstance(warn_data, str):
                motivo = warn_data
                data = "Data não disponível"
                moderador = "Desconhecido"
            else:
                motivo = warn_data.get("motivo", "Sem motivo")
                data = warn_data.get("data", "Data não disponível")
                moderador = warn_data.get("moderador", "Desconhecido")
                
                # Formata a data
                try:
                    dt = datetime.fromisoformat(data)
                    data = dt.strftime("%d/%m/%Y %H:%M")
                except:
                    pass
            
            embed.add_field(
                name=f"#{i}",
                value=f"**Motivo:** {motivo}\n**Data:** {data}\n**Mod:** {moderador}",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name="clearwarns", aliases=["limparwarns"])
    async def clearwarns(self, ctx, member: discord.Member):
        """Remove todas as advertências de um usuário"""
        if not await self.checar_autorizacao(ctx):
            return

        user_id = str(member.id)
        total_removidos = len(self.warns.get(user_id, []))
        
        if user_id in self.warns:
            del self.warns[user_id]
            save_warns(self.warns)
            
            await ctx.send(f"🧹 Todas as {total_removidos} advertência(s) de {member.mention} foram removidas.")
            
            await send_log(
                ctx.guild,
                f"🧹 **Warns limpos**\n"
                f"👤 Usuário: {member.mention}\n"
                f"👮 Moderador: {ctx.author.mention}\n"
                f"📊 Removidos: {total_removidos}"
            )
        else:
            await ctx.send(f"✅ {member.mention} não tinha advertências para remover.")

    @commands.command(name="unwarn", aliases=["removewarn"])
    async def unwarn(self, ctx, member: discord.Member, index: int):
        """Remove uma advertência específica"""
        if not await self.checar_autorizacao(ctx):
            return

        user_id = str(member.id)
        
        if user_id not in self.warns or index < 1 or index > len(self.warns[user_id]):
            await ctx.send("❌ Índice inválido ou usuário sem advertências.")
            return

        removed = self.warns[user_id].pop(index - 1)
        
        if not self.warns[user_id]:
            del self.warns[user_id]

        save_warns(self.warns)
        
        # Suporta formato antigo e novo
        motivo = removed if isinstance(removed, str) else removed.get("motivo", "Sem motivo")
        
        await ctx.send(f"✅ Advertência #{index} removida de {member.mention}.")
        
        await send_log(
            ctx.guild,
            f"✂️ **Warn removido**\n"
            f"👤 Usuário: {member.mention}\n"
            f"👮 Moderador: {ctx.author.mention}\n"
            f"📝 Motivo removido: {motivo}"
        )

    @commands.command(name="warnslist", aliases=["todoswarns"])
    async def warnslist(self, ctx):
        """Lista todos os usuários com advertências"""
        if not await self.checar_autorizacao(ctx):
            return

        if not self.warns:
            await ctx.send("✅ Ninguém possui advertências no momento.")
            return

        embed = discord.Embed(
            title="📋 Lista de Advertências do Servidor",
            description=f"Total de usuários: {len(self.warns)}",
            color=discord.Color.orange()
        )
        
        for user_id, reasons in sorted(self.warns.items(), key=lambda x: len(x[1]), reverse=True):
            membro = ctx.guild.get_member(int(user_id))
            nome = membro.mention if membro else f"ID: `{user_id}` (não está no servidor)"
            embed.add_field(name=nome, value=f"🔸 {len(reasons)} warn(s)", inline=True)
        
        await ctx.send(embed=embed)

    # ============================================
    # COMANDOS DE MODERAÇÃO
    # ============================================
    @commands.command(name="setupmute")
    @commands.has_permissions(administrator=True)
    async def setupmute(self, ctx):
        """Cria ou configura o cargo de Mutado"""
        guild = ctx.guild
        mutado = discord.utils.get(guild.roles, name=WARNS_CONFIG["cargo_mutado"])

        if not mutado:
            mutado = await guild.create_role(
                name=WARNS_CONFIG["cargo_mutado"],
                reason="Cargo para sistema de mute",
                color=discord.Color.dark_gray()
            )
            await ctx.send(f"✅ Cargo `{WARNS_CONFIG['cargo_mutado']}` criado.")
        else:
            await ctx.send(f"🔁 Cargo `{WARNS_CONFIG['cargo_mutado']}` já existe. Atualizando permissões...")

        canais_atualizados = 0
        canais_erro = 0

        for canal in guild.channels:
            try:
                await canal.set_permissions(
                    mutado,
                    send_messages=False,
                    speak=False,
                    add_reactions=False,
                    send_messages_in_threads=False,
                    create_public_threads=False,
                    create_private_threads=False
                )
                canais_atualizados += 1
            except Exception as e:
                print(f"[ERRO] Canal {canal.name}: {e}")
                canais_erro += 1

        embed = discord.Embed(
            title="🔒 Setup de Mute Concluído",
            description=f"Permissões aplicadas ao cargo `{WARNS_CONFIG['cargo_mutado']}`",
            color=discord.Color.green()
        )
        embed.add_field(name="✅ Canais Configurados", value=canais_atualizados, inline=True)
        embed.add_field(name="❌ Erros", value=canais_erro, inline=True)
        
        await ctx.send(embed=embed)
        
        await send_log(
            guild,
            f"🔧 **Setup de Mute**\n"
            f"👮 Executado por: {ctx.author.mention}\n"
            f"✅ {canais_atualizados} canais configurados\n"
            f"❌ {canais_erro} erros"
        )

    @commands.command(name="mute")
    async def mute(self, ctx, member: discord.Member, tempo: int = 0, *, motivo: str = "Sem motivo especificado"):
        """Silencia um usuário (tempo em minutos, 0 = indefinido)"""
        if not await self.checar_autorizacao(ctx):
            return
        
        if member.id == ctx.author.id:
            await ctx.send("❌ Você não pode mutar a si mesmo!")
            return
        
        if tem_cargo_autorizado(member):
            await ctx.send("❌ Você não pode mutar outros moderadores.")
            return

        role = discord.utils.get(ctx.guild.roles, name=WARNS_CONFIG["cargo_mutado"])
        
        if not role:
            await ctx.send(f"❌ Cargo `{WARNS_CONFIG['cargo_mutado']}` não encontrado. Use `!setupmute` primeiro.")
            return

        if role in member.roles:
            await ctx.send(f"⚠️ {member.mention} já está mutado.")
            return

        try:
            await member.add_roles(role, reason=motivo)
            
            tempo_texto = f"{tempo} minuto(s)" if tempo > 0 else "Tempo indefinido"
            
            embed = discord.Embed(
                title="🔇 Usuário Mutado",
                description=f"{member.mention} foi silenciado.",
                color=discord.Color.red()
            )
            embed.add_field(name="Tempo", value=tempo_texto, inline=True)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            
            await ctx.send(embed=embed)
            
            await send_log(
                ctx.guild,
                f"🔇 **Mute aplicado**\n"
                f"👤 Usuário: {member.mention}\n"
                f"👮 Moderador: {ctx.author.mention}\n"
                f"⏱️ Tempo: {tempo_texto}\n"
                f"📝 Motivo: {motivo}"
            )

            if tempo > 0:
                await asyncio.sleep(tempo * 60)
                if role in member.roles:
                    await member.remove_roles(role)
                    await send_log(
                        ctx.guild,
                        f"🔊 **Desmute automático:** {member.mention} após {tempo} minuto(s)"
                    )
        
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para mutar esse usuário.")

    @commands.command(name="unmute", aliases=["desmute"])
    async def unmute(self, ctx, member: discord.Member):
        """Remove o silenciamento de um usuário"""
        if not await self.checar_autorizacao(ctx):
            return

        role = discord.utils.get(ctx.guild.roles, name=WARNS_CONFIG["cargo_mutado"])
        
        if not role or role not in member.roles:
            await ctx.send(f"✅ {member.mention} não está mutado.")
            return

        try:
            await member.remove_roles(role)
            await ctx.send(f"🔊 {member.mention} foi desmutado.")
            
            await send_log(
                ctx.guild,
                f"🔊 **Desmute aplicado**\n"
                f"👤 Usuário: {member.mention}\n"
                f"👮 Moderador: {ctx.author.mention}"
            )
        
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para desmutar esse usuário.")

    @commands.command(name="limpar", aliases=["clear", "purge"])
    async def limpar(self, ctx, quantidade: int):
        """Apaga mensagens do canal (máx: 100)"""
        if not await self.checar_autorizacao(ctx):
            return
        
        if quantidade < 1:
            await ctx.send("❌ Especifique um número maior que 0.")
            return
        
        if quantidade > 100:
            await ctx.send("❌ Não é possível apagar mais de 100 mensagens por vez.")
            return

        try:
            deletadas = await ctx.channel.purge(limit=quantidade + 1)
            
            msg = await ctx.send(f"🧹 {len(deletadas) - 1} mensagens foram apagadas.")
            await asyncio.sleep(3)
            await msg.delete()
            
            await send_log(
                ctx.guild,
                f"🧹 **Mensagens apagadas**\n"
                f"📍 Canal: {ctx.channel.mention}\n"
                f"👮 Moderador: {ctx.author.mention}\n"
                f"📊 Quantidade: {len(deletadas) - 1}"
            )
        
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para apagar mensagens.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Erro ao apagar mensagens: {e}")

    @commands.command(name="ban", aliases=["banir"])
    async def ban(self, ctx, member: discord.Member, *, reason: str = "Sem motivo especificado"):
        """Bane um usuário do servidor"""
        if not await self.checar_autorizacao(ctx):
            return
        
        if member.id == ctx.author.id:
            await ctx.send("❌ Você não pode banir a si mesmo!")
            return
        
        if tem_cargo_autorizado(member):
            await ctx.send("❌ Você não pode banir outros moderadores.")
            return

        try:
            await member.ban(reason=reason)
            
            embed = discord.Embed(
                title="🔨 Usuário Banido",
                description=f"{member.mention} foi banido do servidor.",
                color=discord.Color.dark_red()
            )
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            
            await send_log(
                ctx.guild,
                f"🔨 **Banimento aplicado**\n"
                f"👤 Usuário: {member.mention} (ID: {member.id})\n"
                f"👮 Moderador: {ctx.author.mention}\n"
                f"📝 Motivo: {reason}"
            )
        
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para banir esse usuário.")

    @commands.command(name="kick", aliases=["expulsar"])
    async def kick(self, ctx, member: discord.Member, *, reason: str = "Sem motivo especificado"):
        """Expulsa um usuário do servidor"""
        if not await self.checar_autorizacao(ctx):
            return
        
        if member.id == ctx.author.id:
            await ctx.send("❌ Você não pode expulsar a si mesmo!")
            return
        
        if tem_cargo_autorizado(member):
            await ctx.send("❌ Você não pode expulsar outros moderadores.")
            return

        try:
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title="👢 Usuário Expulso",
                description=f"{member.mention} foi expulso do servidor.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Motivo", value=reason, inline=False)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            
            await send_log(
                ctx.guild,
                f"👢 **Expulsão aplicada**\n"
                f"👤 Usuário: {member.mention} (ID: {member.id})\n"
                f"👮 Moderador: {ctx.author.mention}\n"
                f"📝 Motivo: {reason}"
            )
        
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para expulsar esse usuário.")

async def setup(bot):
    await bot.add_cog(Moderacao(bot))
