# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o **Xiru Aftonzera Bot**!

## 📋 Como Contribuir

### 1. Reportar Bugs

Se você encontrou um bug, por favor abra uma issue com:
- **Título claro** descrevendo o problema
- **Passos para reproduzir** o bug
- **Comportamento esperado** vs **comportamento atual**
- **Screenshots** (se aplicável)
- **Versão** do Python e discord.py

### 2. Sugerir Melhorias

Para sugestões de recursos:
- Verifique se já não existe uma issue similar
- Descreva **claramente** a funcionalidade proposta
- Explique **por que** essa mudança seria útil

### 3. Contribuir com Código

#### Preparação
```bash
# Clone o repositório
git clone <seu-fork>
cd XiruAftonzera_Bot-Discord

# Crie uma branch para sua feature
git checkout -b feature/minha-feature
```

#### Padrões de Código

**Python:**
- Use **PEP 8** como guia de estilo
- **4 espaços** para indentação
- **Docstrings** em todas as funções/classes
- **Type hints** quando possível

**Commits:**
```
<tipo>: <descrição curta>

[corpo opcional explicando a mudança]

Tipos: feat, fix, docs, style, refactor, test, chore
```

Exemplos:
```
feat: adicionar comando de economia
fix: corrigir bug no sistema de XP
docs: atualizar README com novos comandos
```

#### Testes

Antes de enviar um PR:
```bash
# Teste sintaxe
python3 -m py_compile cogs/*.py

# Teste o bot localmente
python3 main.py
```

#### Enviando Pull Request

1. Atualize a documentação se necessário
2. Certifique-se que o código funciona
3. Faça commit seguindo o padrão
4. Abra um PR descrevendo as mudanças

## 📁 Estrutura do Projeto

```
XiruAftonzera_Bot-Discord/
├── cogs/              # Módulos (comandos e eventos)
├── data/              # Banco de dados
├── images/            # Assets (banners, etc)
├── docs/              # Documentação
│   ├── guias/         # Guias de uso
│   ├── desenvolvimento/ # Docs técnicas
│   └── changelog/     # Histórico de mudanças
├── scripts/           # Scripts utilitários
├── main.py            # Arquivo principal
└── config.py          # Configurações
```

## 🎯 Áreas para Contribuir

- ✨ Novos comandos de diversão
- 🎨 Melhorias no sistema de perfil
- 🏆 Novas conquistas
- 🛡️ Melhorias na moderação
- 📊 Sistema de estatísticas
- 🌐 Tradução/Internacionalização
- 📚 Documentação

## ❓ Dúvidas

Se tiver dúvidas, abra uma **Discussion** ou entre em contato!

---

**Obrigado por contribuir! 🧉**
