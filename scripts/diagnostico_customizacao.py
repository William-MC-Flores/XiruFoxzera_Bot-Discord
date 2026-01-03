#!/usr/bin/env python3
"""
Script de diagnóstico do sistema de customização
Verifica banners, inventário e itens equipados
"""

import sqlite3
import os
from pathlib import Path

# Caminho para o banco de dados
DB_PATH = "data/niveis.db"
IMAGES_PATH = "images/banners"

def verificar_banners_loja():
    """Verifica se todos os banners na loja têm arquivos correspondentes"""
    print("\n🔍 VERIFICANDO BANNERS NA LOJA\n" + "="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nome_item, arquivo 
        FROM loja 
        WHERE tipo_item = 'banner' AND disponivel = 1
    """)
    banners = cursor.fetchall()
    conn.close()
    
    problemas = []
    
    for banner_id, nome, arquivo in banners:
        caminho = f"images/{arquivo}" if arquivo else None
        
        if not arquivo:
            problemas.append(f"❌ ID {banner_id}: {nome} - SEM ARQUIVO DEFINIDO")
        elif not os.path.exists(caminho):
            problemas.append(f"❌ ID {banner_id}: {nome} - ARQUIVO NÃO EXISTE: {caminho}")
        else:
            print(f"✅ ID {banner_id}: {nome}")
            print(f"   📁 {caminho} ({os.path.getsize(caminho) / 1024 / 1024:.2f} MB)")
    
    if problemas:
        print("\n⚠️  PROBLEMAS ENCONTRADOS:")
        for p in problemas:
            print(p)
    else:
        print("\n✅ Todos os banners estão OK!")
    
    return len(problemas) == 0

def verificar_inventarios():
    """Verifica inventários de usuários"""
    print("\n🔍 VERIFICANDO INVENTÁRIOS\n" + "="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verifica se há itens no inventário que não existem mais na loja
    cursor.execute("""
        SELECT i.id_discord, i.id_item, u.nome
        FROM inventario i
        LEFT JOIN loja l ON i.id_item = l.id
        LEFT JOIN usuarios u ON i.id_discord = u.id_discord
        WHERE l.id IS NULL
    """)
    inventario_invalido = cursor.fetchall()
    
    if inventario_invalido:
        print("⚠️  ITENS ÓRFÃOS NO INVENTÁRIO:")
        for discord_id, item_id, nome in inventario_invalido:
            print(f"   ❌ Usuário {nome} (ID: {discord_id}) tem item ID {item_id} que não existe na loja")
    else:
        print("✅ Todos os inventários estão consistentes!")
    
    # Estatísticas de inventário
    cursor.execute("""
        SELECT COUNT(DISTINCT id_discord) 
        FROM inventario
    """)
    usuarios_com_itens = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM inventario
    """)
    total_itens = cursor.fetchone()[0]
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   👥 Usuários com itens: {usuarios_com_itens}")
    print(f"   📦 Total de itens no inventário: {total_itens}")
    
    conn.close()
    return len(inventario_invalido) == 0

