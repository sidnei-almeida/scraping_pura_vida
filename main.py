#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌿 SCRAPING PURA VIDA - Interface Bonita
=======================================
Script principal padronizado para scraping incremental dos produtos Pura Vida
"""
import os
import sys
import time
import glob
import json
from datetime import datetime
import pandas as pd
from config.scraper import extract_nutritional_info
from config.url_collector import collect_product_urls

# ================= CORES ANSI =================
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

# =============== UTILITÁRIAS ================
def limpar_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                🌿 SCRAPING PURA VIDA                        ║
║                                                            ║
║    Coleta de Dados Nutricionais de Produtos v1.0           ║
║                                                            ║
║  📊 Extração incremental de produtos e sabores             ║
║  🎯 Exportação incremental para CSV                        ║
║  📝 Visualização e limpeza de arquivos                     ║
╚══════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
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
    menu = f"""
{Cores.AZUL}{Cores.BOLD}══════════════════ MENU PRINCIPAL ═══════════════════{Cores.RESET}

{Cores.VERDE}🚀 OPERAÇÕES:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🔗 {Cores.BRANCO}Coletar URLs dos Produtos{Cores.RESET} - Busca todas as URLs
  {Cores.AMARELO}2.{Cores.RESET} 🌐 {Cores.BRANCO}Coletar Dados de Todas as URLs{Cores.RESET} - Scraping incremental
  {Cores.AMARELO}3.{Cores.RESET} 🎯 {Cores.BRANCO}Coleta Completa (URLs + Dados){Cores.RESET} - Tudo de uma vez
  {Cores.AMARELO}4.{Cores.RESET} 🧪 {Cores.BRANCO}Teste: Coleta de 10 Produtos{Cores.RESET} - Teste rápido

{Cores.VERDE}📁 GERENCIAR DADOS:{Cores.RESET}
  {Cores.AMARELO}5.{Cores.RESET} 📋 {Cores.BRANCO}Ver Arquivos{Cores.RESET} - Lista arquivos gerados
  {Cores.AMARELO}6.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados{Cores.RESET} - Remove arquivos antigos

{Cores.VERDE}ℹ️  INFORMAÇÕES:{Cores.RESET}
  {Cores.AMARELO}7.{Cores.RESET} 📖 {Cores.BRANCO}Sobre o Programa{Cores.RESET} - Informações e estatísticas
  {Cores.AMARELO}8.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET} - Encerrar programa

{Cores.AZUL}══════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (1-8): {Cores.RESET}").strip()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

# ========== FUNÇÕES DO PROJETO =============
def save_incremental(df_novo, csv_file='dados/produtos.csv'):
    if os.path.exists(csv_file):
        df_existente = pd.read_csv(csv_file)
        df_total = pd.concat([df_existente, df_novo], ignore_index=True)
        df_total = df_total.drop_duplicates(subset=['NOME_PRODUTO'], keep='last')
    else:
        df_total = df_novo
    df_total.to_csv(csv_file, index=False)
    return len(df_novo), len(df_total)

