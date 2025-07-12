from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os
from .browser import get_browser_driver
from .utils import print_step, print_progress, print_collection_status, log_error

def setup_driver():
    """Configura o driver do Chrome com as opções necessárias"""
    print_progress("Iniciando configuração do navegador (modo headless)...")
    
    # Obtém o driver do módulo browser.py com modo headless ativado
    driver, browser_name = get_browser_driver(headless=True)
    print_progress(f"Usando navegador: {browser_name}")
    
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

def collect_product_urls():
    """Coleta as URLs dos produtos da Pura Vida"""
    start_time = time.time()
    print_step("Iniciando coleta de URLs dos produtos Pura Vida")
    
    # Cria o diretório dados se não existir
    print_step("Verificando diretório de dados")
    print_progress("Criando diretório 'dados' se não existir...")
    os.makedirs('dados', exist_ok=True)
    
    # Inicializa o arquivo JSON vazio se não existir
    output_file = 'dados/product_urls.json'
    if not os.path.exists(output_file):
        print_progress("Criando arquivo JSON vazio...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    base_url = "https://www.corpoevidasuplementos.com.br"
    search_url = f"{base_url}/advanced_search_result.php?keywords=Pura%20Vida"
    
    print_progress(f"URL base: {search_url}")
    
    driver = setup_driver()
    all_product_urls = []
    current_page = 1
    has_more_pages = True
    
    try:
        while has_more_pages:
            # Constrói a URL da página atual
            page_url = f"{search_url}&page={current_page}" if current_page > 1 else search_url
            print_step(f"Processando página {current_page}")
            print_progress(f"URL: {page_url}")
            
            # Acessa a página
            driver.get(page_url)
            time.sleep(2)  # Espera o carregamento inicial
            
            # Espera os produtos carregarem
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.produto"))
                )
            except:
                print_progress("Nenhum produto encontrado nesta página. Finalizando coleta...")
                has_more_pages = False
                break
            
            # Coleta os links dos produtos
            product_links = driver.find_elements(By.CSS_SELECTOR, "a.produto")
            
            # Se não encontrou produtos, termina a coleta
            if not product_links:
                print_progress("Nenhum produto encontrado nesta página. Finalizando coleta...")
                has_more_pages = False
                break
            
            # Extrai e formata as URLs
            page_urls = []
            for i, link in enumerate(product_links, 1):
                href = link.get_attribute('href')
                try:
                    product_name = link.find_element(By.CSS_SELECTOR, "span.nome").text.strip()
                except:
                    product_name = "Nome não encontrado"
                
                if href and href.startswith(base_url):
                    page_urls.append(href)
                    print_collection_status(
                        i, 
                        len(product_links),
                        f"produtos na página {current_page}",
                        start_time,
                        f"Produto: {product_name}"
                    )
            
            # Adiciona as URLs desta página à lista geral
            all_product_urls.extend(page_urls)
            print_progress(f"Coletados {len(page_urls)} produtos na página {current_page}")
            
            # Avança para a próxima página
            current_page += 1
        
        # Remove URLs duplicadas
        all_product_urls = list(set(all_product_urls))
        
        # Salva apenas a lista de URLs em um arquivo JSON
        print_step("Salvando resultados")
        print_progress(f"Salvando {len(all_product_urls)} URLs únicas no arquivo: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_product_urls, f, ensure_ascii=False, indent=2)
            
        print_step("Coleta finalizada com sucesso!")
        print_progress(f"Total de páginas processadas: {current_page - 1}")
        print_progress(f"Total de URLs únicas coletadas: {len(all_product_urls)}")
        print_progress(f"Arquivo salvo em: {output_file}")
        print_progress(f"Tempo total de execução: {time.time() - start_time:.1f} segundos")
        print('='*80)
        
    except Exception as e:
        error_msg = f"ERRO DURANTE A EXECUÇÃO: {str(e)}"
        print_step(error_msg)
        log_error(error_msg)
    
    finally:
        print_progress("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    collect_product_urls() 