"""
Comandos de Informação e Ajuda
Sistema de ajuda e informações sobre o bot
"""
import discord
from discord.ext import commands

class Ajuda(commands.Cog):
    """Comandos de ajuda e informação"""
    
    def __init__(self, bot):
        self.bot = bot
        print("  ℹ️ Sistema de ajuda inicializado")

    @commands.command(name="ajuda", aliases=["help", "comandos"])
    async def ajuda(self, ctx, categoria: str = None):
        """Mostra todos os comandos disponíveis no bot"""
        
        if categoria:
            # Ajuda específica por categoria
            return await self._ajuda_categoria(ctx, categoria.lower())
        
        # Ajuda geral
        embed = discord.Embed(
            title="📚 Central de Ajuda",
            description=(
                "Bem-vindo à central de ajuda! Aqui estão todas as categorias de comandos disponíveis.\n\n"
                "💡 **Dica:** Use `!ajuda <categoria>` para ver comandos detalhados de uma categoria.\n"
                "Exemplo: `!ajuda moderacao`"
            ),
            color=discord.Color.blue()
        )

        # Categorias
        embed.add_field(
            name="🛡️ Moderação",
            value=(
                "Comandos para moderação do servidor.\n"
                "`!ajuda moderacao` para detalhes"
            ),
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ Informação",
            value=(
                "Comandos de informações e ajuda.\n"
                "`!ajuda info` para detalhes"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⭐ Níveis e XP",
            value=(
                "Sistema de experiência e ranking.\n"
                "`!ajuda niveis` para detalhes"
            ),
            inline=False
        )
        
        embed.add_field(
            name="💰 Economia e Loja",
            value=(
                "Sistema de moedas, loja e inventário.\n"
                "`!ajuda economia` para detalhes"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Utilitários",
            value=(
                "Comandos úteis e de diversão.\n"
                "`!ajuda utilitarios` para detalhes"
            ),
            inline=False
        )
        

        
        embed.set_footer(text=f"Bot criado por William MC Flores")
        
        await ctx.send(embed=embed)

    async def _ajuda_categoria(self, ctx, categoria):
        """Mostra ajuda detalhada de uma categoria"""
        
        if categoria in ["moderacao", "mod", "moderação"]:
            embed = discord.Embed(
                title="🛡️ Comandos de Moderação",
                description="Comandos para gerenciar e moderar o servidor",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="📝 Sistema de Warns",
                value=(
                    "`!warn <usuário> [motivo]` — Adverte um usuário\n"
                    "`!verwarns [usuário]` — Ver advertências\n"
                    "`!clearwarns <usuário>` — Remove todas advertências\n"
                    "`!unwarn <usuário> <número>` — Remove warn específico\n"
                    "`!warnslist` — Lista todos com advertências\n"
                    "⚠️ *3 warns = mute automático*"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🔇 Silenciamento",
                value=(
                    "`!mute <usuário> [tempo] [motivo]` — Silencia usuário\n"
                    "`!unmute <usuário>` — Remove silenciamento\n"
                    "`!setupmute` — Configura sistema de mute\n"
                    "💡 *Tempo em minutos, 0 = indefinido*"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🚨 Ações de Moderação",
                value=(
                    "`!kick <usuário> [motivo]` — Expulsa usuário\n"
                    "`!ban <usuário> [motivo]` — Bane usuário\n"
                    "`!limpar <quantidade>` — Apaga mensagens (máx: 100)"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🤖 Sistemas Automáticos",
                value=(
                    "• **Anti-Spam:** 5 mensagens em 10s = warn automático\n"
                    "• **Mute Automático:** 3 warns = mute\n"
                    "• **Logs:** Todas ações são registradas"
                ),
                inline=False
            )
        
        elif categoria in ["info", "informacao", "informação"]:
            embed = discord.Embed(
                title="ℹ️ Comandos de Informação",
                description="Comandos para obter informações",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="📋 Comandos Disponíveis",
                value=(
                    "`!ajuda` — Mostra esta mensagem\n"
                    "`!ping` — Verifica latência do bot\n"
                    "`!botinfo` — Informações do bot\n"
                    "`!terms` — Termos de Serviço\n"
                    "`!privacy` — Política de Privacidade"
                ),
                inline=False
            )
        
        elif categoria in ["niveis", "níveis", "xp", "level"]:
            embed = discord.Embed(
                title="⭐ Sistema de Níveis e XP",
                description="Ganhe experiência conversando no servidor!",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="📊 Como Funciona",
                value=(
                    "• Ganhe **10 XP** a cada mensagem enviada\n"
                    "• Ganhe **1 moeda** a cada mensagem enviada\n"
                    "• Máximo de 50 XP por minuto (anti-spam)\n"
                    "• Fórmula de nível: `√(XP/100)`\n"
                    "• Ganhe **10 moedas** ao subir de nível!\n"
                    "• Receba notificação ao subir de nível!\n"
                    "• Desbloqueie conquistas ao atingir marcos!"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🎮 Comandos de Perfil",
                value=(
                    "`!perfil [@usuário]` — Ver perfil completo\n"
                    "`!editarperfil bio <texto>` — Definir bio (máx 200 chars)\n"
                    "`!editarperfil status <texto>` — Definir status (máx 50 chars)\n"
                    "`!editarperfil limpar` — Limpar bio e status\n"
                    "`!rank [página]` — Top 10 usuários com mais XP"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🏆 Conquistas",
                value=(
                    "`!conquistas [@usuário]` — Ver conquistas desbloqueadas\n\n"
                    "Desbloqueie conquistas ao:\n"
                    "• Enviar mensagens (1, 100, 1000)\n"
                    "• Ficar em canais de voz (10 horas)\n"
                    "• Completar 1 ano no servidor\n"
                    "• Subir de nível (1, 5, 10, 20, 50)\n"
                    "• Acumular XP (10k, 100k)"
                ),
                inline=False
            )
            
            embed.add_field(
                name="👑 Comandos Fundador",
                value=(
                    "`!addxp @usuário <valor>` — Adiciona XP (Owner)\n"
                    "`!resetperfil @usuário` — Reseta perfil (Owner)"
                ),
                inline=False
            )
        
        elif categoria in ["economia", "moedas", "loja", "shop"]:
            embed = discord.Embed(
                title="💰 Sistema de Economia e Loja",
                description="Ganhe e gaste moedas no servidor!",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="💵 Como Ganhar Moedas",
                value=(
                    "• **+1 moeda** por mensagem enviada\n"
                    "• **+10 moedas** ao subir de nível\n"
                    "• Receba moedas de outros usuários\n"
                    "• Ganhe recompensas de eventos (Admin)"
                ),
                inline=False
            )
            
            embed.add_field(
                name="💰 Comandos de Moedas",
                value=(
                    "`!saldo [@usuário]` — Ver saldo de moedas\n"
                    "`!pagar @usuário <valor>` — Transferir moedas\n"
                    "`!ranking [página]` — Top 10 mais ricos"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🏪 Sistema de Loja",
                value=(
                    "`!loja` — Ver resumo de categorias\n"
                    "`!loja <categoria>` — Ver itens da categoria\n"
                    "`!loja todos` — Ver todos os itens\n"
                    "`!comprar <ID>` — Comprar item\n"
                    "`!inventario [@usuário]` — Ver itens comprados\n"
                    "`!usaritem <ID>` — Aplicar item ao perfil"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🎨 Personalização",
                value=(
                    "`!customizar` — Menu de personalização\n"
                    "`!customizar cor <#hex>` — Cor do perfil\n"
                    "`!customizar titulo <texto>` — Título customizado\n"
                    "`!customizar limpar` — Remover customizações\n\n"
                    "⚠️ **Banners só pela loja** (`!loja banner`)"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🎨 Categorias da Loja",
                value=(
                    "**banner** — 6 banners Gaucho (450-600 moedas)\n"
                    "**cor** — 5 cores personalizadas de perfil\n"
                    "**titulo** — 3 títulos especiais\n"
                    "**badge** — 5 badges exclusivas\n"
                    "**cargo** — 4 cargos especiais\n"
                    "**boost** — 3 multiplicadores de XP/moedas\n\n"
                    "📦 **Total:** 26 itens disponíveis"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🛡️ Comandos Administrador",
                value=(
                    "`!darmoedas @usuário <valor>` — Dar moedas (Admin)\n"
                    "💡 *Limite de 10.000 moedas por uso*"
                ),
                inline=False
            )
            
            embed.add_field(
                name="👑 Comandos Fundador",
                value=(
                    "`!addmoedas @usuário <valor>` — Adicionar moedas (Owner)\n"
                    "`!removermoedas @usuário <valor>` — Remover moedas (Owner)\n"
                    "`!setmoedas @usuário <valor>` — Definir saldo (Owner)"
                ),
                inline=False
            )
        
        elif categoria in ["utilitarios", "util", "utilitários"]:
            embed = discord.Embed(
                title="⚙️ Comandos Utilitários",
                description="Comandos úteis e de diversão",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="👤 Informações",
                value=(
                    "`!avatar [usuário]` — Mostra avatar\n"
                    "`!userinfo [usuário]` — Info do usuário\n"
                    "`!serverinfo` — Info do servidor"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🎮 Diversão",
                value=(
                    "`!coinflip` — Cara ou coroa\n"
                    "`!dado [lados]` — Rola um dado\n"
                    "`!escolher <op1> <op2> ...` — Escolhe aleatoriamente"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🎪 Interativos",
                value=(
                    "`!votacao [pergunta]` — Inicia votação\n"
                    "`!sorteio [tempo] [prêmio]` — Faz sorteio\n"
                    "`!say <mensagem>` — Bot repete mensagem\n"
                    "`!embed <título> <descrição>` — Cria embed"
                ),
                inline=False
            )
        
        else:
            await ctx.send(
                "❌ Categoria não encontrada!\n"
                "📚 **Categorias disponíveis:**\n"
                "`moderacao`, `info`, `niveis`, `economia`, `utilitarios`"
            )
            return
        
        embed.set_footer(text="Use ! antes de cada comando")
        await ctx.send(embed=embed)

    @commands.command(name="terms", aliases=["termos", "tos"])
    async def terms(self, ctx):
        """Exibe os Termos de Serviço do bot"""
        embed = discord.Embed(
            title="📄 Termos de Serviço",
            description=(
                "Ao usar este bot, você concorda com os seguintes termos:\n\n"
                "**1. Uso Adequado**\n"
                "• O bot deve ser usado apenas para fins legítimos\n"
                "• Não utilize o bot para spam, assédio ou conteúdo inapropriado\n\n"
                "**2. Moderação**\n"
                "• As ações de moderação são de responsabilidade dos moderadores\n"
                "• O bot registra ações para auditoria\n\n"
                "**3. Disponibilidade**\n"
                "• O bot é fornecido \"como está\"\n"
                "• Pode haver períodos de indisponibilidade para manutenção\n\n"
                "**4. Alterações**\n"
                "• Os termos podem ser alterados a qualquer momento"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Última atualização: Dezembro 2025")
        await ctx.send(embed=embed)

    @commands.command(name="privacy", aliases=["privacidade", "dados"])
    async def privacy(self, ctx):
        """Exibe a Política de Privacidade do bot"""
        embed = discord.Embed(
            title="🔒 Política de Privacidade",
            description=(
                "Informações sobre como seus dados são tratados:\n\n"
                "**Dados Coletados**\n"
                "• IDs de usuários, servidores e mensagens\n"
                "• Advertências e ações de moderação\n"
                "• XP, níveis e estatísticas de atividade\n"
                "• Logs de comandos usados\n\n"
                "**Uso dos Dados**\n"
                "• Funcionamento do sistema de moderação\n"
                "• Sistema de níveis e ranking\n"
                "• Auditoria e segurança do servidor\n"
                "• Melhoria do bot\n\n"
                "**Armazenamento**\n"
                "• Dados armazenados localmente em arquivos JSON e SQLite\n"
                "• Não compartilhamos dados com terceiros\n"
                "• Backup automático para segurança\n\n"
                "**Seus Direitos**\n"
                "• Você pode solicitar remoção dos seus dados\n"
                "• Entre em contato com os administradores"
            ),
            color=discord.Color.purple()
        )
        embed.set_footer(text="Última atualização: Dezembro 2025")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ajuda(bot))
