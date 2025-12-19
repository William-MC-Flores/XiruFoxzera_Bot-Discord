#!/usr/bin/env python3
"""
Script de Verificação do Bot
Verifica se todos os módulos podem ser importados corretamente
"""

import sys
import os
from pathlib import Path

# Define o diretório raiz do projeto (parent do diretório scripts)
PROJETO_ROOT = Path(__file__).parent.parent

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(PROJETO_ROOT))

# Muda para o diretório do projeto
os.chdir(PROJETO_ROOT)

print("🔍 Verificando estrutura do projeto...")
print(f"📁 Diretório: {PROJETO_ROOT}")
print("=" * 50)

# Verifica arquivos essenciais
arquivos_essenciais = [
    'main.py',
    'config.py', 
    'keep_alive.py',
    'data/warns.json',
    'Python/boasvindas.py',
    'Python/cadastro.py',
    'Python/info.py',
    'Python/interacoes.py',
    'Python/logger.py',
    'Python/Logs.py',
    'Python/Moderacao.py',
    'Python/Util.py'
]

missing_files = []
for arquivo in arquivos_essenciais:
    caminho = PROJETO_ROOT / arquivo
    if caminho.exists():
        print(f"✅ {arquivo}")
    else:
        print(f"❌ {arquivo} - NÃO ENCONTRADO")
        missing_files.append(arquivo)

print("=" * 50)

if missing_files:
    print(f"⚠️  {len(missing_files)} arquivo(s) faltando!")
    sys.exit(1)

print("\n🔍 Verificando sintaxe Python...")
print("=" * 50)

# Verifica sintaxe de cada arquivo
import py_compile

erros_sintaxe = []
for arquivo in arquivos_essenciais:
    if arquivo.endswith('.py'):
        try:
            py_compile.compile(arquivo, doraise=True)
            print(f"✅ {arquivo}")
        except py_compile.PyCompileError as e:
            print(f"❌ {arquivo} - ERRO DE SINTAXE")
            erros_sintaxe.append((arquivo, str(e)))

print("=" * 50)

if erros_sintaxe:
    print(f"\n❌ {len(erros_sintaxe)} erro(s) de sintaxe encontrado(s):")
    for arquivo, erro in erros_sintaxe:
        print(f"\n{arquivo}:")
        print(erro)
    sys.exit(1)

print("\n🔍 Verificando configurações...")
print("=" * 50)

try:
    import config
    print(f"✅ GUILD_ID: {config.GUILD_ID}")
    print(f"✅ Canais configurados: {len(config.CANAIS)}")
    print(f"✅ Emojis de cadastro: {len(config.EMOJI_CARGO)}")
    print(f"✅ Cargos de moderação: {len(config.ROLES_MODERACAO)}")
    print(f"✅ Porta keep-alive: {config.KEEP_ALIVE_PORT}")
except Exception as e:
    print(f"❌ Erro ao importar config.py: {e}")
    sys.exit(1)

print("=" * 50)

print("\n🔍 Verificando variáveis de ambiente...")
print("=" * 50)

token = os.getenv("DISCORD_TOKEN")
if token:
    print(f"✅ DISCORD_TOKEN encontrado (comprimento: {len(token)})")
else:
    print("⚠️  DISCORD_TOKEN não configurado")
    print("   Configure a variável de ambiente antes de executar o bot")

print("=" * 50)

print("\n🔍 Resumo da Verificação")
print("=" * 50)
print(f"📁 Arquivos verificados: {len(arquivos_essenciais)}")
print(f"✅ Arquivos OK: {len(arquivos_essenciais) - len(missing_files)}")
print(f"❌ Arquivos faltando: {len(missing_files)}")
print(f"🐍 Erros de sintaxe: {len(erros_sintaxe)}")

if not missing_files and not erros_sintaxe:
    print("\n✅ Projeto está pronto para executar!")
    print("\n📋 Próximos passos:")
    print("1. Configure DISCORD_TOKEN nas variáveis de ambiente")
    print("2. Ajuste os IDs em config.py conforme seu servidor")
    print("3. Execute: python3 main.py")
else:
    print("\n❌ Corrija os erros antes de executar o bot")
    sys.exit(1)

print("=" * 50)