def verificar_perfis_equipados():
    """Verifica itens equipados nos perfis"""
    print("\n🔍 VERIFICANDO ITENS EQUIPADOS\n" + "="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_discord, nome, cor_perfil, banner_perfil, titulo_perfil, item_ativo_borda
        FROM usuarios
        WHERE banner_perfil != '' OR titulo_perfil != '' OR cor_perfil != '#7289DA'
    """)
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("ℹ️  Nenhum usuário com itens equipados")
        conn.close()
        return True
    
    problemas = []
    
    for user_id, nome, cor, banner, titulo, badge in usuarios:
        print(f"\n👤 {nome} (ID: {user_id})")
        
        if cor and cor != '#7289DA':
            print(f"   🎨 Cor: {cor}")
        
        if banner:
            caminho = f"images/{banner}"
            if os.path.exists(caminho):
                print(f"   ✅ Banner: {banner}")
            else:
                problemas.append(f"   ❌ Banner equipado não existe: {banner}")
                print(f"   ❌ Banner: {banner} (ARQUIVO NÃO EXISTE)")
        
        if titulo:
            print(f"   👑 Título: {titulo}")
        
        if badge:
            print(f"   🏅 Badge: {badge}")
    
    if problemas:
        print("\n⚠️  PROBLEMAS ENCONTRADOS:")
        for p in problemas:
            print(p)
    
    conn.close()
    return len(problemas) == 0

def listar_arquivos_banners():
    """Lista todos os arquivos de banners disponíveis"""
    print("\n🔍 ARQUIVOS DE BANNERS DISPONÍVEIS\n" + "="*50)
    
    if not os.path.exists(IMAGES_PATH):
        print(f"❌ Pasta {IMAGES_PATH} não encontrada!")
        return False
    
    arquivos = list(Path(IMAGES_PATH).glob("*.png"))
    
    if not arquivos:
        print("⚠️  Nenhum arquivo PNG encontrado na pasta banners")
        return False
    
    for arquivo in sorted(arquivos):
        tamanho = arquivo.stat().st_size / 1024 / 1024
        print(f"📁 {arquivo.name} ({tamanho:.2f} MB)")
    
    print(f"\n✅ Total: {len(arquivos)} arquivo(s)")
    return True

def corrigir_banners_orfaos():
    """Remove referências a banners que não existem mais"""
    print("\n🔧 CORRIGINDO BANNERS ÓRFÃOS\n" + "="*50)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Busca usuários com banners equipados
    cursor.execute("""
        SELECT id_discord, nome, banner_perfil
        FROM usuarios
        WHERE banner_perfil != ''
    """)
    usuarios = cursor.fetchall()
    
    corrigidos = 0
    
    for user_id, nome, banner in usuarios:
        caminho = f"images/{banner}"
        if not os.path.exists(caminho):
            print(f"🔧 Removendo banner órfão de {nome}: {banner}")
            cursor.execute("""
                UPDATE usuarios
                SET banner_perfil = ''
                WHERE id_discord = ?
            """, (user_id,))
            corrigidos += 1
    
    if corrigidos > 0:
        conn.commit()
        print(f"\n✅ {corrigidos} banner(s) órfão(s) removido(s)")
    else:
        print("✅ Nenhum banner órfão encontrado")
    
    conn.close()
    return corrigidos

def main():
    print("🔍 DIAGNÓSTICO DO SISTEMA DE CUSTOMIZAÇÃO")
    print("="*50)
    
    # Verifica se banco existe
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return
    
    print(f"✅ Banco de dados: {DB_PATH}")
    print(f"📏 Tamanho: {os.path.getsize(DB_PATH) / 1024:.2f} KB")
    
    # Executa verificações
    ok1 = listar_arquivos_banners()
    ok2 = verificar_banners_loja()
    ok3 = verificar_inventarios()
    ok4 = verificar_perfis_equipados()
    
    # Pergunta se quer corrigir
    if not ok4:
        print("\n" + "="*50)
        resposta = input("🔧 Deseja corrigir banners órfãos automaticamente? (s/n): ")
        if resposta.lower() == 's':
            corrigir_banners_orfaos()
    
    # Resumo final
    print("\n" + "="*50)
    print("📋 RESUMO:")
    print(f"   Arquivos de banner: {'✅' if ok1 else '❌'}")
    print(f"   Banners na loja: {'✅' if ok2 else '❌'}")
    print(f"   Inventários: {'✅' if ok3 else '❌'}")
    print(f"   Perfis equipados: {'✅' if ok4 else '❌'}")
    
    if all([ok1, ok2, ok3, ok4]):
        print("\n🎉 SISTEMA 100% FUNCIONAL!")
    else:
        print("\n⚠️  Alguns problemas foram encontrados. Veja acima.")

if __name__ == "__main__":
    main()
