#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para salvar o HTML da página mantendo a codificação ISO-8859-1 original
"""

import os
import sys
from typing import Optional
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from rich.console import Console
from rich.panel import Panel

# Adiciona o diretório pai ao path para importar os módulos do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.browser import get_browser_driver

console = Console()

def save_html(url: str, output_file: str = 'debug/page.html') -> Optional[str]:
    """
    Salva o HTML da página mantendo a codificação ISO-8859-1 original
    """
    console.print(Panel("[bold blue]🔍 Salvando HTML da página[/bold blue]"))
    
    try:
        # Obtém o driver em modo headless
        console.print("[yellow]Iniciando navegador...[/yellow]")
        driver, browser_name = get_browser_driver(headless=True)
        console.print(f"[green]✓[/green] Usando navegador: {browser_name}")
        
        # Configura zoom para 50%
        console.print("[yellow]Configurando zoom para 50%...[/yellow]")
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 1920,
            'height': 1080,
            'deviceScaleFactor': 0.5,
            'mobile': False
        })
        
        # Acessa a URL
        console.print(f"\n[yellow]Acessando URL:[/yellow] {url}")
        driver.get(url)
        
        # Espera a página carregar
        console.print("[yellow]Aguardando carregamento da página...[/yellow]")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bloco_texto"))
        )
        
        # Obtém o HTML da página
        html_content = driver.page_source
        
        # Cria o diretório debug se não existir
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Salva o HTML mantendo a codificação ISO-8859-1
        try:
            with open(output_file, 'w', encoding='iso-8859-1', errors='ignore') as f:
                f.write(html_content)
            console.print(f"[green]✓ HTML salvo com codificação ISO-8859-1:[/green] {output_file}")
            
            # Lê o início do arquivo para verificar
            with open(output_file, 'r', encoding='iso-8859-1') as f:
                inicio = f.read(500)
                console.print("\n[yellow]Primeiros 500 caracteres do arquivo salvo:[/yellow]")
                console.print(inicio)
                
        except Exception as e:
            console.print(f"[red]❌ Erro ao salvar arquivo:[/red] {str(e)}")
        
        return html_content
        
    except Exception as e:
        console.print(f"[red]❌ Erro ao salvar HTML:[/red] {str(e)}")
        import traceback
        console.print("[red]Stack trace:[/red]")
        console.print(traceback.format_exc())
        return None
        
    finally:
        console.print("\n[yellow]Fechando navegador...[/yellow]")
        driver.quit()
        console.print("[green]✓ Navegador fechado[/green]")

if __name__ == "__main__":
    URL = "https://www.corpoevidasuplementos.com.br/whey-protein-isolado-450g-pura-vida"
    save_html(URL) 