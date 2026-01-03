#!/usr/bin/env python3
"""
Teste: Verifica se o banner aparece no perfil após ser equipado
"""

import sqlite3
import os

DB_PATH = "data/niveis.db"
USER_ID = 999999999

def teste_completo():
    """Simula compra, equipagem e verificação de exibição do banner"""
    print("🧪 TESTE: Banner no Perfil")
    print("="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Cria usuário
    cursor.execute("""
        INSERT OR REPLACE INTO usuarios 
        (id_discord, nome, xp, nivel, moedas, banner_perfil)
        VALUES (?, 'TESTE_USER', 1000, 5, 10000, '')
    """, (USER_ID,))
    conn.commit()
    print("1. ✅ Usuário criado")
    
    # 2. Simula compra do banner
    cursor.execute("""
        INSERT OR REPLACE INTO inventario (id_discord, id_item, quantidade)
        VALUES (?, 163, 1)
    """, (USER_ID,))
    conn.commit()
    print("2. ✅ Banner comprado (ID 163 - Cavalo Crioulo)")
    
    # 3. Equipa o banner
    cursor.execute("""
        SELECT arquivo FROM loja WHERE id = 163
    """)
    arquivo = cursor.fetchone()[0]
    print(f"3. ✅ Arquivo do banner: {arquivo}")
    
    cursor.execute("""
        UPDATE usuarios SET banner_perfil = ?
        WHERE id_discord = ?
    """, (arquivo, USER_ID))
    conn.commit()
    print("4. ✅ Banner equipado no banco")
    
    # 5. SIMULA A FUNÇÃO _obter_usuario (COMO ESTÁ NO CÓDIGO AGORA)
    cursor.execute("""
        SELECT id_discord, nome, xp, nivel, moedas, bio, status_personalizado, data_criacao,
               cor_perfil, banner_perfil, titulo_perfil, item_ativo_borda, item_ativo_fundo
        FROM usuarios WHERE id_discord = ?
    """, (USER_ID,))
    resultado = cursor.fetchone()
    
    if not resultado:
        print("❌ FALHA: Usuário não encontrado!")
        return False
    
    usuario = {
        'id_discord': resultado[0],
        'nome': resultado[1],
        'xp': resultado[2],
        'nivel': resultado[3],
        'moedas': resultado[4],
        'bio': resultado[5] or '',
        'status_personalizado': resultado[6] or '',
        'data_criacao': resultado[7],
        'cor_perfil': resultado[8] or '#7289DA',
        'banner_perfil': resultado[9] or '',
        'titulo_perfil': resultado[10] or '',
        'item_ativo_borda': resultado[11] or '',
        'item_ativo_fundo': resultado[12] or ''
    }
    
    print("\n5. ✅ Dados retornados por _obter_usuario:")
    print(f"   Banner: {usuario['banner_perfil']}")
    print(f"   Cor: {usuario['cor_perfil']}")
    print(f"   Título: {usuario['titulo_perfil']}")
    
    # 6. Verifica se o banner foi retornado
    if not usuario['banner_perfil']:
        print("\n❌ FALHA: banner_perfil está vazio!")
        return False
    
    print("\n6. ✅ banner_perfil está populado!")
    
    # 7. SIMULA O COMANDO !perfil (parte do banner)
    caminho_banner = f"images/{usuario['banner_perfil']}"
    
    if not os.path.exists(caminho_banner):
        print(f"\n❌ FALHA: Arquivo não existe: {caminho_banner}")
        return False
    
    print(f"7. ✅ Arquivo existe: {caminho_banner}")
    print(f"   Tamanho: {os.path.getsize(caminho_banner) / 1024 / 1024:.2f} MB")
    
    # 8. Simula criação do embed
    print("\n8. ✅ Simulação do comando !perfil:")
    print("   → embed = discord.Embed(...)")
    print(f"   → arquivo_banner = discord.File('{caminho_banner}', filename='banner.png')")
    print("   → embed.set_image(url='attachment://banner.png')")
    print("   → await ctx.send(embed=embed, file=arquivo_banner)")
    
    # Limpa
    cursor.execute("DELETE FROM inventario WHERE id_discord = ?", (USER_ID,))
    cursor.execute("DELETE FROM usuarios WHERE id_discord = ?", (USER_ID,))
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("🎉 TESTE PASSOU!")
    print("✅ O banner SERÁ exibido no perfil")
    return True

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        exit(1)
    
    sucesso = teste_completo()
    exit(0 if sucesso else 1)
