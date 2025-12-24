"""
Sistema de Níveis e XP
Sistema completo de experiência, níveis e ranking para usuários do servidor
"""
import discord
from discord.ext import commands
import sqlite3
import math
import asyncio
from typing import Optional

class SistemaNiveis(commands.Cog):
    """Sistema de XP e níveis para usuários"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "data/niveis.db"
        self.xp_cooldown = {}  # Prevenir spam de XP
        self.cooldown_time = 60  # Segundos entre ganhos de XP
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Cria tabela de usuários se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_discord INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                xp INTEGER DEFAULT 0,
                nivel INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados de níveis inicializado")
    
    def _calcular_nivel(self, xp: int) -> int:
        """
        Calcula o nível baseado no XP
        Fórmula: nível = floor(sqrt(xp / 100))
        
        Args:
            xp: Quantidade de XP do usuário
            
        Returns:
            Nível calculado
        """
        return math.floor(math.sqrt(xp / 100))
    
    def _xp_para_proximo_nivel(self, nivel_atual: int) -> int:
        """
        Calcula quanto XP é necessário para o próximo nível
        
        Args:
            nivel_atual: Nível atual do usuário
            
        Returns:
            XP total necessário para o próximo nível
        """
        return (nivel_atual + 1) ** 2 * 100
    
    def _obter_usuario(self, user_id: int, nome: str) -> dict:
        """
        Obtém dados do usuário do banco ou cria novo registro
        
        Args:
            user_id: ID do Discord do usuário
            nome: Nome do usuário
            
        Returns:
            Dicionário com dados do usuário
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca usuário
        cursor.execute('SELECT id_discord, nome, xp, nivel FROM usuarios WHERE id_discord = ?', (user_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            # Atualiza nome se mudou
            if resultado[1] != nome:
                cursor.execute('UPDATE usuarios SET nome = ? WHERE id_discord = ?', (nome, user_id))
                conn.commit()
            
            usuario = {
                'id_discord': resultado[0],
                'nome': nome,
                'xp': resultado[2],
                'nivel': resultado[3]
            }
        else:
            # Cria novo usuário
            cursor.execute('INSERT INTO usuarios (id_discord, nome, xp, nivel) VALUES (?, ?, 0, 0)',
                          (user_id, nome))
            conn.commit()
            usuario = {
                'id_discord': user_id,
                'nome': nome,
                'xp': 0,
                'nivel': 0
            }
        
        conn.close()
        return usuario
    
    def _atualizar_usuario(self, user_id: int, xp: int, nivel: int):
        """
        Atualiza XP e nível do usuário no banco
        
        Args:
            user_id: ID do Discord do usuário
            xp: Novo valor de XP
            nivel: Novo nível
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE usuarios SET xp = ?, nivel = ? WHERE id_discord = ?',
                      (xp, nivel, user_id))
        
        conn.commit()
        conn.close()
    
    async def _adicionar_xp(self, member: discord.Member, quantidade: int = 10) -> dict:
        """
        Adiciona XP ao usuário e verifica se subiu de nível
        
        Args:
            member: Membro do Discord
            quantidade: Quantidade de XP a adicionar (padrão: 10)
            
        Returns:
            Dicionário com informações da atualização:
            - subiu_nivel: bool
            - nivel_anterior: int
            - nivel_novo: int
            - xp_total: int
        """
        usuario = self._obter_usuario(member.id, str(member.name))
        
        # Adiciona XP
        xp_anterior = usuario['xp']
        nivel_anterior = usuario['nivel']
        
        xp_novo = xp_anterior + quantidade
        nivel_novo = self._calcular_nivel(xp_novo)
        
        # Atualiza banco
        self._atualizar_usuario(member.id, xp_novo, nivel_novo)
        
        return {
            'subiu_nivel': nivel_novo > nivel_anterior,
            'nivel_anterior': nivel_anterior,
            'nivel_novo': nivel_novo,
            'xp_total': xp_novo
        }
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Evento que dá XP quando usuário envia mensagem
        Sistema de cooldown para evitar spam
        """
        # Ignora bots e mensagens de comando
        if message.author.bot or message.content.startswith('!'):
            return
        
        # Verifica cooldown
        user_id = message.author.id
        import time
        tempo_atual = time.time()
        
        if user_id in self.xp_cooldown:
            tempo_passado = tempo_atual - self.xp_cooldown[user_id]
            if tempo_passado < self.cooldown_time:
                return  # Ainda em cooldown
        
        # Atualiza cooldown
        self.xp_cooldown[user_id] = tempo_atual
        
        # Adiciona XP
        resultado = await self._adicionar_xp(message.author, 10)
        
        # Se subiu de nível, parabeniza
        if resultado['subiu_nivel']:
            embed = discord.Embed(
                title="🎉 Level Up!",
                description=f"Parabéns {message.author.mention}! Você subiu para o **nível {resultado['nivel_novo']}**!",
                color=discord.Color.gold()
            )
            embed.add_field(
                name="📊 Progresso",
                value=f"Nível anterior: {resultado['nivel_anterior']}\n"
                      f"Nível atual: {resultado['nivel_novo']}\n"
                      f"XP total: {resultado['xp_total']:,}",
                inline=False
            )
            
            await message.channel.send(embed=embed)
    
    @commands.command(name="perfil", aliases=["profile", "nivel", "level"])
    async def perfil(self, ctx, membro: discord.Member = None):
        """
        Mostra o perfil de XP e nível do usuário
        
        Uso: !perfil [@usuário]
        """
        membro = membro or ctx.author
        usuario = self._obter_usuario(membro.id, str(membro.name))
        
        # Calcula XP para próximo nível
        xp_atual = usuario['xp']
        nivel_atual = usuario['nivel']
        xp_proximo = self._xp_para_proximo_nivel(nivel_atual)
        xp_nivel_atual = nivel_atual ** 2 * 100
        xp_necessario = xp_proximo - xp_atual
        
        # Calcula progresso em porcentagem
        xp_no_nivel = xp_atual - xp_nivel_atual
        xp_para_nivel = xp_proximo - xp_nivel_atual
        progresso = (xp_no_nivel / xp_para_nivel * 100) if xp_para_nivel > 0 else 0
        
        # Barra de progresso
        barra_tamanho = 10
        barra_preenchida = int(progresso / 10)
        barra = "█" * barra_preenchida + "░" * (barra_tamanho - barra_preenchida)
        
        embed = discord.Embed(
            title=f"📊 Perfil de {membro.display_name}",
            color=membro.color if membro.color != discord.Color.default() else discord.Color.blue()
        )
        
        avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        embed.add_field(
            name="⭐ Nível",
            value=f"**{nivel_atual}**",
            inline=True
        )
        embed.add_field(
            name="💎 XP Total",
            value=f"**{xp_atual:,}**",
            inline=True
        )
        embed.add_field(
            name="🎯 Próximo Nível",
            value=f"**{nivel_atual + 1}**",
            inline=True
        )
        
        embed.add_field(
            name="📈 Progresso para o próximo nível",
            value=f"{barra} {progresso:.1f}%\n"
                  f"`{xp_no_nivel:,} / {xp_para_nivel:,} XP` (faltam {xp_necessario:,} XP)",
            inline=False
        )
        
        embed.set_footer(text=f"ID: {membro.id}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="ranking", aliases=["rank", "leaderboard", "top"])
    async def ranking(self, ctx, pagina: int = 1):
        """
        Mostra o ranking dos 10 usuários com mais XP
        
        Uso: !ranking [página]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca top usuários
        cursor.execute('SELECT nome, xp, nivel FROM usuarios ORDER BY xp DESC LIMIT 10 OFFSET ?',
                      ((pagina - 1) * 10,))
        resultados = cursor.fetchall()
        conn.close()
        
        if not resultados:
            await ctx.send("❌ Nenhum usuário encontrado no ranking!")
            return
        
        embed = discord.Embed(
            title="🏆 Ranking de Níveis",
            description="Top 10 usuários com mais XP",
            color=discord.Color.gold()
        )
        
        medalhas = ["🥇", "🥈", "🥉"]
        
        for idx, (nome, xp, nivel) in enumerate(resultados, start=(pagina - 1) * 10 + 1):
            medalha = medalhas[idx - 1] if idx <= 3 else f"**#{idx}**"
            
            embed.add_field(
                name=f"{medalha} {nome}",
                value=f"Nível: **{nivel}** | XP: **{xp:,}**",
                inline=False
            )
        
        embed.set_footer(text=f"Página {pagina} • Use !ranking [página] para ver mais")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="addxp")
    @commands.has_permissions(administrator=True)
    async def addxp(self, ctx, membro: discord.Member, quantidade: int):
        """
        Adiciona XP manualmente a um usuário (apenas administradores)
        
        Uso: !addxp @usuário <quantidade>
        """
        if quantidade <= 0:
            await ctx.send("❌ A quantidade de XP deve ser maior que zero!")
            return
        
        resultado = await self._adicionar_xp(membro, quantidade)
        
        embed = discord.Embed(
            title="✅ XP Adicionado",
            description=f"{quantidade:,} XP foi adicionado a {membro.mention}",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="📊 Status Atual",
            value=f"Nível: **{resultado['nivel_novo']}**\n"
                  f"XP Total: **{resultado['xp_total']:,}**",
            inline=False
        )
        
        if resultado['subiu_nivel']:
            embed.add_field(
                name="🎉 Level Up!",
                value=f"Subiu do nível {resultado['nivel_anterior']} para {resultado['nivel_novo']}!",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="resetperfil", aliases=["resetxp"])
    @commands.has_permissions(administrator=True)
    async def resetperfil(self, ctx, membro: discord.Member):
        """
        Reseta o XP e nível de um usuário (apenas administradores)
        
        Uso: !resetperfil @usuário
        """
        # Atualiza para XP e nível 0
        self._atualizar_usuario(membro.id, 0, 0)
        
        embed = discord.Embed(
            title="🔄 Perfil Resetado",
            description=f"O perfil de {membro.mention} foi resetado!",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="📊 Novo Status",
            value="Nível: **0**\nXP: **0**",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @addxp.error
    @resetperfil.error
    async def comando_admin_error(self, ctx, error):
        """Tratamento de erros para comandos administrativos"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você precisa ser administrador para usar este comando!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Usuário não encontrado!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Argumento faltando! Use: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")

# Setup para carregar o cog
async def setup(bot):
    await bot.add_cog(SistemaNiveis(bot))
