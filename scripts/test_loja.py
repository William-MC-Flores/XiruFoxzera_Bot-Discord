#!/usr/bin/env python3
"""
Script de teste para o sistema de loja virtual
"""
import sqlite3
import os

def testar_loja():
    """Testa a estrutura e dados da loja"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'niveis.db')
    
    print("🔍 Testando sistema de loja virtual...\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verifica se a tabela loja existe
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='loja'
        ''')
        if not cursor.fetchone():
            print("❌ Tabela 'loja' não encontrada!")
            return False
        print("✅ Tabela 'loja' existe")
        
        # Verifica se a tabela inventario existe
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='inventario'
        ''')
        if not cursor.fetchone():
            print("❌ Tabela 'inventario' não encontrada!")
            return False
        print("✅ Tabela 'inventario' existe")
        
        # Conta itens na loja
        cursor.execute('SELECT COUNT(*) FROM loja')
        total_itens = cursor.fetchone()[0]
        print(f"✅ Total de itens na loja: {total_itens}")
        
        # Lista itens por categoria
        cursor.execute('''
            SELECT tipo_item, COUNT(*) 
            FROM loja 
            WHERE disponivel = 1
            GROUP BY tipo_item
        ''')
        categorias = cursor.fetchall()
        
        print("\n📦 Itens por categoria:")
        for tipo, qtd in categorias:
            print(f"  • {tipo}: {qtd} itens")
        
        # Lista alguns itens
        cursor.execute('''
            SELECT id, nome_item, preco, tipo_item 
            FROM loja 
            WHERE disponivel = 1
            ORDER BY preco ASC
            LIMIT 5
        ''')
        itens = cursor.fetchall()
        
        print("\n💰 Itens mais baratos:")
        for item_id, nome, preco, tipo in itens:
            print(f"  • ID {item_id}: {nome} ({tipo}) - {preco} moedas")
        
        # Verifica estrutura da tabela loja
        cursor.execute('PRAGMA table_info(loja)')
        colunas = cursor.fetchall()
        print("\n📋 Estrutura da tabela 'loja':")
        for col in colunas:
            print(f"  • {col[1]} ({col[2]})")
        
        # Verifica estrutura da tabela inventario
        cursor.execute('PRAGMA table_info(inventario)')
        colunas = cursor.fetchall()
        print("\n📋 Estrutura da tabela 'inventario':")
        for col in colunas:
            print(f"  • {col[1]} ({col[2]})")
        
        conn.close()
        
        print("\n✅ Todos os testes passaram!")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    testar_loja()
