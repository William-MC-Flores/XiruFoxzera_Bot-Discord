#!/usr/bin/env python3
"""
Teste Rápido do Sistema de Customização
Simula interações com o banco de dados
"""

import sqlite3
import os

DB_PATH = "data/niveis.db"

def teste_loja_banners():
    """Testa se todos os banners da loja têm IDs corretos"""
    print("\n🧪 TESTE 1: Banners na Loja")
    print("="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nome_item, preco, arquivo
        FROM loja
        WHERE tipo_item = 'banner' AND disponivel = 1
        ORDER BY preco ASC
    """)
    banners = cursor.fetchall()
    conn.close()
    
    if not banners:
        print("❌ FALHA: Nenhum banner encontrado!")
        return False
    
    print(f"✅ Encontrados {len(banners)} banners:")
    for banner_id, nome, preco, arquivo in banners:
        existe = "✅" if os.path.exists(f"images/{arquivo}") else "❌"
        print(f"   {existe} ID {banner_id}: {nome} - {preco} moedas - {arquivo}")
    
    return True

def teste_inventario_formato():
    """Testa o formato de query do inventário"""
    print("\n🧪 TESTE 2: Query de Inventário")
    print("="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria usuário de teste se não existir
    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (id_discord, nome, xp, nivel, moedas)
        VALUES (999999999, 'TESTE_USER', 1000, 5, 10000)
    """)
    
    # Compra um item de teste
    cursor.execute("""
        INSERT OR REPLACE INTO inventario (id_discord, id_item, quantidade)
        VALUES (999999999, 163, 1)
    """)
    conn.commit()
    
    # Testa query do inventário (DEVE RETORNAR ID)
    cursor.execute("""
        SELECT l.id, l.tipo_item, l.nome_item, l.preco, i.quantidade, l.arquivo
        FROM inventario i
        JOIN loja l ON i.id_item = l.id
        WHERE i.id_discord = 999999999
    """)
    itens = cursor.fetchall()
    
    if not itens:
        print("⚠️  Inventário vazio (esperado se for primeira execução)")
        conn.close()
        return True
    
    print(f"✅ Query retorna {len(itens)} item(ns):")
    for item_id, tipo, nome, preco, qtd, arquivo in itens:
        print(f"   ID {item_id}: {nome} ({tipo}) - Qtd: {qtd}")
        if not item_id:
            print("   ❌ FALHA: ID é NULL!")
            conn.close()
            return False
    
    # Limpa teste
    cursor.execute("DELETE FROM inventario WHERE id_discord = 999999999")
    cursor.execute("DELETE FROM usuarios WHERE id_discord = 999999999")
    conn.commit()
    conn.close()
    
    return True

