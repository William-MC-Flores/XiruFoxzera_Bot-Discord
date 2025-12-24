#!/usr/bin/env python3
"""
Script de Teste - Sistema de Níveis e XP
Valida a estrutura e funcionalidade do sistema antes de rodar o bot
"""
import sqlite3
import math
import os

def criar_banco_teste():
    """Cria banco de dados de teste"""
    print("🔧 Criando banco de dados de teste...")
    
    # Remove banco antigo se existir
    if os.path.exists("data/niveis_teste.db"):
        os.remove("data/niveis_teste.db")
    
    conn = sqlite3.connect("data/niveis_teste.db")
    cursor = conn.cursor()
    
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
    print("✅ Banco criado com sucesso!")

def calcular_nivel(xp: int) -> int:
    """Testa cálculo de nível"""
    return math.floor(math.sqrt(xp / 100))

def testar_progressao():
    """Testa progressão de níveis"""
    print("\n📊 Testando progressão de níveis...")
    
    testes = [
        (0, 0),
        (100, 1),
        (400, 2),
        (900, 3),
        (1600, 4),
        (2500, 5),
        (10000, 10),
        (40000, 20),
        (250000, 50),
    ]
    
    erros = 0
    for xp, nivel_esperado in testes:
        nivel_calculado = calcular_nivel(xp)
        status = "✅" if nivel_calculado == nivel_esperado else "❌"
        print(f"{status} {xp:,} XP → Nível {nivel_calculado} (esperado: {nivel_esperado})")
        if nivel_calculado != nivel_esperado:
            erros += 1
    
    if erros == 0:
        print("✅ Todos os testes de progressão passaram!")
    else:
        print(f"❌ {erros} teste(s) falharam!")
    
    return erros == 0

def testar_banco():
    """Testa operações no banco de dados"""
    print("\n🗄️ Testando operações no banco...")
    
    conn = sqlite3.connect("data/niveis_teste.db")
    cursor = conn.cursor()
    
    try:
        # Teste 1: Inserir usuário
        print("  📝 Inserindo usuário de teste...")
        cursor.execute('INSERT INTO usuarios (id_discord, nome, xp, nivel) VALUES (?, ?, ?, ?)',
                      (123456789, "Teste", 500, 2))
        conn.commit()
        print("  ✅ Usuário inserido")
        
        # Teste 2: Buscar usuário
        print("  🔍 Buscando usuário...")
        cursor.execute('SELECT * FROM usuarios WHERE id_discord = ?', (123456789,))
        resultado = cursor.fetchone()
        assert resultado is not None, "Usuário não encontrado"
        assert resultado[1] == "Teste", "Nome incorreto"
        assert resultado[2] == 500, "XP incorreto"
        assert resultado[3] == 2, "Nível incorreto"
        print("  ✅ Usuário encontrado corretamente")
        
        # Teste 3: Atualizar XP
        print("  📈 Atualizando XP...")
        novo_xp = 600
        novo_nivel = calcular_nivel(novo_xp)
        cursor.execute('UPDATE usuarios SET xp = ?, nivel = ? WHERE id_discord = ?',
                      (novo_xp, novo_nivel, 123456789))
        conn.commit()
        
        cursor.execute('SELECT xp, nivel FROM usuarios WHERE id_discord = ?', (123456789,))
        resultado = cursor.fetchone()
        assert resultado[0] == novo_xp, "XP não atualizado"
        assert resultado[1] == novo_nivel, "Nível não atualizado"
        print("  ✅ XP e nível atualizados")
        
        # Teste 4: Ranking
        print("  🏆 Testando ranking...")
        cursor.execute('INSERT INTO usuarios (id_discord, nome, xp, nivel) VALUES (?, ?, ?, ?)',
                      (987654321, "Teste2", 1000, 3))
        cursor.execute('INSERT INTO usuarios (id_discord, nome, xp, nivel) VALUES (?, ?, ?, ?)',
                      (111222333, "Teste3", 2500, 5))
        conn.commit()
        
        cursor.execute('SELECT nome, xp FROM usuarios ORDER BY xp DESC LIMIT 3')
        ranking = cursor.fetchall()
        assert len(ranking) == 3, "Ranking não retornou 3 usuários"
        assert ranking[0][1] >= ranking[1][1] >= ranking[2][1], "Ranking não ordenado"
        print("  ✅ Ranking funcionando")
        
        print("✅ Todos os testes de banco passaram!")
        return True
        
    except AssertionError as e:
        print(f"❌ Teste falhou: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        conn.close()

def testar_formulas():
    """Testa fórmulas matemáticas"""
    print("\n🔢 Testando fórmulas...")
    
    # XP necessário para próximo nível
    def xp_para_nivel(nivel: int) -> int:
        return (nivel ** 2) * 100
    
    testes = [
        (1, 100),
        (2, 400),
        (5, 2500),
        (10, 10000),
    ]
    
    erros = 0
    for nivel, xp_esperado in testes:
        xp_calculado = xp_para_nivel(nivel)
        status = "✅" if xp_calculado == xp_esperado else "❌"
        print(f"{status} Nível {nivel} = {xp_calculado:,} XP (esperado: {xp_esperado:,})")
        if xp_calculado != xp_esperado:
            erros += 1
    
    if erros == 0:
        print("✅ Todas as fórmulas corretas!")
    else:
        print(f"❌ {erros} fórmula(s) incorreta(s)!")
    
    return erros == 0

def verificar_arquivos():
    """Verifica se arquivos necessários existem"""
    print("\n📁 Verificando arquivos...")
    
    arquivos = [
        ("Python/niveis.py", "Módulo de níveis"),
        ("data", "Diretório de dados"),
        ("main.py", "Arquivo principal"),
    ]
    
    erros = 0
    for arquivo, descricao in arquivos:
        existe = os.path.exists(arquivo)
        status = "✅" if existe else "❌"
        print(f"{status} {descricao}: {arquivo}")
        if not existe:
            erros += 1
    
    if erros == 0:
        print("✅ Todos os arquivos encontrados!")
    else:
        print(f"❌ {erros} arquivo(s) faltando!")
    
    return erros == 0

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA DE NÍVEIS E XP")
    print("=" * 60)
    
    # Cria diretório data se não existir
    if not os.path.exists("data"):
        os.makedirs("data")
        print("📁 Diretório 'data' criado")
    
    testes = [
        ("Arquivos", verificar_arquivos),
        ("Banco de Dados", criar_banco_teste),
        ("Progressão", testar_progressao),
        ("Fórmulas", testar_formulas),
        ("Operações no Banco", testar_banco),
    ]
    
    resultados = []
    for nome, funcao in testes:
        try:
            resultado = funcao() if nome != "Banco de Dados" else (funcao(), True)[1]
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro no teste '{nome}': {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    sucesso = 0
    total = len([r for r in resultados if r[1] is not None])
    
    for nome, resultado in resultados:
        if resultado is None:
            continue
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} - {nome}")
        if resultado:
            sucesso += 1
    
    print("=" * 60)
    print(f"📈 Resultado Final: {sucesso}/{total} testes passaram")
    
    if sucesso == total:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso!")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
    
    print("=" * 60)
    
    # Limpa arquivo de teste
    if os.path.exists("data/niveis_teste.db"):
        os.remove("data/niveis_teste.db")
        print("🧹 Arquivo de teste removido")

if __name__ == "__main__":
    main()
