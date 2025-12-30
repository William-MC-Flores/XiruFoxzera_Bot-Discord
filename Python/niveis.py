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
from datetime import datetime

class SistemaNiveis(commands.Cog):
    """Sistema de XP e níveis para usuários"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "data/niveis.db"
        self.xp_por_mensagem = 10  # XP ganho por mensagem
        self.max_xp_por_minuto = 50  # Limite anti-spam
        self.xp_historico = {}  # Rastreia XP ganho no último minuto por usuário
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
                nivel INTEGER DEFAULT 0,
                moedas INTEGER DEFAULT 0,
                bio TEXT DEFAULT '',
                status_personalizado TEXT DEFAULT '',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cria tabela de conquistas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conquistas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                descricao TEXT NOT NULL,
                emoji TEXT NOT NULL,
                requisito_tipo TEXT NOT NULL,
                requisito_valor INTEGER NOT NULL
            )
        ''')
        
        # Cria tabela de conquistas dos usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios_conquistas (
                id_discord INTEGER,
                conquista_id INTEGER,
                data_desbloqueio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id_discord, conquista_id),
                FOREIGN KEY (id_discord) REFERENCES usuarios(id_discord),
                FOREIGN KEY (conquista_id) REFERENCES conquistas(id)
            )
        ''')
        
        # Cria tabela de loja
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_item TEXT UNIQUE NOT NULL,
                preco INTEGER NOT NULL,
                tipo_item TEXT NOT NULL,
                descricao TEXT DEFAULT '',
                disponivel INTEGER DEFAULT 1
            )
        ''')
        
        # Cria tabela de inventário
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventario (
                id_discord INTEGER,
                id_item INTEGER,
                data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                quantidade INTEGER DEFAULT 1,
                PRIMARY KEY (id_discord, id_item),
                FOREIGN KEY (id_discord) REFERENCES usuarios(id_discord),
                FOREIGN KEY (id_item) REFERENCES loja(id)
            )
        ''')
        
        # Adiciona colunas na tabela existente se não existirem
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN bio TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN status_personalizado TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN moedas INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        except sqlite3.OperationalError:
            pass
        
        # Insere conquistas padrão se não existirem
        conquistas_padrao = [
            ("Primeira Mensagem", "Enviou a primeira mensagem", "✨", "mensagens", 1),
            ("Conversador", "Enviou 100 mensagens", "💬", "mensagens", 100),
            ("Tagarela", "Enviou 1000 mensagens", "🗣️", "mensagens", 1000),
            ("Novato", "Alcançou o nível 1", "🌱", "nivel", 1),
            ("Iniciante", "Alcançou o nível 5", "🔰", "nivel", 5),
            ("Experiente", "Alcançou o nível 10", "⭐", "nivel", 10),
            ("Veterano", "Alcançou o nível 20", "🏆", "nivel", 20),
            ("Lenda", "Alcançou o nível 50", "👑", "nivel", 50),
            ("Colecionador de XP", "Acumulou 10.000 XP", "💎", "xp", 10000),
            ("Mestre do XP", "Acumulou 100.000 XP", "💠", "xp", 100000),
        ]
        
        for nome, desc, emoji, tipo, valor in conquistas_padrao:
            try:
                cursor.execute(
                    'INSERT OR IGNORE INTO conquistas (nome, descricao, emoji, requisito_tipo, requisito_valor) VALUES (?, ?, ?, ?, ?)',
                    (nome, desc, emoji, tipo, valor)
                )
            except sqlite3.IntegrityError:
                pass
        
        # Insere itens padrão da loja se não existirem
        itens_padrao = [
            # Decorações de perfil
            ("Borda Dourada", 150, "decoração", "Borda dourada elegante para seu perfil"),
            ("Borda Arco-Íris", 200, "decoração", "Borda colorida com efeito arco-íris"),
            ("Fundo Estrelas", 180, "decoração", "Fundo estrelado para seu perfil"),
            ("Fundo Galaxia", 250, "decoração", "Fundo espacial com galáxias"),
            ("Título Personalizado", 400, "decoração", "Define um título único que aparece no seu perfil"),
            ("Cor Personalizada", 300, "decoração", "Permite escolher uma cor para seu nome no ranking"),
            
            # Badges especiais
            ("Badge VIP", 500, "badge", "Badge exclusivo VIP exibido no perfil"),
            ("Badge Desenvolvedor", 800, "badge", "Badge especial de desenvolvedor"),
            ("Badge Estrela", 350, "badge", "Badge de estrela brilhante"),
            ("Badge Coroa", 600, "badge", "Badge de coroa real"),
            ("Badge Diamante", 1000, "badge", "Badge exclusivo de diamante"),
            
            # Cargos exclusivos
            ("Cargo VIP", 1500, "cargo", "Cargo VIP exclusivo com benefícios especiais"),
            ("Cargo Elite", 2500, "cargo", "Cargo Elite para membros dedicados"),
            ("Cargo Lendário", 5000, "cargo", "Cargo Lendário para os mais ativos"),
            ("Cargo Apoiador", 1000, "cargo", "Cargo especial de apoiador da comunidade"),
            
            # Boosts e utilidades
            ("Boost de XP (1h)", 100, "boost", "Dobra o ganho de XP por 1 hora"),
            ("Boost de XP (24h)", 500, "boost", "Dobra o ganho de XP por 24 horas"),
            ("Boost de Moedas (1h)", 150, "boost", "Dobra o ganho de moedas por 1 hora"),
            ("Carta Especial", 50, "item", "Uma carta especial para personalizar seu perfil"),
        ]
        
        for nome, preco, tipo, desc in itens_padrao:
            try:
                cursor.execute(
                    'INSERT OR IGNORE INTO loja (nome_item, preco, tipo_item, descricao) VALUES (?, ?, ?, ?)',
                    (nome, preco, tipo, desc)
                )
            except sqlite3.IntegrityError:
                pass
        
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
        
        # Busca usuário com todos os campos
        cursor.execute('''
            SELECT id_discord, nome, xp, nivel, moedas, bio, status_personalizado, data_criacao 
            FROM usuarios WHERE id_discord = ?
        ''', (user_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            # Atualiza nome e timestamp se mudou
            if resultado[1] != nome:
                cursor.execute('''
                    UPDATE usuarios 
                    SET nome = ?, ultima_atualizacao = CURRENT_TIMESTAMP 
                    WHERE id_discord = ?
                ''', (nome, user_id))
                conn.commit()
            
            usuario = {
                'id_discord': resultado[0],
                'nome': nome,
                'xp': resultado[2],
                'nivel': resultado[3],
                'moedas': resultado[4],
                'bio': resultado[5] or '',
                'status_personalizado': resultado[6] or '',
                'data_criacao': resultado[7]
            }
        else:
            # Cria novo usuário
            cursor.execute('''
                INSERT INTO usuarios (id_discord, nome, xp, nivel, moedas, bio, status_personalizado) 
                VALUES (?, ?, 0, 0, 0, '', '')
            ''', (user_id, nome))
            conn.commit()
            
            # Busca o usuário criado para pegar a data
            cursor.execute('''
                SELECT id_discord, nome, xp, nivel, moedas, bio, status_personalizado, data_criacao 
                FROM usuarios WHERE id_discord = ?
            ''', (user_id,))
            resultado = cursor.fetchone()
            
            usuario = {
                'id_discord': user_id,
                'nome': nome,
                'xp': 0,
                'nivel': 0,
                'moedas': 0,
                'bio': '',
                'status_personalizado': '',
                'data_criacao': resultado[7] if resultado else None
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
        
        # Calcula moedas a ganhar: +1 por mensagem + 10 por nível
        moedas_ganhas_nivel = 0
        if nivel_novo > nivel_anterior:
            niveis_ganhos = nivel_novo - nivel_anterior
            moedas_ganhas_nivel = niveis_ganhos * 10
        
        # OTIMIZAÇÃO: Combina todas as atualizações em uma única transação
        # +1 moeda por mensagem + moedas por level up (se aplicável)
        total_moedas = 1 + moedas_ganhas_nivel
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Atualiza XP, nível E moedas em uma única transação
        cursor.execute('''
            UPDATE usuarios 
            SET xp = ?, nivel = ?, moedas = moedas + ?
            WHERE id_discord = ?
        ''', (xp_novo, nivel_novo, total_moedas, member.id))
        
        conn.commit()
        conn.close()
        
        # Verifica conquistas desbloqueadas
        novas_conquistas = await self._verificar_conquistas(member.id, xp_novo, nivel_novo)
        
        return {
            'subiu_nivel': nivel_novo > nivel_anterior,
            'nivel_anterior': nivel_anterior,
            'nivel_novo': nivel_novo,
            'xp_total': xp_novo,
            'moedas_ganhas': moedas_ganhas_nivel,
            'novas_conquistas': novas_conquistas
        }
    
    async def _verificar_conquistas(self, user_id: int, xp: int, nivel: int) -> list:
        """
        Verifica e desbloqueia conquistas para o usuário
        
        Args:
            user_id: ID do Discord do usuário
            xp: XP atual do usuário
            nivel: Nível atual do usuário
            
        Returns:
            Lista de conquistas recém-desbloqueadas
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca todas as conquistas
        cursor.execute('SELECT id, nome, descricao, emoji, requisito_tipo, requisito_valor FROM conquistas')
        conquistas = cursor.fetchall()
        
        # Busca conquistas já desbloqueadas
        cursor.execute('SELECT conquista_id FROM usuarios_conquistas WHERE id_discord = ?', (user_id,))
        desbloqueadas = set(row[0] for row in cursor.fetchall())
        
        # Calcula número de mensagens (aproximado)
        mensagens = xp // 10
        
        novas_conquistas = []
        
        for conquista_id, nome, desc, emoji, req_tipo, req_valor in conquistas:
            # Se já desbloqueou, pula
            if conquista_id in desbloqueadas:
                continue
            
            # Verifica requisito
            desbloqueou = False
            if req_tipo == "mensagens" and mensagens >= req_valor:
                desbloqueou = True
            elif req_tipo == "nivel" and nivel >= req_valor:
                desbloqueou = True
            elif req_tipo == "xp" and xp >= req_valor:
                desbloqueou = True
            
            if desbloqueou:
                # Adiciona conquista ao usuário
                cursor.execute('''
                    INSERT INTO usuarios_conquistas (id_discord, conquista_id) 
                    VALUES (?, ?)
                ''', (user_id, conquista_id))
                novas_conquistas.append({
                    'nome': nome,
                    'descricao': desc,
                    'emoji': emoji
                })
        
        conn.commit()
        conn.close()
        
        return novas_conquistas
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Evento que dá XP quando usuário envia mensagem
        Sistema anti-spam: máximo 50 XP por minuto
        """
        # Ignora bots e mensagens de comando
        if message.author.bot or message.content.startswith('!'):
            return
        
        user_id = message.author.id
        import time
        tempo_atual = time.time()
        
        # Inicializa histórico do usuário se não existir
        if user_id not in self.xp_historico:
            self.xp_historico[user_id] = []
        
        # Remove mensagens com mais de 60 segundos do histórico
        self.xp_historico[user_id] = [
            timestamp for timestamp in self.xp_historico[user_id]
            if tempo_atual - timestamp < 60
        ]
        
        # Verifica se já atingiu o limite de XP no último minuto
        xp_ganho_ultimo_minuto = len(self.xp_historico[user_id]) * self.xp_por_mensagem
        
        if xp_ganho_ultimo_minuto >= self.max_xp_por_minuto:
            # Atingiu o limite, não ganha XP
            return
        
        # Adiciona timestamp atual ao histórico
        self.xp_historico[user_id].append(tempo_atual)
        
        # Adiciona XP (e moedas serão atualizadas dentro de _adicionar_xp)
        resultado = await self._adicionar_xp(message.author, self.xp_por_mensagem)
        
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
            
            # Adiciona informação sobre moedas ganhas
            if resultado.get('moedas_ganhas', 0) > 0:
                embed.add_field(
                    name="💰 Recompensa",
                    value=f"+{resultado['moedas_ganhas']} moedas",
                    inline=False
                )
            
            await message.channel.send(embed=embed)
        
        # Notifica sobre novas conquistas
        if resultado.get('novas_conquistas'):
            for conquista in resultado['novas_conquistas']:
                embed = discord.Embed(
                    title="🏆 Conquista Desbloqueada!",
                    description=f"{message.author.mention} desbloqueou uma conquista!",
                    color=discord.Color.purple()
                )
                embed.add_field(
                    name=f"{conquista['emoji']} {conquista['nome']}",
                    value=conquista['descricao'],
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
        
        # Busca conquistas do usuário
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.emoji, c.nome 
            FROM conquistas c
            JOIN usuarios_conquistas uc ON c.id = uc.conquista_id
            WHERE uc.id_discord = ?
            ORDER BY uc.data_desbloqueio DESC
        ''', (membro.id,))
        conquistas = cursor.fetchall()
        conn.close()
        
        # Cria embed
        embed = discord.Embed(
            title=f"📊 Perfil de {membro.display_name}",
            color=membro.color if membro.color != discord.Color.default() else discord.Color.blue()
        )
        
        avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        # Status personalizado (se houver)
        if usuario.get('status_personalizado'):
            embed.description = f"💬 *{usuario['status_personalizado']}*"
        
        # Bio personalizada (se houver)
        if usuario.get('bio'):
            embed.add_field(
                name="📝 Bio",
                value=usuario['bio'],
                inline=False
            )
        
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
            name="💰 Moedas",
            value=f"**{usuario['moedas']:,}**",
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
        
        # Mostra conquistas (máximo 5 mais recentes)
        if conquistas:
            conquistas_texto = " ".join([f"{emoji}" for emoji, nome in conquistas[:5]])
            total_conquistas = len(conquistas)
            if total_conquistas > 5:
                conquistas_texto += f" **+{total_conquistas - 5}**"
            
            embed.add_field(
                name=f"🏆 Conquistas ({total_conquistas})",
                value=conquistas_texto,
                inline=False
            )
        
        # Data de criação do perfil
        if usuario.get('data_criacao'):
            embed.add_field(
                name="📅 Membro desde",
                value=f"<t:{int(datetime.fromisoformat(usuario['data_criacao']).timestamp())}:D>",
                inline=False
            )
        
        embed.set_footer(text=f"ID: {membro.id} • Use !editarperfil para personalizar")
        
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
    
    @commands.command(name='saldo', aliases=['balance', 'moedas', 'coins'])
    async def saldo(self, ctx, membro: discord.Member = None):
        """
        Mostra o saldo de moedas de um usuário
        
        Uso: !saldo [@usuário]
        """
        membro = membro or ctx.author
        usuario = self._obter_usuario(membro.id, str(membro.name))
        
        embed = discord.Embed(
            title=f"💰 Saldo de {membro.display_name}",
            description=f"**{usuario['moedas']:,}** moedas",
            color=discord.Color.gold()
        )
        
        avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        embed.add_field(
            name="📊 Informações",
            value=f"Nível: **{usuario['nivel']}**\n"
                  f"XP: **{usuario['xp']:,}**",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='pagar', aliases=['pay', 'transferir', 'transfer'])
    async def pagar(self, ctx, destinatario: discord.Member, valor: int):
        """
        Transfere moedas para outro usuário
        
        Uso: !pagar @usuário <valor>
        """
        # Validações
        if destinatario.bot:
            await ctx.send("❌ Você não pode transferir moedas para bots!")
            return
        
        if destinatario.id == ctx.author.id:
            await ctx.send("❌ Você não pode transferir moedas para si mesmo!")
            return
        
        if valor <= 0:
            await ctx.send("❌ O valor deve ser maior que zero!")
            return
        
        # Verifica saldo do remetente
        remetente = self._obter_usuario(ctx.author.id, str(ctx.author.name))
        
        if remetente['moedas'] < valor:
            await ctx.send(f"❌ Você não tem moedas suficientes! Saldo atual: **{remetente['moedas']:,}** moedas")
            return
        
        # Realiza transferência
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Remove moedas do remetente
        cursor.execute('''
            UPDATE usuarios 
            SET moedas = moedas - ?
            WHERE id_discord = ?
        ''', (valor, ctx.author.id))
        
        # Adiciona moedas ao destinatário
        cursor.execute('''
            UPDATE usuarios 
            SET moedas = moedas + ?
            WHERE id_discord = ?
        ''', (valor, destinatario.id))
        
        conn.commit()
        conn.close()
        
        # Confirmação
        embed = discord.Embed(
            title="✅ Transferência Realizada",
            description=f"{ctx.author.mention} transferiu **{valor:,}** moedas para {destinatario.mention}",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="💸 Remetente",
            value=f"{ctx.author.display_name}\n"
                  f"Saldo: **{remetente['moedas'] - valor:,}** moedas",
            inline=True
        )
        
        dest_usuario = self._obter_usuario(destinatario.id, str(destinatario.name))
        embed.add_field(
            name="💰 Destinatário",
            value=f"{destinatario.display_name}\n"
                  f"Saldo: **{dest_usuario['moedas'] + valor:,}** moedas",
            inline=True
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='rankingmoedas', aliases=['topmoedas', 'rankmoedas', 'richest'])
    async def ranking_moedas(self, ctx, pagina: int = 1):
        """
        Mostra o ranking dos 10 usuários mais ricos
        
        Uso: !rankingmoedas [página]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca top usuários por moedas
        cursor.execute('SELECT nome, moedas, nivel FROM usuarios ORDER BY moedas DESC LIMIT 10 OFFSET ?',
                      ((pagina - 1) * 10,))
        resultados = cursor.fetchall()
        conn.close()
        
        if not resultados:
            await ctx.send("❌ Nenhum usuário encontrado no ranking!")
            return
        
        embed = discord.Embed(
            title="💰 Ranking de Moedas",
            description="Top 10 usuários mais ricos",
            color=discord.Color.gold()
        )
        
        medalhas = ["🥇", "🥈", "🥉"]
        
        for idx, (nome, moedas, nivel) in enumerate(resultados, start=1):
            posicao = ((pagina - 1) * 10) + idx
            medalha = medalhas[posicao - 1] if posicao <= 3 else f"`#{posicao}`"
            
            embed.add_field(
                name=f"{medalha} {nome}",
                value=f"💰 **{moedas:,}** moedas | Nível {nivel}",
                inline=False
            )
        
        embed.set_footer(text=f"Página {pagina} • Use !rankingmoedas <página> para ver mais")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="addxp")
    @commands.is_owner()
    async def addxp(self, ctx, membro: discord.Member, quantidade: int):
        """
        Adiciona XP manualmente a um usuário (apenas fundador)
        
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
    @commands.is_owner()
    async def resetperfil(self, ctx, membro: discord.Member):
        """
        Reseta o XP e nível de um usuário (apenas fundador)
        
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
    
    @commands.command(name="editarperfil", aliases=["editprofile", "setbio"])
    async def editarperfil(self, ctx, tipo: str = None, *, conteudo: str = None):
        """
        Edita informações do seu perfil
        
        Uso: 
        !editarperfil bio <texto> - Define sua bio (máx 200 caracteres)
        !editarperfil status <texto> - Define seu status (máx 50 caracteres)
        !editarperfil limpar - Remove bio e status
        """
        if not tipo:
            embed = discord.Embed(
                title="✏️ Editar Perfil",
                description="Configure seu perfil personalizado!",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="📝 Comandos Disponíveis",
                value=(
                    "`!editarperfil bio <texto>` - Define sua bio\n"
                    "`!editarperfil status <texto>` - Define seu status\n"
                    "`!editarperfil limpar` - Remove bio e status"
                ),
                inline=False
            )
            embed.add_field(
                name="📏 Limites",
                value="Bio: 200 caracteres\nStatus: 50 caracteres",
                inline=False
            )
            await ctx.send(embed=embed)
            return
        
        tipo = tipo.lower()
        
        if tipo == "limpar":
            # Remove bio e status
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE usuarios 
                SET bio = '', status_personalizado = '', ultima_atualizacao = CURRENT_TIMESTAMP
                WHERE id_discord = ?
            ''', (ctx.author.id,))
            conn.commit()
            conn.close()
            
            await ctx.send("✅ Bio e status removidos com sucesso!")
            return
        
        if not conteudo:
            await ctx.send(f"❌ Você precisa fornecer um texto! Exemplo: `!editarperfil {tipo} Seu texto aqui`")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if tipo in ["bio", "biografia"]:
            if len(conteudo) > 200:
                await ctx.send("❌ A bio deve ter no máximo 200 caracteres!")
                return
            
            cursor.execute('''
                UPDATE usuarios 
                SET bio = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                WHERE id_discord = ?
            ''', (conteudo, ctx.author.id))
            conn.commit()
            conn.close()
            
            embed = discord.Embed(
                title="✅ Bio Atualizada!",
                description=f"📝 **Nova bio:**\n{conteudo}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            
        elif tipo in ["status", "estado"]:
            if len(conteudo) > 50:
                await ctx.send("❌ O status deve ter no máximo 50 caracteres!")
                return
            
            cursor.execute('''
                UPDATE usuarios 
                SET status_personalizado = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                WHERE id_discord = ?
            ''', (conteudo, ctx.author.id))
            conn.commit()
            conn.close()
            
            embed = discord.Embed(
                title="✅ Status Atualizado!",
                description=f"💬 **Novo status:**\n*{conteudo}*",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Tipo inválido! Use: `bio` ou `status`")
            conn.close()
    
    @commands.command(name="conquistas", aliases=["achievements", "badges"])
    async def conquistas(self, ctx, membro: discord.Member = None):
        """
        Mostra todas as conquistas desbloqueadas
        
        Uso: !conquistas [@usuário]
        """
        try:
            membro = membro or ctx.author
            
            # Busca conquistas do usuário
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Conquistas desbloqueadas
            cursor.execute('''
                SELECT c.emoji, c.nome, c.descricao, uc.data_desbloqueio
                FROM conquistas c
                JOIN usuarios_conquistas uc ON c.id = uc.conquista_id
                WHERE uc.id_discord = ?
                ORDER BY uc.data_desbloqueio DESC
            ''', (membro.id,))
            desbloqueadas = cursor.fetchall()
            
            # Total de conquistas disponíveis
            cursor.execute('SELECT COUNT(*) FROM conquistas')
            total_conquistas = cursor.fetchone()[0]
            conn.close()
            
            # Se não há conquistas no sistema
            if total_conquistas == 0:
                await ctx.send("⚠️ Nenhuma conquista está disponível no sistema ainda.")
                return
            
            embed = discord.Embed(
                title=f"🏆 Conquistas de {membro.display_name}",
                description=f"**{len(desbloqueadas)}/{total_conquistas}** conquistas desbloqueadas",
                color=discord.Color.gold() if desbloqueadas else discord.Color.greyple()
            )
            
            avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
            embed.set_thumbnail(url=avatar_url)
            
            if desbloqueadas:
                for emoji, nome, desc, data in desbloqueadas:
                    # Formata data
                    try:
                        data_obj = datetime.fromisoformat(data)
                        data_formatada = data_obj.strftime("%d/%m/%Y")
                    except:
                        data_formatada = "Data desconhecida"
                    
                    embed.add_field(
                        name=f"{emoji} {nome}",
                        value=f"{desc}\n*Desbloqueado em: {data_formatada}*",
                        inline=False
                    )
            else:
                pronome = "Você ainda não desbloqueou" if membro == ctx.author else f"{membro.display_name} ainda não desbloqueou"
                embed.add_field(
                    name="📭 Nenhuma conquista ainda",
                    value=f"{pronome} nenhuma conquista.\n\n"
                          f"💡 **Como desbloquear:**\n"
                          f"• Ganhe níveis conversando\n"
                          f"• Acumule XP e moedas\n"
                          f"• Participe ativamente do servidor",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(f"❌ Erro no comando conquistas: {e}")
            await ctx.send(f"❌ Ocorreu um erro ao buscar as conquistas. Tente novamente mais tarde.\n"
                          f"💡 Se o problema persistir, contate um administrador.")
    
    @commands.command(name='loja', aliases=['shop', 'store'])
    async def loja(self, ctx, categoria: str = None):
        """
        Mostra a loja de itens
        
        Uso: !loja [categoria]
        Categorias: decoracao, badge, cargo, boost, todos
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca moedas do usuário
        usuario = self._obter_usuario(ctx.author.id, str(ctx.author.name))
        
        # Se não especificou categoria, mostra resumo
        if not categoria:
            # Busca itens disponíveis agrupados por tipo
            cursor.execute('''
                SELECT tipo_item, COUNT(*), MIN(preco), MAX(preco)
                FROM loja 
                WHERE disponivel = 1
                GROUP BY tipo_item
                ORDER BY MIN(preco) ASC
            ''')
            categorias = cursor.fetchall()
            
            embed = discord.Embed(
                title="🏪 Loja Virtual",
                description=f"💰 Suas moedas: **{usuario['moedas']:,}**\n\n"
                            f"**Escolha uma categoria:**\n"
                            f"`!loja decoracao` — Decorações de perfil\n"
                            f"`!loja badge` — Badges especiais\n"
                            f"`!loja cargo` — Cargos exclusivos\n"
                            f"`!loja boost` — Boosts e utilidades\n"
                            f"`!loja todos` — Ver todos os itens",
                color=discord.Color.green()
            )
            
            emoji_categorias = {
                "decoração": "✨",
                "badge": "🏅",
                "cargo": "👑",
                "boost": "⚡",
                "item": "📦"
            }
            
            for tipo, qtd, min_preco, max_preco in categorias:
                emoji = emoji_categorias.get(tipo, "🎁")
                embed.add_field(
                    name=f"{emoji} {tipo.title()}",
                    value=f"{qtd} itens disponíveis\n"
                          f"💰 {min_preco:,} - {max_preco:,} moedas",
                    inline=True
                )
            
            conn.close()
            await ctx.send(embed=embed)
            return
        
        # Se especificou "todos", lista todos os itens
        if categoria.lower() == "todos":
            cursor.execute('''
                SELECT id, nome_item, preco, tipo_item, descricao 
                FROM loja 
                WHERE disponivel = 1
                ORDER BY tipo_item, preco ASC
            ''')
            todos_itens = cursor.fetchall()
            conn.close()
            
            if not todos_itens:
                await ctx.send("🏪 A loja está vazia no momento!")
                return
            
            embed = discord.Embed(
                title="🏪 Loja Virtual - Todos os Itens",
                description=f"💰 Suas moedas: **{usuario['moedas']:,}**\n"
                            f"Use `!comprar <ID>` para comprar um item",
                color=discord.Color.green()
            )
            
            # Agrupa por tipo
            tipo_atual = None
            for item_id, nome, preco, tipo, desc in todos_itens:
                emoji_tipo = {
                    "decoração": "✨",
                    "badge": "🏅",
                    "cargo": "👑",
                    "boost": "⚡",
                    "item": "📦"
                }.get(tipo, "🎁")
                
                pode_comprar = "✅" if usuario['moedas'] >= preco else "❌"
                
                # Adiciona separador de categoria
                if tipo != tipo_atual:
                    tipo_atual = tipo
                
                embed.add_field(
                    name=f"{pode_comprar} {nome} (ID: {item_id})",
                    value=f"{emoji_tipo} {tipo.title()} | 💰 **{preco:,}** moedas\n📝 {desc}",
                    inline=False
                )
            
            embed.set_footer(text="Use !loja <categoria> para filtrar por categoria")
            await ctx.send(embed=embed)
            return
        
        # Filtra por categoria específica
        categoria_map = {
            "decoracao": "decoração",
            "decoração": "decoração",
            "decoracoes": "decoração",
            "badge": "badge",
            "badges": "badge",
            "cargo": "cargo",
            "cargos": "cargo",
            "boost": "boost",
            "boosts": "boost"
        }
        
        tipo_filtro = categoria_map.get(categoria.lower())
        
        if not tipo_filtro:
            await ctx.send("❌ Categoria inválida! Use: decoracao, badge, cargo, boost ou todos")
            conn.close()
            return
        
        # Busca itens da categoria
        cursor.execute('''
            SELECT id, nome_item, preco, tipo_item, descricao 
            FROM loja 
            WHERE disponivel = 1 AND tipo_item = ?
            ORDER BY preco ASC
        ''', (tipo_filtro,))
        itens = cursor.fetchall()
        conn.close()
        
        if not itens:
            await ctx.send(f"🏪 Não há itens disponíveis nesta categoria no momento!")
            return
        
        emoji_tipo = {
            "decoração": "✨",
            "badge": "🏅",
            "cargo": "👑",
            "boost": "⚡",
            "item": "📦"
        }.get(tipo_filtro, "🎁")
        
        embed = discord.Embed(
            title=f"🏪 Loja - {emoji_tipo} {tipo_filtro.title()}",
            description=f"💰 Suas moedas: **{usuario['moedas']:,}**\n"
                        f"Use `!comprar <ID>` para comprar um item",
            color=discord.Color.green()
        )
        
        for item_id, nome, preco, tipo, desc in itens:
            pode_comprar = "✅" if usuario['moedas'] >= preco else "❌"
            
            embed.add_field(
                name=f"{pode_comprar} {nome} (ID: {item_id})",
                value=f"💰 **{preco:,}** moedas\n"
                      f"📝 {desc}",
                inline=False
            )
        
        embed.set_footer(text="Use !loja para ver todas as categorias")
        await ctx.send(embed=embed)
    
    @commands.command(name='comprar', aliases=['buy'])
    async def comprar(self, ctx, item_id: int):
        """
        Compra um item da loja
        
        Uso: !comprar <ID do item>
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verifica se o item existe e está disponível
        cursor.execute('''
            SELECT nome_item, preco, tipo_item, descricao 
            FROM loja 
            WHERE id = ? AND disponivel = 1
        ''', (item_id,))
        item = cursor.fetchone()
        
        if not item:
            await ctx.send("❌ Item não encontrado ou indisponível!")
            conn.close()
            return
        
        nome_item, preco, tipo_item, descricao = item
        
        # Busca moedas do usuário
        usuario = self._obter_usuario(ctx.author.id, str(ctx.author.name))
        
        if usuario['moedas'] < preco:
            await ctx.send(f"❌ Você não tem moedas suficientes! Você tem **{usuario['moedas']:,}** moedas, mas precisa de **{preco:,}**.")
            conn.close()
            return
        
        # Verifica se já possui o item
        cursor.execute('''
            SELECT quantidade FROM inventario 
            WHERE id_discord = ? AND id_item = ?
        ''', (ctx.author.id, item_id))
        possui = cursor.fetchone()
        
        if possui:
            # Incrementa quantidade
            cursor.execute('''
                UPDATE inventario 
                SET quantidade = quantidade + 1, data_compra = CURRENT_TIMESTAMP
                WHERE id_discord = ? AND id_item = ?
            ''', (ctx.author.id, item_id))
        else:
            # Adiciona ao inventário
            cursor.execute('''
                INSERT INTO inventario (id_discord, id_item, quantidade)
                VALUES (?, ?, 1)
            ''', (ctx.author.id, item_id))
        
        # Deduz moedas
        cursor.execute('''
            UPDATE usuarios 
            SET moedas = moedas - ?
            WHERE id_discord = ?
        ''', (preco, ctx.author.id))
        
        conn.commit()
        conn.close()
        
        # Mensagem de confirmação
        embed = discord.Embed(
            title="✅ Compra Realizada!",
            description=f"Você comprou **{nome_item}**!",
            color=discord.Color.green()
        )
        embed.add_field(name="💰 Preço", value=f"{preco:,} moedas", inline=True)
        embed.add_field(name="💵 Saldo Restante", value=f"{usuario['moedas'] - preco:,} moedas", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='inventario', aliases=['inv', 'inventário', 'bag'])
    async def inventario(self, ctx, membro: discord.Member = None):
        """
        Mostra o inventário de itens
        
        Uso: !inventario [@usuário]
        """
        membro = membro or ctx.author
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca itens do inventário agrupados por tipo
        cursor.execute('''
            SELECT l.tipo_item, l.nome_item, l.preco, i.quantidade, i.data_compra
            FROM inventario i
            JOIN loja l ON i.id_item = l.id
            WHERE i.id_discord = ?
            ORDER BY l.tipo_item, i.data_compra DESC
        ''', (membro.id,))
        itens = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(
            title=f"🎒 Inventário de {membro.display_name}",
            color=membro.color if membro.color != discord.Color.default() else discord.Color.blue()
        )
        
        avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        if not itens:
            embed.description = "Inventário vazio! Visite a loja com `!loja`"
        else:
            # Agrupa itens por categoria
            categorias = {}
            total_valor = 0
            total_itens = 0
            
            for tipo, nome, preco, qtd, data in itens:
                if tipo not in categorias:
                    categorias[tipo] = []
                categorias[tipo].append((nome, preco, qtd))
                total_valor += preco * qtd
                total_itens += qtd
            
            # Exibe estatísticas gerais
            embed.description = f"📦 Total de itens: **{total_itens}**\n💰 Valor total: **{total_valor:,}** moedas"
            
            # Emojis por categoria
            emoji_tipo = {
                "decoração": "✨",
                "badge": "🏅",
                "cargo": "👑",
                "boost": "⚡",
                "item": "📦"
            }
            
            # Exibe itens por categoria
            for tipo, lista_itens in categorias.items():
                emoji = emoji_tipo.get(tipo, "🎁")
                itens_texto = []
                
                for nome, preco, qtd in lista_itens:
                    if qtd > 1:
                        itens_texto.append(f"• **{nome}** x{qtd}")
                    else:
                        itens_texto.append(f"• **{nome}**")
                
                embed.add_field(
                    name=f"{emoji} {tipo.title()} ({len(lista_itens)})",
                    value="\n".join(itens_texto) if itens_texto else "Nenhum",
                    inline=False
                )
        
        embed.set_footer(text="Use !loja para comprar mais itens")
        await ctx.send(embed=embed)
    
    @commands.command(name="addmoedas", aliases=["addcoins", "darmoedas"])
    @commands.is_owner()
    async def addmoedas(self, ctx, membro: discord.Member, quantidade: int):
        """
        Adiciona moedas manualmente a um usuário (apenas fundador)
        
        Uso: !addmoedas @usuário <quantidade>
        """
        if quantidade <= 0:
            await ctx.send("❌ A quantidade de moedas deve ser maior que zero!")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE usuarios 
            SET moedas = moedas + ?
            WHERE id_discord = ?
        ''', (quantidade, membro.id))
        
        conn.commit()
        
        # Busca novo saldo
        usuario = self._obter_usuario(membro.id, str(membro.name))
        conn.close()
        
        embed = discord.Embed(
            title="💰 Moedas Adicionadas",
            description=f"{quantidade:,} moedas foram adicionadas a {membro.mention}",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="💵 Saldo Atual",
            value=f"**{usuario['moedas']:,}** moedas",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="darmoedas", aliases=["givemoedas", "recompensar"])
    @commands.has_permissions(administrator=True)
    async def darmoedas(self, ctx, membro: discord.Member, quantidade: int):
        """
        Dá moedas para um usuário como recompensa (Admin)
        Limite: 10.000 moedas por vez
        
        Uso: !darmoedas @usuário <quantidade>
        Exemplo: !darmoedas @João 500
        """
        # Limite de segurança para administradores
        MAX_MOEDAS_ADMIN = 10000
        
        if quantidade <= 0:
            await ctx.send("❌ A quantidade de moedas deve ser maior que zero!")
            return
        
        if quantidade > MAX_MOEDAS_ADMIN:
            await ctx.send(f"❌ Administradores podem dar no máximo **{MAX_MOEDAS_ADMIN:,}** moedas por vez!\n"
                          f"💡 Use comandos menores ou peça ao fundador para usar `!addmoedas`")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE usuarios 
            SET moedas = moedas + ?
            WHERE id_discord = ?
        ''', (quantidade, membro.id))
        
        conn.commit()
        
        # Busca novo saldo
        usuario = self._obter_usuario(membro.id, str(membro.name))
        conn.close()
        
        embed = discord.Embed(
            title="🎁 Recompensa Entregue",
            description=f"{membro.mention} recebeu **{quantidade:,}** moedas de {ctx.author.mention}!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="💵 Saldo Atual",
            value=f"**{usuario['moedas']:,}** moedas",
            inline=False
        )
        
        embed.set_footer(text=f"Administrador: {ctx.author.name}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="removermoedas", aliases=["removecoins", "tirarmoedas"])
    @commands.is_owner()
    async def removermoedas(self, ctx, membro: discord.Member, quantidade: int):
        """
        Remove moedas manualmente de um usuário (apenas fundador)
        
        Uso: !removermoedas @usuário <quantidade>
        """
        if quantidade <= 0:
            await ctx.send("❌ A quantidade de moedas deve ser maior que zero!")
            return
        
        usuario = self._obter_usuario(membro.id, str(membro.name))
        
        if usuario['moedas'] < quantidade:
            await ctx.send(f"❌ {membro.mention} não tem moedas suficientes! Saldo atual: **{usuario['moedas']:,}** moedas")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE usuarios 
            SET moedas = moedas - ?
            WHERE id_discord = ?
        ''', (quantidade, membro.id))
        
        conn.commit()
        
        # Busca novo saldo
        usuario = self._obter_usuario(membro.id, str(membro.name))
        conn.close()
        
        embed = discord.Embed(
            title="💸 Moedas Removidas",
            description=f"{quantidade:,} moedas foram removidas de {membro.mention}",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="💵 Saldo Atual",
            value=f"**{usuario['moedas']:,}** moedas",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="setmoedas", aliases=["definirmoedas"])
    @commands.is_owner()
    async def setmoedas(self, ctx, membro: discord.Member, quantidade: int):
        """
        Define o saldo de moedas de um usuário (apenas fundador)
        
        Uso: !setmoedas @usuário <quantidade>
        """
        if quantidade < 0:
            await ctx.send("❌ A quantidade de moedas não pode ser negativa!")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE usuarios 
            SET moedas = ?
            WHERE id_discord = ?
        ''', (quantidade, membro.id))
        
        conn.commit()
        conn.close()
        
        embed = discord.Embed(
            title="💰 Saldo Definido",
            description=f"O saldo de {membro.mention} foi definido para **{quantidade:,}** moedas",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @comprar.error
    async def comprar_error(self, ctx, error):
        """Tratamento de erros para o comando comprar"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Você precisa especificar o ID do item! Use: `!comprar <ID>`\n"
                          "💡 Veja os itens disponíveis com `!loja`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ ID inválido! O ID deve ser um número.\n"
                          "💡 Use `!loja` para ver os IDs dos itens")
    
    @addxp.error
    @resetperfil.error
    @addmoedas.error
    @removermoedas.error
    @setmoedas.error
    async def comando_owner_error(self, ctx, error):
        """Tratamento de erros para comandos do fundador"""
        if isinstance(error, commands.NotOwner):
            await ctx.send("❌ Apenas o fundador do bot pode usar este comando!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Usuário não encontrado!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Argumento faltando! Use: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Argumento inválido! Verifique o comando e tente novamente.")
    
    @darmoedas.error
    async def darmoedas_error(self, ctx, error):
        """Tratamento de erros para o comando darmoedas"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Você não tem permissão de administrador!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Usuário não encontrado!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Use: `!darmoedas @usuário <quantidade>`\n"
                          "💡 Exemplo: `!darmoedas @João 500`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Argumento inválido! A quantidade deve ser um número.")

# Setup para carregar o cog
async def setup(bot):
    await bot.add_cog(SistemaNiveis(bot))
