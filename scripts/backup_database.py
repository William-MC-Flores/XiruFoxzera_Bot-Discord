#!/usr/bin/env python3
"""
Sistema de Backup Automático do Banco de Dados
Mantém backups incrementais para evitar perda de dados
"""
import os
import shutil
import sqlite3
from datetime import datetime
import json

# Configurações
DB_PATH = "data/niveis.db"
BACKUP_DIR = "backups"
MAX_BACKUPS = 30  # Manter últimos 30 backups

def create_backup_dir():
    """Cria diretório de backup se não existir"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✅ Diretório de backup criado: {BACKUP_DIR}")

def backup_database():
    """Cria backup do banco de dados"""
    if not os.path.exists(DB_PATH):
        print(f"⚠️ Banco de dados não encontrado: {DB_PATH}")
        return False
    
    create_backup_dir()
    
    # Nome do backup com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"niveis_backup_{timestamp}.db")
    
    try:
        # Copia o banco de dados
        shutil.copy2(DB_PATH, backup_file)
        
        # Obtém estatísticas
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        stats = {}
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        stats['usuarios'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM loja WHERE disponivel = 1")
        stats['itens_loja'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM conquistas")
        stats['conquistas'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios_conquistas")
        stats['conquistas_desbloqueadas'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM inventario")
        stats['itens_inventario'] = cursor.fetchone()[0]
        
        conn.close()
        
        # Salva metadados
        metadata_file = backup_file.replace('.db', '_info.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'date': datetime.now().isoformat(),
                'statistics': stats,
                'size_bytes': os.path.getsize(backup_file)
            }, f, indent=2, ensure_ascii=False)
        
        size_mb = os.path.getsize(backup_file) / 1024 / 1024
        
        print(f"✅ Backup criado com sucesso!")
        print(f"📁 Arquivo: {backup_file}")
        print(f"📊 Tamanho: {size_mb:.2f} MB")
        print(f"👥 Usuários: {stats['usuarios']}")
        print(f"🏆 Conquistas desbloqueadas: {stats['conquistas_desbloqueadas']}")
        print(f"🛍️ Itens no inventário: {stats['itens_inventario']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return False

def cleanup_old_backups():
    """Remove backups antigos, mantendo apenas os mais recentes"""
    if not os.path.exists(BACKUP_DIR):
        return
    
    # Lista todos os backups
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')]
    backups.sort(reverse=True)  # Mais recente primeiro
    
    # Remove backups antigos
    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[MAX_BACKUPS:]:
            backup_path = os.path.join(BACKUP_DIR, old_backup)
            metadata_path = backup_path.replace('.db', '_info.json')
            
            try:
                os.remove(backup_path)
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)
                print(f"🗑️ Backup antigo removido: {old_backup}")
            except Exception as e:
                print(f"⚠️ Erro ao remover {old_backup}: {e}")

def list_backups():
    """Lista todos os backups disponíveis"""
    if not os.path.exists(BACKUP_DIR):
        print("📂 Nenhum backup encontrado")
        return
    
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')]
    backups.sort(reverse=True)
    
    if not backups:
        print("📂 Nenhum backup encontrado")
        return
    
    print(f"\n📦 {len(backups)} backups disponíveis:\n")
    
    for i, backup in enumerate(backups[:10], 1):  # Mostra últimos 10
        backup_path = os.path.join(BACKUP_DIR, backup)
        metadata_path = backup_path.replace('.db', '_info.json')
        
        size_mb = os.path.getsize(backup_path) / 1024 / 1024
        
        # Tenta ler metadados
        stats_text = ""
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    stats = meta.get('statistics', {})
                    stats_text = f" | 👥 {stats.get('usuarios', 0)} usuários | 🏆 {stats.get('conquistas_desbloqueadas', 0)} conquistas"
            except:
                pass
        
        print(f"{i}. {backup} ({size_mb:.2f} MB){stats_text}")

def restore_backup(backup_file):
    """Restaura um backup específico"""
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup não encontrado: {backup_file}")
        return False
    
    try:
        # Cria backup do banco atual antes de restaurar
        if os.path.exists(DB_PATH):
            emergency_backup = DB_PATH + ".before_restore"
            shutil.copy2(DB_PATH, emergency_backup)
            print(f"💾 Backup de emergência criado: {emergency_backup}")
        
        # Restaura o backup
        shutil.copy2(backup_path, DB_PATH)
        
        print(f"✅ Backup restaurado com sucesso!")
        print(f"📁 Arquivo: {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao restaurar backup: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "backup":
            backup_database()
            cleanup_old_backups()
        elif command == "list":
            list_backups()
        elif command == "restore" and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Comandos disponíveis:")
            print("  python scripts/backup_database.py backup    - Cria novo backup")
            print("  python scripts/backup_database.py list      - Lista backups disponíveis")
            print("  python scripts/backup_database.py restore <arquivo> - Restaura backup")
    else:
        # Comportamento padrão: criar backup
        backup_database()
        cleanup_old_backups()
