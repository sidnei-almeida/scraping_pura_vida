#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 TEMPLATE MAIN.PY - Interface Bonita Universal
===============================================
Template reutilizável para criar interfaces profissionais em qualquer projeto Python

COMO USAR:
1. Copie este arquivo para seu projeto
2. Substitua os textos em MAIÚSCULO pelos dados do seu projeto
3. Personalize as funções conforme suas necessidades
4. Execute e tenha uma interface linda! ✨
"""

import os
import sys
import time
import glob
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================================
# 🎨 SISTEMA DE CORES ANSI PARA TERMINAL
# ============================================================================
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'
    BRANCO = '\033[97m'

# ============================================================================
# 🛠️ FUNÇÕES UTILITÁRIAS
# ============================================================================
def limpar_terminal():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Exibe o banner principal do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🚀 NOME_DO_SEU_PROJETO                    ║
║                                                              ║
║              DESCRIÇÃO_CURTA_DO_PROJETO v1.0                ║
║                                                              ║
║  📊 FUNCIONALIDADE_PRINCIPAL_1                               ║
║  🎯 FUNCIONALIDADE_PRINCIPAL_2                               ║
║  📝 FUNCIONALIDADE_PRINCIPAL_3                               ║
╚══════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Exibe uma barra de progresso animada"""
    print(f"\n{Cores.AMARELO}⏳ {texto}...{Cores.RESET}")
    barra_tamanho = 40
    for i in range(barra_tamanho + 1):
        progresso = i / barra_tamanho
        barra = "█" * i + "░" * (barra_tamanho - i)
        porcentagem = int(progresso * 100)
        print(f"\r{Cores.VERDE}[{barra}] {porcentagem}%{Cores.RESET}", end="", flush=True)
        time.sleep(duracao / barra_tamanho)
    print()

def mostrar_menu():
    """Exibe o menu principal"""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═══════════════════ MENU PRINCIPAL ═══════════════════{Cores.RESET}

{Cores.VERDE}🚀 OPERAÇÕES PRINCIPAIS:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🧪 {Cores.BRANCO}FUNCAO_1{Cores.RESET} - DESCRIÇÃO_FUNCAO_1
  {Cores.AMARELO}2.{Cores.RESET} 📊 {Cores.BRANCO}FUNCAO_2{Cores.RESET} - DESCRIÇÃO_FUNCAO_2
  {Cores.AMARELO}3.{Cores.RESET} 🎯 {Cores.BRANCO}FUNCAO_3{Cores.RESET} - DESCRIÇÃO_FUNCAO_3

{Cores.VERDE}📁 GERENCIAR DADOS:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 📋 {Cores.BRANCO}Ver Arquivos{Cores.RESET} - Lista arquivos gerados
  {Cores.AMARELO}5.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados{Cores.RESET} - Remove arquivos antigos

{Cores.VERDE}ℹ️  INFORMAÇÕES:{Cores.RESET}
  {Cores.AMARELO}6.{Cores.RESET} 📖 {Cores.BRANCO}Sobre o Programa{Cores.RESET} - Informações e estatísticas
  {Cores.AMARELO}7.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET} - Encerrar programa

