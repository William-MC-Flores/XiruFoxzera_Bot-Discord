#!/usr/bin/env python3
"""
Script de testes para validar as implementações do bot
"""
import sqlite3
import os

def test_database_structure():
    """Testa se o banco tem a estrutura correta"""
    print("🔍 Testando estrutura do banco de dados...")
    
    db_path = "data/niveis.db"
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Testa colunas da tabela usuarios
    cursor.execute("PRAGMA table_info(usuarios)")
    colunas = {row[1] for row in cursor.fetchall()}
    
    colunas_esperadas = {
        'id_discord', 'nome', 'xp', 'nivel', 'moedas',
        'bio', 'status_personalizado', 'cor_perfil', 'banner_perfil',
        'titulo_perfil', 'item_ativo_borda', 'item_ativo_fundo',
        'total_mensagens', 'tempo_voz_segundos'
    }
    
    if not colunas_esperadas.issubset(colunas):
        faltando = colunas_esperadas - colunas
        print(f"❌ Colunas faltando em usuarios: {faltando}")
        return False
    
    print("✅ Tabela usuarios OK")
    
    # Testa coluna arquivo na loja
    cursor.execute("PRAGMA table_info(loja)")
    colunas_loja = {row[1] for row in cursor.fetchall()}
    
    if 'arquivo' not in colunas_loja:
        print("❌ Coluna 'arquivo' faltando na tabela loja")
        return False
    
    print("✅ Tabela loja OK")
    
    # Testa conquistas
    cursor.execute("SELECT COUNT(*) FROM conquistas WHERE requisito_tipo = 'voz'")
    if cursor.fetchone()[0] == 0:
        print("❌ Conquista 'Ativo' (tipo voz) não encontrada")
        return False
    
    cursor.execute("SELECT COUNT(*) FROM conquistas WHERE requisito_tipo = 'tempo'")
    if cursor.fetchone()[0] == 0:
        print("❌ Conquista 'Veterano do Servidor' (tipo tempo) não encontrada")
        return False
    
    print("✅ Conquistas OK")
    
    # Testa itens da loja
    cursor.execute("SELECT COUNT(*) FROM loja WHERE tipo_item = 'banner'")
    banners = cursor.fetchone()[0]
    if banners == 0:
        print("❌ Nenhum banner encontrado na loja")
        return False
    
    print(f"✅ {banners} banners encontrados na loja")
    
    cursor.execute("SELECT COUNT(*) FROM loja WHERE tipo_item = 'cor'")
    cores = cursor.fetchone()[0]
    print(f"✅ {cores} cores encontradas na loja")
    
    cursor.execute("SELECT COUNT(*) FROM loja WHERE tipo_item = 'titulo'")
    titulos = cursor.fetchone()[0]
    print(f"✅ {titulos} títulos encontrados na loja")
    
    conn.close()
    return True

def test_banner_files():
    """Testa se os arquivos de banner existem"""
    print("\n🔍 Testando arquivos de banner...")
    
    banners_esperados = [
        'images/banners/espaco.png',
        'images/banners/floresta.png',
        'images/banners/oceano.png',
        'images/banners/montanhas.png',
        'images/banners/cidade.png',
        'images/banners/padrao.png'
    ]
    
    todos_ok = True
    for banner in banners_esperados:
        if os.path.exists(banner):
            tamanho = os.path.getsize(banner)
            print(f"✅ {banner} ({tamanho} bytes)")
        else:
            print(f"❌ {banner} não encontrado!")
            todos_ok = False
    
    return todos_ok

def test_loja_integrity():
    """Testa integridade dos dados da loja"""
    print("\n🔍 Testando integridade da loja...")
    
    conn = sqlite3.connect("data/niveis.db")
    cursor = conn.cursor()
    
    # Verifica se banners têm arquivo associado
    cursor.execute("SELECT nome_item, arquivo FROM loja WHERE tipo_item = 'banner'")
    banners = cursor.fetchall()
    
    todos_ok = True
    for nome, arquivo in banners:
        if not arquivo:
            print(f"❌ Banner '{nome}' sem arquivo associado")
            todos_ok = False
        else:
            caminho_completo = f"images/{arquivo}"
            if os.path.exists(caminho_completo):
                print(f"✅ {nome} → {arquivo}")
            else:
                print(f"⚠️ {nome} → {arquivo} (arquivo não existe ainda)")
    
    conn.close()
    return todos_ok

def test_conquistas():
    """Testa conquistas implementadas"""
    print("\n🔍 Testando conquistas...")
    
    conn = sqlite3.connect("data/niveis.db")
    cursor = conn.cursor()
    
    conquistas_obrigatorias = [
        ("Falador", "mensagens", 1000),
        ("Ativo", "voz", 36000),
        ("Veterano do Servidor", "tempo", 365)
    ]
    
    todos_ok = True
    for nome, tipo, valor in conquistas_obrigatorias:
        cursor.execute(
            "SELECT nome FROM conquistas WHERE requisito_tipo = ? AND requisito_valor = ?",
            (tipo, valor)
        )
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"✅ {nome} ({tipo}, {valor})")
        else:
            print(f"❌ Conquista '{nome}' não encontrada")
            todos_ok = False
    
    conn.close()
    return todos_ok

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTES DE IMPLEMENTAÇÃO - Bot Discord")
    print("=" * 60)
    
    resultados = []
    
    # Teste 1: Estrutura do banco
    resultados.append(("Estrutura do Banco", test_database_structure()))
    
    # Teste 2: Arquivos de banner
    resultados.append(("Arquivos de Banner", test_banner_files()))
    
    # Teste 3: Integridade da loja
    resultados.append(("Integridade da Loja", test_loja_integrity()))
    
    # Teste 4: Conquistas
    resultados.append(("Conquistas", test_conquistas()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    aprovados = sum(1 for _, ok in resultados if ok)
    total = len(resultados)
    
    for nome, ok in resultados:
        status = "✅ PASSOU" if ok else "❌ FALHOU"
        print(f"{status} - {nome}")
    
    print("\n" + "=" * 60)
    print(f"Resultado Final: {aprovados}/{total} testes aprovados")
    
    if aprovados == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        return 0
    else:
        print("⚠️ Alguns testes falharam. Verifique os detalhes acima.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit(main())