def executar_scraping_incremental():
    print(f"\n{Cores.CIANO}{Cores.BOLD}🌐 COLETANDO DADOS DE TODAS AS URLs{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    if not os.path.exists('dados/product_urls.json'):
        print(f"{Cores.VERMELHO}❌ Arquivo de URLs não encontrado!{Cores.RESET}")
        return
    with open('dados/product_urls.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    total_urls = len(urls)
    print(f"\n{Cores.VERDE}🔗 Total de URLs para processar: {total_urls}{Cores.RESET}")
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Iniciar scraping incremental? (s/N): {Cores.RESET}").lower()
    if confirmar not in ['s', 'sim', 'y', 'yes']:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
        return
    mostrar_barra_progresso("Preparando scraping", 1.0)
    inicio = time.time()
    for i, url in enumerate(urls, 1):
        print(f"{Cores.AMARELO}({i}/{total_urls}) {Cores.BRANCO}Processando:{Cores.RESET} {url}")
        df = extract_nutritional_info(url)
        nome_produto = df['NOME_PRODUTO'].iloc[0] if df is not None and not df.empty and 'NOME_PRODUTO' in df.columns else 'Desconhecido'
        if df is not None:
            novos, total = save_incremental(df)
            print(f"{Cores.VERDE}✔ {novos} linhas adicionadas. Total no CSV: {total}{Cores.RESET}")
        else:
            print(f"{Cores.VERMELHO}⚠ Nenhum dado extraído para: {url}{Cores.RESET}")
        # Feedback visual
        perc = (i / total_urls) * 100
        tempo_decorrido = time.time() - inicio
        tempo_restante = (tempo_decorrido / i) * (total_urls - i) if i > 0 else 0
        barra = '█' * int(perc // 2) + '░' * (50 - int(perc // 2))
        print(f"{Cores.CIANO}[{barra}] {perc:.1f}%{Cores.RESET}")
        print(f"{Cores.AZUL}Produto: {Cores.BRANCO}{nome_produto}{Cores.RESET}")
        print(f"{Cores.AMARELO}Restantes: {total_urls - i}{Cores.RESET} | {Cores.VERDE}Tempo decorrido: {tempo_decorrido:.1f}s{Cores.RESET} | {Cores.CIANO}Est. restante: {tempo_restante:.1f}s{Cores.RESET}")
        print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
        time.sleep(0.1)
    print(f"\n{Cores.VERDE}🏁 Coleta finalizada!{Cores.RESET}")

def listar_arquivos_gerados():
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    pasta_dados = "dados"
    extensao = "*.csv"
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
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    pasta_dados = "dados"
    extensao = "*.csv"
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
    print(f"\n{Cores.CIANO}{Cores.BOLD}📖 SOBRE O PROGRAMA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    print(f"\n{Cores.VERDE}🌿 Scraping Pura Vida v1.0{Cores.RESET}")
    print(f"{Cores.BRANCO}Ferramenta para coleta automática de dados nutricionais dos produtos Pura Vida{Cores.RESET}")
    print(f"\n{Cores.VERDE}📊 Funcionalidades:{Cores.RESET}")
    print(f"   • Coleta incremental de dados de múltiplos produtos e sabores")
    print(f"   • Exportação incremental para CSV")
    print(f"   • Interface visual padronizada e amigável")
    print(f"\n{Cores.VERDE}💾 Arquivos gerados:{Cores.RESET}")
    print(f"   • {Cores.AMARELO}dados/product_urls.json{Cores.RESET} - Lista de URLs dos produtos")
    print(f"   • {Cores.AMARELO}dados/produtos.csv{Cores.RESET} - Dados nutricionais extraídos")
    print(f"\n{Cores.VERDE}🛠️  Tecnologias utilizadas:{Cores.RESET}")
    print(f"   • Python 3.x")
    print(f"   • Selenium WebDriver + BeautifulSoup + Pandas")
    print(f"   • Chrome/Firefox em modo headless")
    input(f"\n{Cores.MAGENTA}Pressione ENTER para voltar ao menu...{Cores.RESET}")

def pausar():
    input(f"\n{Cores.MAGENTA}Pressione ENTER para continuar...{Cores.RESET}")

def executar_coleta_urls():
    print(f"\n{Cores.CIANO}{Cores.BOLD}🔗 COLETANDO URLs DOS PRODUTOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Iniciar coleta de URLs? (s/N): {Cores.RESET}").lower()
    if confirmar not in ['s', 'sim', 'y', 'yes']:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
        return
    mostrar_barra_progresso("Preparando coleta de URLs", 1.0)
    try:
        collect_product_urls()
        print(f"{Cores.VERDE}✅ Coleta de URLs concluída!{Cores.RESET}")
    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")

def executar_coleta_completa():
    print(f"\n{Cores.CIANO}{Cores.BOLD}🎯 COLETA COMPLETA (URLs + Dados){Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Iniciar coleta completa? (s/N): {Cores.RESET}").lower()
    if confirmar not in ['s', 'sim', 'y', 'yes']:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
        return
    mostrar_barra_progresso("Coletando URLs", 1.0)
    try:
        collect_product_urls()
        print(f"{Cores.VERDE}✅ URLs coletadas!{Cores.RESET}")
    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao coletar URLs: {e}{Cores.RESET}")
        return
    mostrar_barra_progresso("Coletando dados nutricionais", 1.0)
    executar_scraping_incremental()

def coletar_10_urls_primeira_pagina():
    from config.browser import get_browser_driver
    base_url = "https://www.corpoevidasuplementos.com.br"
    search_url = f"{base_url}/advanced_search_result.php?keywords=Pura%20Vida"
    driver, browser_name = get_browser_driver(headless=True)
    driver.get(search_url)
    import time
    time.sleep(2)
    html = driver.page_source
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('a.produto')
    urls = []
    for link in links:
        href = link.get('href')
        if href and href.startswith(base_url):
            urls.append(href)
        if len(urls) >= 10:
            break
    driver.quit()
    return urls

def executar_teste_10_produtos():
    print(f"\n{Cores.CIANO}{Cores.BOLD}🧪 TESTE: Coleta de 10 Produtos (Primeira Página){Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Iniciar teste de 10 produtos? (s/N): {Cores.RESET}").lower()
    if confirmar not in ['s', 'sim', 'y', 'yes']:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
        return
    mostrar_barra_progresso("Coletando 10 URLs da primeira página", 1.0)
    try:
        urls_teste = coletar_10_urls_primeira_pagina()
        with open('dados/teste.json', 'w', encoding='utf-8') as f:
            json.dump(urls_teste, f, ensure_ascii=False, indent=2)
        print(f"{Cores.VERDE}✅ 10 URLs salvas em dados/teste.json!{Cores.RESET}")
    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao coletar URLs: {e}{Cores.RESET}")
        return
    mostrar_barra_progresso("Coletando dados dos 10 produtos", 1.0)
    import pandas as pd
    df_total = pd.DataFrame()
    for i, url in enumerate(urls_teste, 1):
        print(f"{Cores.AMARELO}({i}/10) {Cores.BRANCO}Processando:{Cores.RESET} {url}")
        df = extract_nutritional_info(url)
        if df is not None:
            df_total = pd.concat([df_total, df], ignore_index=True)
            print(f"{Cores.VERDE}✔ Dados extraídos para a URL!{Cores.RESET}")
        else:
            print(f"{Cores.VERMELHO}⚠ Nenhum dado extraído para: {url}{Cores.RESET}")
        mostrar_barra_progresso(f"Progresso teste: {i}/10", 0.2)
    df_total.to_csv('dados/teste.csv', index=False)
    print(f"\n{Cores.VERDE}🏁 Teste finalizado! Dados salvos em dados/teste.csv{Cores.RESET}")

def main():
    while True:
        limpar_terminal()
        mostrar_banner()
        mostrar_menu()
        escolha = obter_escolha()
        if escolha == '1':
            executar_coleta_urls()
        elif escolha == '2':
            executar_scraping_incremental()
        elif escolha == '3':
            executar_coleta_completa()
        elif escolha == '4':
            executar_teste_10_produtos()
        elif escolha == '5':
            listar_arquivos_gerados()
        elif escolha == '6':
            limpar_dados_antigos()
        elif escolha == '7':
            mostrar_sobre()
        elif escolha == '8':
            print(f"\n{Cores.VERDE}✨ Obrigado por usar o Scraping Pura Vida! Até logo!{Cores.RESET}")
            sys.exit(0)
        else:
            print(f"\n{Cores.VERMELHO}❌ Opção inválida! Tente novamente.{Cores.RESET}")
        pausar()

if __name__ == "__main__":
    main() 