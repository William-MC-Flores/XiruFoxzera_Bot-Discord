"""
Sistema de Cadastro e Auto-Roles
Gerencia a atribuição automática de cargos através de reações
"""
import discord
from discord.ext import commands
from config import MENSAGEM_CADASTRO_ID, EMOJI_CARGO

class Cadastro(commands.Cog):
    """Sistema de auto-roles baseado em reações"""
    
    def __init__(self, bot):
        self.bot = bot
        print("  📝 Sistema de cadastro inicializado")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Adiciona cargo quando usuário reage à mensagem de cadastro"""
        
        # Verifica se é a mensagem de cadastro
        if payload.message_id != MENSAGEM_CADASTRO_ID:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        # Busca o membro
        try:
            member = await guild.fetch_member(payload.user_id)
        except discord.NotFound:
            print(f"⚠️ Membro {payload.user_id} não encontrado")
            return
        except discord.Forbidden:
            print(f"⚠️ Sem permissão para buscar membro {payload.user_id}")
            return

        # Ignora bots
        if member.bot:
            return

        # Verifica se o emoji está mapeado para um cargo
        emoji = str(payload.emoji)
        cargo_nome = EMOJI_CARGO.get(emoji)
        
        if not cargo_nome:
            return

        # Busca e adiciona o cargo
        cargo = discord.utils.get(guild.roles, name=cargo_nome)
        
        if not cargo:
            print(f"⚠️ Cargo '{cargo_nome}' não encontrado no servidor")
            return
        
        if cargo in member.roles:
            return  # Membro já tem o cargo
        
        try:
            await member.add_roles(cargo, reason="Auto-role via reação")
            print(f"[+] {member.name} recebeu o cargo: {cargo.name}")
        except discord.Forbidden:
            print(f"❌ Sem permissão para adicionar cargo {cargo.name} a {member.name}")
        except Exception as e:
            print(f"❌ Erro ao adicionar cargo: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Remove cargo quando usuário remove reação"""
        
        # Verifica se é a mensagem de cadastro
        if payload.message_id != MENSAGEM_CADASTRO_ID:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        # Busca o membro
        try:
            member = await guild.fetch_member(payload.user_id)
        except discord.NotFound:
            return
        except discord.Forbidden:
            return

        # Verifica se o emoji está mapeado para um cargo
        emoji = str(payload.emoji)
        cargo_nome = EMOJI_CARGO.get(emoji)
        
        if not cargo_nome:
            return

        # Busca e remove o cargo
        cargo = discord.utils.get(guild.roles, name=cargo_nome)
        
        if not cargo:
            return
        
        if cargo not in member.roles:
            return  # Membro não tem o cargo
        
        try:
            await member.remove_roles(cargo, reason="Remoção de auto-role via reação")
            print(f"[-] {member.name} perdeu o cargo: {cargo.name}")
        except discord.Forbidden:
            print(f"❌ Sem permissão para remover cargo {cargo.name} de {member.name}")
        except Exception as e:
            print(f"❌ Erro ao remover cargo: {e}")

    @commands.command(name="add_reacoes", aliases=["setup_cadastro"])
    @commands.has_permissions(administrator=True)
    async def add_reacoes(self, ctx):
        """Adiciona todas as reações à mensagem de cadastro"""
        
        try:
            # Busca a mensagem de cadastro
            mensagem = await ctx.channel.fetch_message(MENSAGEM_CADASTRO_ID)
            
            # Adiciona cada emoji
            sucesso = 0
            falhas = 0
            
            for emoji in EMOJI_CARGO.keys():
                try:
                    await mensagem.add_reaction(emoji)
                    sucesso += 1
                except discord.HTTPException as e:
                    print(f"❌ Erro ao adicionar emoji {emoji}: {e}")
                    falhas += 1
                except Exception as e:
                    print(f"❌ Erro inesperado com emoji {emoji}: {e}")
                    falhas += 1
            
            # Feedback para o administrador
            embed = discord.Embed(
                title="✅ Reações Adicionadas",
                description=f"**Sucesso:** {sucesso}\n**Falhas:** {falhas}",
                color=discord.Color.green() if falhas == 0 else discord.Color.orange()
            )
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            await ctx.send(f"❌ Mensagem com ID `{MENSAGEM_CADASTRO_ID}` não encontrada neste canal.")
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para adicionar reações nesta mensagem.")
        except Exception as e:
            await ctx.send(f"❌ Erro inesperado: {e}")

    @commands.command(name="criar_mensagem_cadastro")
    @commands.has_permissions(administrator=True)
    async def criar_mensagem_cadastro(self, ctx):
        """Cria uma nova mensagem de cadastro com instruções"""
        
        embed = discord.Embed(
            title="📝 Sistema de Cadastro",
            description="Reaja aos emojis abaixo para receber seus cargos!\n\n"
                       "**🎭 Perfil:**\n"
                       "👨‍💻 Programador | 🎮 Gamer | 🎨 Designer\n"
                       "🎥 Criador de Conteúdo | 🎸 Músico\n"
                       "🧪 Curioso | 😎 Tô de boa\n\n"
                       "**🎮 Jogos:**\n"
                       "🧱 Minecraft | 🎯 Roblox | 🤖 R.E.P.O | 🃏 Balatro\n\n"
                       "**🎯 Plataforma:**\n"
                       "📱 Mobile | 💻 PC | 🕹️ Console\n\n"
                       "**🔔 Notificações:**\n"
                       "📣 Anúncios | 🗓️ Eventos | 🎁 Jogos Promo | 🆕 Novidades\n\n"
                       "**✅ Concordo** - Aceito as regras do servidor",
            color=discord.Color.purple()
        )
        embed.set_footer(text="Clique nos emojis para adicionar/remover cargos")
        
        msg = await ctx.send(embed=embed)
        await ctx.send(f"✅ Mensagem criada! ID: `{msg.id}`\n"
                      f"Configure este ID em `config.py` como `MENSAGEM_CADASTRO_ID`")

async def setup(bot):
    await bot.add_cog(Cadastro(bot))