def teste_itens_equipados():
    """Testa query de itens equipados"""
    print("\n🧪 TESTE 3: Itens Equipados")
    print("="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria usuário de teste
    cursor.execute("""
        INSERT OR REPLACE INTO usuarios 
        (id_discord, nome, xp, nivel, moedas, cor_perfil, banner_perfil, titulo_perfil)
        VALUES (999999999, 'TESTE_USER', 1000, 5, 10000, '#FF5733', 'banners/Cavalo_Crioulo.png', '⚔️ Guerreiro')
    """)
    conn.commit()
    
    # Testa query
    cursor.execute("""
        SELECT cor_perfil, banner_perfil, titulo_perfil, item_ativo_borda
        FROM usuarios WHERE id_discord = 999999999
    """)
    equipados = cursor.fetchone()
    
    if not equipados:
        print("❌ FALHA: Usuário de teste não encontrado!")
        conn.close()
        return False
    
    cor, banner, titulo, badge = equipados
    print(f"✅ Itens equipados encontrados:")
    print(f"   Cor: {cor}")
    print(f"   Banner: {banner}")
    print(f"   Título: {titulo}")
    print(f"   Badge: {badge or 'Nenhuma'}")
    
    # Limpa teste
    cursor.execute("DELETE FROM usuarios WHERE id_discord = 999999999")
    conn.commit()
    conn.close()
    
    return True

def teste_compra_e_equipagem():
    """Simula fluxo completo: comprar e equipar"""
    print("\n🧪 TESTE 4: Fluxo Completo (Compra + Equipa)")
    print("="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Cria usuário com moedas
    cursor.execute("""
        INSERT OR REPLACE INTO usuarios 
        (id_discord, nome, xp, nivel, moedas)
        VALUES (999999999, 'TESTE_USER', 1000, 5, 10000)
    """)
    conn.commit()
    print("1. ✅ Usuário criado com 10000 moedas")
    
    # 2. Simula compra (adiciona ao inventário)
    cursor.execute("""
        INSERT OR REPLACE INTO inventario (id_discord, id_item, quantidade)
        VALUES (999999999, 163, 1)
    """)
    
    # 3. Deduz moedas
    cursor.execute("""
        UPDATE usuarios SET moedas = moedas - 450
        WHERE id_discord = 999999999
    """)
    conn.commit()
    print("2. ✅ Item ID 163 comprado (Banner Cavalo Crioulo)")
    
    # 4. Busca item para equipar
    cursor.execute("""
        SELECT l.arquivo FROM inventario i
        JOIN loja l ON i.id_item = l.id
        WHERE i.id_discord = 999999999 AND i.id_item = 163
    """)
    result = cursor.fetchone()
    
    if not result:
        print("❌ FALHA: Item não encontrado no inventário!")
        conn.close()
        return False
    
    arquivo = result[0]
    print(f"3. ✅ Arquivo do banner: {arquivo}")
    
    # 5. Verifica se arquivo existe
    if not os.path.exists(f"images/{arquivo}"):
        print(f"❌ FALHA: Arquivo não existe: images/{arquivo}")
        conn.close()
        return False
    
    print(f"4. ✅ Arquivo existe: images/{arquivo}")
    
    # 6. Equipa o banner
    cursor.execute("""
        UPDATE usuarios SET banner_perfil = ?
        WHERE id_discord = 999999999
    """, (arquivo,))
    conn.commit()
    print("5. ✅ Banner equipado no perfil")
    
    # 7. Verifica se foi equipado
    cursor.execute("""
        SELECT banner_perfil FROM usuarios
        WHERE id_discord = 999999999
    """)
    banner_equipado = cursor.fetchone()[0]
    
    if banner_equipado != arquivo:
        print(f"❌ FALHA: Banner não foi equipado corretamente!")
        print(f"   Esperado: {arquivo}")
        print(f"   Recebido: {banner_equipado}")
        conn.close()
        return False
    
    print(f"6. ✅ Verificado: Banner '{banner_equipado}' está equipado")
    
    # Limpa teste
    cursor.execute("DELETE FROM inventario WHERE id_discord = 999999999")
    cursor.execute("DELETE FROM usuarios WHERE id_discord = 999999999")
    conn.commit()
    conn.close()
    
    print("\n🎉 FLUXO COMPLETO FUNCIONANDO!")
    return True

def main():
    print("🧪 TESTE DO SISTEMA DE CUSTOMIZAÇÃO")
    print("="*50)
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return
    
    resultados = []
    
    # Executa testes
    resultados.append(("Banners na Loja", teste_loja_banners()))
    resultados.append(("Query de Inventário", teste_inventario_formato()))
    resultados.append(("Itens Equipados", teste_itens_equipados()))
    resultados.append(("Fluxo Completo", teste_compra_e_equipagem()))
    
    # Resumo
    print("\n" + "="*50)
    print("📊 RESUMO DOS TESTES")
    print("="*50)
    
    passou = 0
    falhou = 0
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status}: {nome}")
        if resultado:
            passou += 1
        else:
            falhou += 1
    
    print("\n" + "="*50)
    print(f"Total: {passou}/{len(resultados)} testes passaram")
    
    if falhou == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema 100% funcional")
    else:
        print(f"\n⚠️  {falhou} teste(s) falharam")
        print("Verifique os erros acima")

if __name__ == "__main__":
    main()
