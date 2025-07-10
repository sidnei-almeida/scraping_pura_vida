from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
import os
import time

def print_step(message):
    """Função auxiliar para imprimir mensagens de progresso formatadas"""
    print(f"\n{'='*80}")
    print(f">>> {message}")
    print('='*80)

def print_progress(message):
    """Função auxiliar para imprimir mensagens de progresso menores"""
    print(f"  → {message}")

def setup_driver():
    """Configura o driver do Chrome com as opções necessárias"""
    print_progress("Iniciando configuração do navegador Chrome (modo headless)...")
    options = webdriver.ChromeOptions()
    
    # Configurações para modo headless
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Configurações para simular um navegador normal
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    
    # User agent de um navegador normal
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    
    # Remove a flag que indica automação
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    
    # Remove o flag navigator.webdriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print_progress("Configurando zoom para 50%...")
    # Configura o zoom para 50%
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 1920,
        'height': 1080,
        'deviceScaleFactor': 0.5,
        'mobile': False
    })
    
    print_progress("Navegador configurado com sucesso!")
    return driver

def scroll_to_bottom(driver, sleep_time=1):
    """Rola a página até o final para carregar todos os produtos"""
    print_step("Iniciando processo de rolagem da página")
    last_height = driver.execute_script("return document.body.scrollHeight")
    total_scrolls = 0
    
    while True:
        total_scrolls += 1
        # Rola até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Espera o carregamento
        time.sleep(sleep_time)
        
        # Calcula a nova altura da página
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Se a altura não mudou, chegamos ao final
        if new_height == last_height:
            print_progress(f"Rolagem concluída após {total_scrolls} iterações!")
            break
            
        last_height = new_height
        print_progress(f"Rolagem #{total_scrolls} - Altura atual: {new_height}px")

def collect_product_urls():
    """Coleta as URLs dos produtos da Pura Vida"""
    print_step("Iniciando coleta de URLs dos produtos Pura Vida")
    
    base_url = "https://www.puravida.com.br"
    products_page = f"{base_url}/todos"
    
    print_progress(f"URL alvo: {products_page}")
    
    driver = setup_driver()
    
    try:
        print_step("Acessando página de produtos")
        # Acessa a página de produtos
        driver.get(products_page)
        
        print_progress("Aguardando carregamento inicial dos produtos...")
        # Espera os elementos de produto carregarem
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "spot-product-info"))
        )
        
        # Rola a página para carregar todos os produtos
        scroll_to_bottom(driver)
        
        print_step("Coletando URLs dos produtos")
        # Espera um pouco para garantir que tudo carregou
        time.sleep(2)
        
        # Coleta todos os links de produtos
        print_progress("Buscando elementos na página...")
        product_links = driver.find_elements(By.CSS_SELECTOR, "a.spot-product-info")
        total_links = len(product_links)
        print_progress(f"Encontrados {total_links} produtos para processar")
        
        # Extrai e formata as URLs
        print_progress("Extraindo URLs...")
        product_urls = []
        for i, link in enumerate(product_links, 1):
            href = link.get_attribute('href')
            if href and href.startswith(f"{base_url}/"):
                product_urls.append(href)
                if i % 20 == 0:  # Feedback a cada 20 produtos
                    print_progress(f"Processados {i}/{total_links} produtos...")
        
        # Cria o diretório dados se não existir
        print_step("Salvando resultados")
        print_progress("Verificando diretório de dados...")
        os.makedirs('../dados', exist_ok=True)
        
        # Salva apenas a lista de URLs em um arquivo JSON
        output_file = '../dados/product_urls.json'
        
        print_progress(f"Salvando {len(product_urls)} URLs no arquivo: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(product_urls, f, ensure_ascii=False, indent=2)
            
        print_step("Coleta finalizada com sucesso!")
        print_progress(f"Total de URLs coletadas: {len(product_urls)}")
        print_progress(f"Arquivo salvo em: {output_file}")
        print('='*80)
        
    except Exception as e:
        print_step("ERRO DURANTE A EXECUÇÃO!")
        print_progress(f"Detalhes do erro: {str(e)}")
    
    finally:
        print_progress("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    start_time = time.time()
    collect_product_urls()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nTempo total de execução: {execution_time:.2f} segundos") 