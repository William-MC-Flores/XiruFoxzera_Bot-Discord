"""
Sistema de Interações Automáticas
Responde automaticamente a certas mensagens no servidor
"""
import discord
from discord.ext import commands

class Interacoes(commands.Cog):
    """Interações automáticas do bot"""
    
    def __init__(self, bot):
        self.bot = bot
        # Dicionário de respostas automáticas
        self.respostas = {
            "opa": "🙋‍♂️ Aoba!!",
            "boa noite": "🌙 Boa noite! Durma bem!",
            "bom dia": "🌞 Bom dia! Tenha um ótimo dia!",
            "boa tarde": "☀️ Boa tarde!",
            "salve": "🤙 Salve fih!",
            "bão fih?": "😎 Bão fih!",
            "bão fih": "😎 Tamo junto!",
            "leva nabunda ou deixa nabunda?": "🤨 nabunda nada",
            "que time é teu?": "🤨 bateu na trave, entrou no teu",
            "nem te conto": "👀 Opa, fofoca?",
            "sigma": "🧏‍♂️ bye bye",
            "buenas?": "🙋‍♂️ buenas!",
            "buenas": "🙋‍♂️ buenas!",
            "tchau": "👋 Até logo!",
            "obrigado": "😊 De nada!",
            "valeu": "😊 Por nada!",
            "vlw": "😊 Tmj!",
        }
        
        # Dicionário de reações automáticas
        self.reacoes = {
            "suave": "🤙",
            "top": "👍",
            "legal": "😎",
            "massa": "🔥",
            "show": "⭐",
            "te odeio": "💔",
            "te amo": "❤️",
            "amo": "💕",
            "triste": "😢",
            "feliz": "😊",
        }
        
        print("  💬 Sistema de interações inicializado")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Responde automaticamente a certas mensagens"""
        # Ignora mensagens do próprio bot
        if message.author.bot:
            return

        # Converte mensagem para minúsculas para comparação
        conteudo = message.content.lower().strip()

        # Verifica respostas automáticas
        for trigger, resposta in self.respostas.items():
            if trigger in conteudo:
                await message.channel.send(resposta)
                return  # Para após encontrar uma resposta
        
        # Verifica reações automáticas
        for trigger, emoji in self.reacoes.items():
            if trigger in conteudo:
                try:
                    await message.add_reaction(emoji)
                except Exception as e:
                    print(f"❌ Erro ao adicionar reação: {e}")

    @commands.command(name="adicionar_resposta")
    @commands.has_permissions(administrator=True)
    async def adicionar_resposta(self, ctx, trigger: str, *, resposta: str):
        """Adiciona uma nova resposta automática (Admin)"""
        trigger = trigger.lower()
        self.respostas[trigger] = resposta
        await ctx.send(f"✅ Resposta automática adicionada!\n**Trigger:** `{trigger}`\n**Resposta:** {resposta}")

    @commands.command(name="remover_resposta")
    @commands.has_permissions(administrator=True)
    async def remover_resposta(self, ctx, trigger: str):
        """Remove uma resposta automática (Admin)"""
        trigger = trigger.lower()
        if trigger in self.respostas:
            del self.respostas[trigger]
            await ctx.send(f"✅ Resposta automática `{trigger}` removida!")
        else:
            await ctx.send(f"❌ Resposta `{trigger}` não encontrada.")

    @commands.command(name="listar_respostas")
    @commands.has_permissions(administrator=True)
    async def listar_respostas(self, ctx):
        """Lista todas as respostas automáticas (Admin)"""
        if not self.respostas:
            await ctx.send("📭 Nenhuma resposta automática configurada.")
            return
        
        embed = discord.Embed(
            title="💬 Respostas Automáticas",
            description=f"Total: {len(self.respostas)} resposta(s)",
            color=discord.Color.blue()
        )
        
        for i, (trigger, resposta) in enumerate(sorted(self.respostas.items()), 1):
            if i > 25:  # Limite de fields do Discord
                embed.set_footer(text=f"... e mais {len(self.respostas) - 25} respostas")
                break
            embed.add_field(name=f"🔹 {trigger}", value=resposta, inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Interacoes(bot))
