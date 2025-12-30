#!/usr/bin/env python3
"""
Script para inicializar o banco de dados da loja virtual
Este script deve ser executado antes de usar o bot pela primeira vez
"""
import sqlite3
import os

def inicializar_banco():
    """Inicializa as tabelas do banco de dados"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'niveis.db')
    
    print("🔧 Inicializando banco de dados...\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Cria tabela de usuários
        print("📦 Criando tabela 'usuarios'...")
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
        print("✅ Tabela 'usuarios' criada")
        
        # Cria tabela de conquistas
        print("📦 Criando tabela 'conquistas'...")
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
        print("✅ Tabela 'conquistas' criada")
        
        # Cria tabela de conquistas dos usuários
        print("📦 Criando tabela 'usuarios_conquistas'...")
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
        print("✅ Tabela 'usuarios_conquistas' criada")
        
        # Cria tabela de loja
        print("📦 Criando tabela 'loja'...")
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
        print("✅ Tabela 'loja' criada")
        
        # Cria tabela de inventário
        print("📦 Criando tabela 'inventario'...")
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
        print("✅ Tabela 'inventario' criada")
        
        # Adiciona colunas se necessário
        print("\n🔧 Verificando colunas adicionais...")
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN moedas INTEGER DEFAULT 0")
            print("✅ Coluna 'moedas' adicionada")
        except sqlite3.OperationalError:
            print("ℹ️  Coluna 'moedas' já existe")
        
        # Insere conquistas padrão
        print("\n🏆 Inserindo conquistas padrão...")
        conquistas_padrao = [
            ("Primeira Mensagem", "Enviou sua primeira mensagem!", "👋", "mensagens", 1),
            ("Tagarela", "Enviou 100 mensagens", "💬", "mensagens", 100),
            ("Comunicador", "Enviou 1000 mensagens", "🗣️", "mensagens", 1000),
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
        print(f"✅ {len(conquistas_padrao)} conquistas inseridas")
        
        # Insere itens da loja
        print("\n🏪 Inserindo itens da loja...")
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
        print(f"✅ {len(itens_padrao)} itens inseridos na loja")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Banco de dados inicializado com sucesso!")
        print("🎉 Você já pode usar o bot!")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    inicializar_banco()
