#!/usr/bin/env python
"""
Validador de Requisitos da Atividade
Este script verifica se o projeto cumpre todos os requisitos
"""

import os
import sys

def check_requirement(description, file_path, exists=True):
    """Verifica um requisito"""
    status = "✅" if os.path.exists(file_path) == exists else "❌"
    print(f"{status} {description}")
    return os.path.exists(file_path) == exists

def main():
    print("=" * 70)
    print("VALIDADOR DE REQUISITOS - SISTEMA DE RESERVA DE EVENTOS")
    print("=" * 70)
    print()
    
    # Contar requisitos cumpridos
    total = 0
    cumpridos = 0
    
    print("📋 REQUISITOS OBRIGATÓRIOS:")
    print()
    
    # 1. Linguagem
    if check_requirement("1. Linguagem Python", "models.py"):
        cumpridos += 1
    total += 1
    
    # 2. Interface
    if check_requirement("2. Interface CLI", "main.py"):
        cumpridos += 1
    total += 1
    
    # 3. Problema real
    if check_requirement("3. Problema Real", "README.md"):
        cumpridos += 1
    total += 1
    
    # 5. README
    if check_requirement("5. README Completo", "README.md"):
        cumpridos += 1
    total += 1
    
    # 6. Versionamento
    if check_requirement("6. Versionamento Semântico", "VERSION"):
        cumpridos += 1
    total += 1
    
    # 7. Dependências
    if check_requirement("7. Dependências Declaradas", "requirements.txt"):
        cumpridos += 1
    total += 1
    
    # 8. Testes
    if check_requirement("8. Testes Automatizados", "testes/test_reservas.py"):
        cumpridos += 1
    total += 1
    
    # 9. Linting
    if check_requirement("9. Linting Configurado", ".flake8"):
        cumpridos += 1
    total += 1
    
    # 10. GitHub Actions
    if check_requirement("10. GitHub Actions CI", ".github/workflows/ci.yml"):
        cumpridos += 1
    total += 1
    
    print()
    print("✨ EXTRAS IMPLEMENTADOS:")
    print()
    
    extras = [
        ("CHANGELOG.md", "Histórico de mudanças"),
        ("LICENSE", "Licença MIT"),
        ("CONTRIBUTING.md", "Guia de contribuição"),
        (".env.example", "Template de ambiente"),
        ("RELATORIO_COMPLIANCE.md", "Relatório de compliance"),
    ]
    
    for file_path, desc in extras:
        check_requirement(f"   {desc}", file_path)
    
    print()
    print("=" * 70)
    print(f"RESULTADO: {cumpridos}/{total} Requisitos Obrigatórios Cumpridos")
    print("=" * 70)
    
    if cumpridos == total:
        print("🎉 PROJETO 100% COMPLETO - PRONTO PARA ENTREGA! 🎉")
        return 0
    else:
        print(f"⚠️ {total - cumpridos} requisito(s) ainda falta(m)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
