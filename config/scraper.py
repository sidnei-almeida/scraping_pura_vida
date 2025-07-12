#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para extrair informações nutricionais de produtos da Corpo & Vida Suplementos
"""

import os
import sys
import pandas as pd
from bs4 import BeautifulSoup, Tag
from rich.console import Console
from rich.panel import Panel
import re
from typing import List, Optional, Dict, Any

# Adiciona o diretório pai ao path para importar os módulos do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.browser import get_browser_driver

console = Console()

def extract_nutritional_info_liberal(soup: BeautifulSoup, nome: str, categoria: str, url: str) -> Optional[pd.DataFrame]:
    """
    Extrai informações nutricionais de forma mais liberal, procurando por dados
    em qualquer formato dentro do bloco de informações nutricionais.
    """
    df = pd.DataFrame(columns=[
        'NOME_PRODUTO', 'URL', 'CATEGORIA', 'PORCAO (g)', 'CALORIAS (kcal)', 'CARBOIDRATOS (g)',
        'PROTEINAS (g)', 'GORDURAS_TOTAIS (g)', 'GORDURAS_SATURADAS (g)', 'FIBRAS (g)', 'ACUCARES (g)', 'SODIO (mg)'
    ])
    
    # Encontra o bloco de informações nutricionais
    info_div = soup.find('div', {'class': 'bloco_texto', 'id': 'informacoes'})
    if not info_div:
        console.print("[bold red]❌ Não foi possível encontrar o bloco de informações nutricionais")
        return None
    
    # Procura por qualquer texto que contenha "INFORMAÇÃO NUTRICIONAL"
    info_text = info_div.get_text()
    
    # Extrai porção se disponível
    porcao_match = re.search(r'Porção de ([\d,]+\s*g)', info_text)
    porcao = porcao_match.group(1) if porcao_match else "0g"
    
    # Dicionário para armazenar valores nutricionais
    valores = {
        'CALORIAS (kcal)': '0',
        'CARBOIDRATOS (g)': '0',
        'PROTEINAS (g)': '0',
        'GORDURAS_TOTAIS (g)': '0',
        'GORDURAS_SATURADAS (g)': '0',
        'FIBRAS (g)': '0',
        'ACUCARES (g)': '0',
        'SODIO (mg)': '0'
    }
    
    # Procura por dados nutricionais em diferentes formatos
    # 1. Em tabelas HTML
    if isinstance(info_div, Tag):
        tabelas = info_div.find_all('table')
        for tabela in tabelas:
            for row in tabela.find_all('tr'):
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 2:
                    label = cols[0].get_text(strip=True).lower()
                    value = cols[1].get_text(strip=True)
                    
                    # Mapeia diferentes variações de nomes
                    if any(termo in label for termo in ['valor energético', 'calorias', 'energia']):
                        calorias_match = re.search(r'(\d+[\.,]?\d*)', value)
                        if calorias_match and calorias_match.group(1):
                            valores['CALORIAS (kcal)'] = calorias_match.group(1).replace(',', '.')
                    elif any(termo in label for termo in ['carboidratos', 'carboidrato']):
                        carb_match = re.search(r'([\d]+[\.,]?[\d]*)', value)
                        if carb_match and carb_match.group(1):
                            valores['CARBOIDRATOS (g)'] = carb_match.group(1).replace(',', '.')
                    elif any(termo in label for termo in ['proteínas', 'proteína', 'proteinas']):
                        prot_match = re.search(r'([\d]+[\.,]?[\d]*)', value)
                        if prot_match and prot_match.group(1):
                            valores['PROTEINAS (g)'] = prot_match.group(1).replace(',', '.')
                    elif any(termo in label for termo in ['gorduras totais', 'gorduras', 'gorduras totais']):
                        gord_match = re.search(r'([\d]+[\.,]?[\d]*)', value)
                        if gord_match and gord_match.group(1):
                            valores['GORDURAS_TOTAIS (g)'] = gord_match.group(1).replace(',', '.')
                    elif any(termo in label for termo in ['gorduras saturadas', 'gorduras saturadas']):
                        gord_sat_match = re.search(r'([\d]+[\.,]?[\d]*)', value)
                        if gord_sat_match and gord_sat_match.group(1):
                            valores['GORDURAS_SATURADAS (g)'] = gord_sat_match.group(1).replace(',', '.')
                    elif any(termo in label for termo in ['fibra alimentar', 'fibra']):
                        fibra_match = re.search(r'([\d]+[\.,]?[\d]*)', value)
                        if fibra_match and fibra_match.group(1):
                            valores['FIBRAS (g)'] = fibra_match.group(1).replace(',', '.')
                    elif any(termo in label for termo in ['açúcares', 'açucares', 'açúcar', 'açucar']):
                        acucar_match = re.search(r'([\d]+[\.,]?[\d]*)', value)
                        if acucar_match and acucar_match.group(1):
                            valores['ACUCARES (g)'] = acucar_match.group(1).replace(',', '.')
                    elif any(termo in label for termo in ['sódio', 'sodio']):
                        sodio_match = re.search(r'([\d]+[\.,]?[\d]*)', value)
                        if sodio_match and sodio_match.group(1):
                            valores['SODIO (mg)'] = sodio_match.group(1).replace(',', '.')
    
    # 2. Em parágrafos e elementos de texto
    if isinstance(info_div, Tag):
        for elem in info_div.find_all(['p', 'strong', 'span', 'div']):
            texto = elem.get_text(strip=True)
            padroes = [
                (r'valor energético[:\s]*([\d]+[\.,]?[\d]*)\s*kcal', 'CALORIAS (kcal)', 'kcal'),
                (r'carboidratos[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'CARBOIDRATOS (g)', 'g'),
                (r'proteínas[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'PROTEINAS (g)', 'g'),
                (r'gorduras totais[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'GORDURAS_TOTAIS (g)', 'g'),
                (r'gorduras saturadas[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'GORDURAS_SATURADAS (g)', 'g'),
                (r'fibra alimentar[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'FIBRAS (g)', 'g'),
                (r'açúcares[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'ACUCARES (g)', 'g'),
                (r'sódio[:\s]*([\d]+[\.,]?[\d]*)\s*mg', 'SODIO (mg)', 'mg')
            ]
            for padrao, campo, unidade in padroes:
                match = re.search(padrao, texto, re.IGNORECASE)
                if match and match.group(1) and (valores[campo] == f'0 {unidade}' or valores[campo] == f'0{unidade}'):
                    valores[campo] = match.group(1).replace(',', '.') + ' ' + unidade
    
    # 3. Procura por dados em formato de lista ou texto corrido
    texto_completo = info_div.get_text()
    padroes_texto = [
        (r'valor energético[:\s]*([\d]+[\.,]?[\d]*)\s*kcal', 'CALORIAS (kcal)', 'kcal'),
        (r'carboidratos[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'CARBOIDRATOS (g)', 'g'),
        (r'proteínas[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'PROTEINAS (g)', 'g'),
        (r'gorduras totais[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'GORDURAS_TOTAIS (g)', 'g'),
        (r'gorduras saturadas[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'GORDURAS_SATURADAS (g)', 'g'),
        (r'fibra alimentar[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'FIBRAS (g)', 'g'),
        (r'açúcares[:\s]*([\d]+[\.,]?[\d]*)\s*g', 'ACUCARES (g)', 'g'),
        (r'sódio[:\s]*([\d]+[\.,]?[\d]*)\s*mg', 'SODIO (mg)', 'mg')
    ]
    for padrao, campo, unidade in padroes_texto:
        match = re.search(padrao, texto_completo, re.IGNORECASE)
        if match and match.group(1) and (valores[campo] == f'0 {unidade}' or valores[campo] == f'0{unidade}'):
            valores[campo] = match.group(1).replace(',', '.') + ' ' + unidade
    # Garante que nenhum campo fique com vírgula, ponto ou espaço isolado
    for campo, unidade in [('CALORIAS (kcal)', 'kcal'), ('CARBOIDRATOS (g)', 'g'), ('PROTEINAS (g)', 'g'), ('GORDURAS_TOTAIS (g)', 'g'), ('GORDURAS_SATURADAS (g)', 'g'), ('FIBRAS (g)', 'g'), ('ACUCARES (g)', 'g'), ('SODIO (mg)', 'mg')]:
        valor = valores[campo].replace(' ', '')
        if valor in [',', '.', ',g', '.g', ',mg', '.mg', 'g', 'mg', 'kcal', '']:  # Se ficou só unidade ou símbolo
            valores[campo] = f'0{unidade}'
    
    # Cria o registro com os dados encontrados
    dados = {
        'NOME_PRODUTO': nome,
        'URL': url,
        'CATEGORIA': categoria,
        'PORCAO (g)': porcao.replace('g','').replace(',','.') if porcao else '0',
        'CALORIAS (kcal)': valores['CALORIAS (kcal)'],
        'CARBOIDRATOS (g)': valores['CARBOIDRATOS (g)'],
        'PROTEINAS (g)': valores['PROTEINAS (g)'],
        'GORDURAS_TOTAIS (g)': valores['GORDURAS_TOTAIS (g)'],
        'GORDURAS_SATURADAS (g)': valores['GORDURAS_SATURADAS (g)'],
        'FIBRAS (g)': valores['FIBRAS (g)'],
        'ACUCARES (g)': valores['ACUCARES (g)'],
        'SODIO (mg)': valores['SODIO (mg)']
    }
    
    df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
    console.print(f"[bold green]✅ Informações extraídas para {nome}")
    
    return df

def extract_nutritional_info(url: str) -> Optional[pd.DataFrame]:
    """
    Extrai informações nutricionais do produto usando abordagem liberal.
    Retorna um DataFrame com os dados.
    """
    try:
        driver, browser_name = get_browser_driver(headless=True)
        console.print(Panel(f"[bold blue]🔍 Acessando página do produto com {browser_name}"))
        driver.get(url)
        driver.execute_script("document.body.style.zoom='50%'")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        nome_element = soup.find('h1', {'itemprop': 'name'})
        nome = nome_element.text.strip() if nome_element else ''
        categoria_element = soup.find('div', {'itemprop': 'category'})
        categoria = categoria_element.text.strip() if categoria_element else ''

        if not nome:
            console.print("[bold red]❌ Não foi possível encontrar o nome do produto")
            return None

        # Tenta primeiro a abordagem liberal
        df = extract_nutritional_info_liberal(soup, nome, categoria, url)
        
        if df is not None and not df.empty:
            console.print(f"[bold green]✅ Total de {len(df)} produtos processados!")
            return df
        
        # Se não encontrou dados, tenta a abordagem original como fallback
        console.print("[bold yellow]⚠️ Tentando abordagem alternativa...")
        
        info_div = soup.find('div', {'class': 'bloco_texto', 'id': 'informacoes'})
        if not info_div:
            console.print("[bold red]❌ Não foi possível encontrar o bloco de informações nutricionais")
            return None

        df = pd.DataFrame([])
        colunas = [
            'NOME_PRODUTO', 'URL', 'CATEGORIA', 'PORCAO (g)', 'CALORIAS (kcal)', 'CARBOIDRATOS (g)',
            'PROTEINAS (g)', 'GORDURAS_TOTAIS (g)', 'GORDURAS_SATURADAS (g)', 'FIBRAS (g)', 'ACUCARES (g)', 'SODIO (mg)'
        ]
        df = df.reindex(columns=colunas)
        sabor_atual = None
        porcao_atual = None
        if not isinstance(info_div, Tag):
            return None
        for elem in info_div.contents:
            if not isinstance(elem, Tag):
                continue
            texto = elem.get_text(strip=True)
            match_sabor = re.match(r'INFORMAÇÃO NUTRICIONAL\s*[–-]?\s*(.*)', texto, re.IGNORECASE)
            if match_sabor:
                sabor_atual = match_sabor.group(1).strip()
                if not sabor_atual:
                    sabor_atual = None  # Produto sem sabor
                porcao_atual = None
            if sabor_atual is not None and not porcao_atual:
                match_porcao = re.search(r'Porção de ([\d,]+\s*g)', texto)
                if match_porcao:
                    porcao_atual = match_porcao.group(1)
            if sabor_atual is not None and elem.name == 'table':
                valores = {}
                for row in elem.find_all('tr'):
                    if not isinstance(row, Tag):
                        continue
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        label = cols[0].text.strip()
                        value = cols[1].text.strip()
                        if 'Valor Energético' in label:
                            calorias_match = re.search(r'(\d+)\s*kcal', value)
                            if calorias_match:
                                valores['CALORIAS (kcal)'] = calorias_match.group(1)
                        elif 'Carboidratos' in label:
                            carb_match = re.search(r'([\d,]+)', value)
                            if carb_match:
                                valores['CARBOIDRATOS (g)'] = carb_match.group(1)
                        elif 'Proteínas' in label:
                            prot_match = re.search(r'([\d,]+)', value)
                            if prot_match:
                                valores['PROTEINAS (g)'] = prot_match.group(1)
                        elif 'Gorduras Totais' in label:
                            gord_match = re.search(r'([\d,]+)', value)
                            if gord_match:
                                valores['GORDURAS_TOTAIS (g)'] = gord_match.group(1)
                        elif 'Gorduras Saturadas' in label:
                            gord_sat_match = re.search(r'([\d,]+)', value)
                            if gord_sat_match:
                                valores['GORDURAS_SATURADAS (g)'] = gord_sat_match.group(1)
                        elif 'Fibra Alimentar' in label:
                            fibra_match = re.search(r'([\d,]+)', value)
                            if fibra_match:
                                valores['FIBRAS (g)'] = fibra_match.group(1)
                        elif 'Açúcares' in label or 'Açucares' in label:
                            acucar_match = re.search(r'([\d,]+)', value)
                            if acucar_match:
                                valores['ACUCARES (g)'] = acucar_match.group(1)
                        elif 'Sódio' in label:
                            sodio_match = re.search(r'([\d,]+)', value)
                            if sodio_match:
                                valores['SODIO (mg)'] = sodio_match.group(1)
                if sabor_atual:
                    nome_produto = f"{nome} - {sabor_atual}"
                else:
                    nome_produto = nome
                dados = {
                    'NOME_PRODUTO': nome_produto,
                    'URL': f"{url}?sabor={sabor_atual.lower().replace(' ', '-').replace('–','-')}" if sabor_atual else url,
                    'CATEGORIA': categoria,
                    'PORCAO (g)': porcao_atual or "0g",
                    'CALORIAS (kcal)': valores.get('CALORIAS (kcal)', '0'),
                    'CARBOIDRATOS (g)': valores.get('CARBOIDRATOS (g)', '0'),
                    'PROTEINAS (g)': valores.get('PROTEINAS (g)', '0'),
                    'GORDURAS_TOTAIS (g)': valores.get('GORDURAS_TOTAIS (g)', '0'),
                    'GORDURAS_SATURADAS (g)': valores.get('GORDURAS_SATURADAS (g)', '0'),
                    'FIBRAS (g)': valores.get('FIBRAS (g)', '0'),
                    'ACUCARES (g)': valores.get('ACUCARES (g)', '0'),
                    'SODIO (mg)': valores.get('SODIO (mg)', '0')
                }
                df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
                console.print(f"[bold green]✅ Informações extraídas para {nome_produto}")
                sabor_atual = None
        if df.empty:
            console.print("[bold red]❌ Nenhum sabor/tabela encontrado!")
            return None
        console.print(f"[bold green]✅ Total de {len(df)} sabores processados!")
        return df
    except Exception as e:
        console.print(f"[bold red]❌ Erro ao extrair informações: {str(e)}")
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

def save_to_csv(df: pd.DataFrame) -> None:
    """
    Salva o DataFrame em um arquivo CSV, sobrescrevendo o arquivo anterior.
    """
    try:
        csv_file = 'dados/produtos.csv'
        df.to_csv(csv_file, index=False)
        console.print(f"[bold green]✅ Dados salvos em {csv_file}")
        console.print(f"[bold green]✅ Total de {len(df)} produtos no arquivo")
    except Exception as e:
        console.print(f"[bold red]❌ Erro ao salvar CSV: {str(e)}")

if __name__ == "__main__":
    URL = "https://www.corpoevidasuplementos.com.br/whey-protein-isolado-450g-pura-vida"
    df = extract_nutritional_info(URL)
    if df is not None:
        save_to_csv(df) 