{Cores.AZUL}══════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Obtém a escolha do usuário"""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (1-7): {Cores.RESET}").strip()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

# ============================================================================
# 🎯 FUNÇÕES ESPECÍFICAS DO SEU PROJETO
# ============================================================================

def executar_funcao_1():
    """SUBSTITUA: Implementa a primeira funcionalidade principal"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🧪 EXECUTANDO FUNCAO_1{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
    print(f"   📊 Parâmetro 1: {Cores.AMARELO}VALOR_1{Cores.RESET}")
    print(f"   📁 Parâmetro 2: {Cores.AMARELO}VALOR_2{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Executando FUNCAO_1", 2.0)
            
            # SUBSTITUA: Coloque aqui a lógica da sua função
            print(f"{Cores.VERDE}🚀 Processando...{Cores.RESET}")
            time.sleep(1)  # Simula processamento
            print(f"{Cores.VERDE}✅ FUNCAO_1 executada com sucesso!{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_funcao_2():
    """SUBSTITUA: Implementa a segunda funcionalidade principal"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📊 EXECUTANDO FUNCAO_2{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Esta operação pode demorar {Cores.VERMELHO}alguns minutos{Cores.RESET}")
    print(f"   • DESCRIÇÃO_DE_CUIDADOS_ESPECIAIS")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Preparando FUNCAO_2", 1.5)
            
            # SUBSTITUA: Coloque aqui a lógica da sua função
            print(f"{Cores.VERDE}🚀 Processando...{Cores.RESET}")
            time.sleep(2)  # Simula processamento
            print(f"{Cores.VERDE}✅ FUNCAO_2 concluída!{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_funcao_3():
    """SUBSTITUA: Implementa a terceira funcionalidade principal"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🎯 EXECUTANDO FUNCAO_3{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    try:
        # SUBSTITUA: Exemplo de input personalizado
        parametro = input(f"\n{Cores.MAGENTA}📊 Digite um parâmetro: {Cores.RESET}").strip()
        
        if not parametro:
            print(f"{Cores.VERMELHO}❌ Parâmetro obrigatório!{Cores.RESET}")
            return
            
        print(f"\n{Cores.VERDE}✅ Processando com parâmetro: {Cores.AMARELO}{parametro}{Cores.RESET}")
        
        # SUBSTITUA: Coloque aqui a lógica da sua função
        mostrar_barra_progresso("Executando FUNCAO_3", 1.0)
        print(f"{Cores.VERDE}✅ FUNCAO_3 concluída!{Cores.RESET}")
        
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro: {e}{Cores.RESET}")

def listar_arquivos_gerados():
    """Lista arquivos gerados pelo programa"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # SUBSTITUA: Ajuste a pasta e extensão conforme seu projeto
    pasta_dados = "PASTA_DE_SAIDA"  # Ex: "dados", "output", "results"
    extensao = "EXTENSAO_ARQUIVO"    # Ex: "*.csv", "*.json", "*.txt"
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    arquivos = glob.glob(f"{pasta_dados}/{extensao}")
    
    if not arquivos:
        print(f"{Cores.AMARELO}📄 Nenhum arquivo encontrado em '{pasta_dados}'{Cores.RESET}")
        return
    
    print(f"\n{Cores.VERDE}📊 Total de arquivos: {len(arquivos)}{Cores.RESET}\n")
    
    for i, arquivo in enumerate(sorted(arquivos, reverse=True), 1):
        nome_arquivo = os.path.basename(arquivo)
        tamanho = os.path.getsize(arquivo)
        data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
        
        # Calcula o tamanho em formato legível
        if tamanho < 1024:
            tamanho_str = f"{tamanho} B"
        elif tamanho < 1024 * 1024:
            tamanho_str = f"{tamanho / 1024:.1f} KB"
        else:
            tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
        
        print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
        print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"     📏 {tamanho_str}")
        print()

def limpar_dados_antigos():
    """Remove arquivos antigos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # SUBSTITUA: Ajuste conforme seu projeto
    pasta_dados = "PASTA_DE_SAIDA"
    extensao = "EXTENSAO_ARQUIVO"
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    arquivos = glob.glob(f"{pasta_dados}/{extensao}")
    
    if not arquivos:
        print(f"{Cores.VERDE}✅ Nenhum arquivo para limpar{Cores.RESET}")
        return
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Serão removidos {Cores.VERMELHO}{len(arquivos)} arquivos{Cores.RESET}")
    print(f"   • Esta ação {Cores.VERMELHO}NÃO PODE ser desfeita{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza? Digite 'CONFIRMAR' para prosseguir: {Cores.RESET}")
    
    if confirmar == "CONFIRMAR":
        try:
            for arquivo in arquivos:
                os.remove(arquivo)
            print(f"\n{Cores.VERDE}✅ {len(arquivos)} arquivos removidos com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro ao remover arquivos: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def mostrar_sobre():
    """Exibe informações sobre o programa"""
    sobre = f"""
{Cores.CIANO}{Cores.BOLD}📖 SOBRE O SEU_PROJETO{Cores.RESET}
{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}

{Cores.VERDE}🎯 OBJETIVO:{Cores.RESET}
   DESCRIÇÃO_DETALHADA_DO_OBJETIVO_DO_PROJETO

{Cores.VERDE}📊 FUNCIONALIDADES:{Cores.RESET}
   • FUNCIONALIDADE_1
   • FUNCIONALIDADE_2  
   • FUNCIONALIDADE_3

{Cores.VERDE}🛠️  TECNOLOGIAS:{Cores.RESET}
   • Python 3.8+
   • BIBLIOTECA_1
   • BIBLIOTECA_2
   • BIBLIOTECA_3

{Cores.VERDE}📂 ARQUIVOS GERADOS:{Cores.RESET}
   • Formato: FORMATO_SAIDA
   • Localização: PASTA_SAIDA/
   • Nomenclatura: PADRAO_NOMENCLATURA

{Cores.VERDE}⚡ CARACTERÍSTICAS:{Cores.RESET}
   • CARACTERISTICA_1
   • CARACTERISTICA_2
   • CARACTERISTICA_3

{Cores.VERDE}📝 DESENVOLVIDO POR:{Cores.RESET}
   • SEU_NOME
   • Versão: 1.0
   • Data: {datetime.now().strftime('%B %Y')}

{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}
"""
    print(sobre)

def pausar():
    """Pausa o programa aguardando input do usuário"""
    input(f"\n{Cores.CIANO}⏯️  Pressione Enter para continuar...{Cores.RESET}")

# ============================================================================
# 🚀 FUNÇÃO PRINCIPAL
# ============================================================================
def main():
    """Função principal do programa"""
    try:
        while True:
            limpar_terminal()
            mostrar_banner()
            mostrar_menu()
            
            escolha = obter_escolha()
            
            if escolha == "1":
                executar_funcao_1()
                pausar()
                
            elif escolha == "2":
                executar_funcao_2()
                pausar()
                
            elif escolha == "3":
                executar_funcao_3()
                pausar()
                
            elif escolha == "4":
                listar_arquivos_gerados()
                pausar()
                
            elif escolha == "5":
                limpar_dados_antigos()
                pausar()
                
            elif escolha == "6":
                mostrar_sobre()
                pausar()
                
            elif escolha == "7":
                print(f"\n{Cores.VERDE}👋 Obrigado por usar o SEU_PROJETO!{Cores.RESET}")
                print(f"{Cores.CIANO}🚀 Até a próxima!{Cores.RESET}\n")
                break
                
            else:
                print(f"\n{Cores.VERMELHO}❌ Opção inválida! Por favor, escolha entre 1-7{Cores.RESET}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Programa encerrado pelo usuário. Até logo!{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}")

if __name__ == "__main__":
    main() 