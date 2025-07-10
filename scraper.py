import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extract_numeric_value(text):
    """Extrai valor numérico de uma string"""
    try:
        # Remove caracteres não numéricos exceto ponto e vírgula
        value = re.sub(r'[^\d,.]', '', text.replace(',', '.'))
        return float(value) if value else 0
    except:
        return 0

def extract_portion_info(text):
    """Extrai informação de porção do texto"""
    try:
        # Procura especificamente por "Porção: X,X g" no texto completo
        match = re.search(r'Porção:\s*([\d,]+)\s*g', text)
        if match:
            return extract_numeric_value(match.group(1))
        return 0
    except:
        return 0

def get_nutrient_value(table, nutrient_text):
    """Busca o valor de um nutriente específico na tabela usando o texto exato"""
    try:
        # Procura pela célula td que contém exatamente o texto do nutriente
        # e pega o valor da segunda coluna (valor numérico)
        xpath = f"//tbody/tr[td[1][normalize-space()='{nutrient_text}']]/td[2]"
        value_cell = table.find_element(By.XPATH, xpath)
        return extract_numeric_value(value_cell.text)
    except Exception as e:
        print(f"Erro ao buscar nutriente '{nutrient_text}': {str(e)}")
        return 0

def scrape_product(url):
    """Coleta dados nutricionais de um produto"""
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    
    try:
        print(f"\nProcessando URL: {url}")
        driver.get(url)
        print("Aguardando carregamento inicial...")
        time.sleep(5)
        
        # Espera e coleta o nome do produto
        nome_produto = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-name"))
        ).text
        print(f"Nome do produto: {nome_produto}")
        
        # Espera e coleta a categoria
        breadcrumb = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "nav.breadcrumb"))
        )
        breadcrumb_items = breadcrumb.find_elements(By.TAG_NAME, "li")
        categoria = breadcrumb_items[-2].text if len(breadcrumb_items) > 1 else "Categoria não encontrada"
        print(f"Categoria: {categoria}")
        
        # Configura zoom para 50%
        print("Ajustando zoom para 50%...")
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'width': 1920,
            'height': 1080,
            'deviceScaleFactor': 0.5,
            'mobile': False
        })
        time.sleep(2)
        
        print("Procurando tabela nutricional...")
        found = False
        scroll_height = 300
        max_scrolls = 20  # Limite de segurança
        scrolls = 0
        
        while not found and scrolls < max_scrolls:
            # Rola a página
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(1)
            
            # Procura pelo texto específico da tabela
            try:
                tabela = driver.find_element(By.XPATH, "//div[contains(@class, 'tabela_nutricional')]//td[contains(text(), 'Valor energético (kcal)')]")
                if tabela:
                    found = True
                    print("Tabela nutricional encontrada!")
                    # Rola até a tabela e centraliza
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tabela)
                    time.sleep(2)
            except:
                scrolls += 1
                print(f"Rolando... ({scrolls}/{max_scrolls})")
        
        if not found:
            raise Exception("Tabela nutricional não encontrada após rolar a página")
        
        # Agora que encontramos a tabela, vamos coletar os dados
        tabela_div = driver.find_element(By.CSS_SELECTOR, "div.tabela_nutricional")
        
        print("Extraindo informações nutricionais...")
        # Coleta informação de porção
        porcao_text = tabela_div.find_element(By.CLASS_NAME, "porcao").text
        porcao = extract_portion_info(porcao_text)
        print(f"Porção: {porcao}g")
        
        # Coleta dados nutricionais usando os seletores exatos
        table = tabela_div.find_element(By.TAG_NAME, "table")
        
        # Lista de nutrientes exatamente como aparecem na tabela
        nutrientes = [
            "Valor energético (kcal)",
            "Gorduras totais (g)",
            "Gorduras saturadas (g)",
            "Gorduras trans (g)",
            "Ácido hialurônico (mg)",
            "Metilsulfonilmetano (mg)",
            "Coenzima Q10 (mg)",
            "Colágeno de frango com colágeno tipo II não desnaturado (mg)",
            "Colágeno tipo II não desnaturado (mg)"
        ]
        
        # Inicializa dicionário com dados básicos
        dados = {
            'NOME_PRODUTO': nome_produto,
            'URL': url,
            'CATEGORIA': categoria,
            'PORCAO (g)': porcao
        }
        
        # Adiciona os valores nutricionais
        for nutriente in nutrientes:
            print(f"Buscando {nutriente}...")
            valor = get_nutrient_value(table, nutriente)
            nome_coluna = nutriente.split(' (')[0].upper().replace(' ', '_')
            dados[nome_coluna] = valor
            print(f"Encontrado: {nome_coluna}: {valor}")
        
        # Verifica o texto do footer para nutrientes não significativos
        footer_text = tabela_div.find_element(By.CLASS_NAME, "footer_table").text.lower()
        if "não contém quantidades significativas" in footer_text:
            print("Processando nutrientes não significativos do footer...")
            for nutriente in ["CARBOIDRATOS", "ACUCARES_TOTAIS", "ACUCARES_ADICIONADOS", 
                            "PROTEINAS", "FIBRAS_ALIMENTARES", "SODIO"]:
                dados[nutriente] = 0
                print(f"Definido {nutriente}: 0 (conforme footer)")
        
        return dados
        
    except Exception as e:
        print(f"Erro ao processar URL: {str(e)}")
        return None
        
    finally:
        driver.quit()

def setup_driver():
    """Configura o driver do Chrome com as opções necessárias"""
    options = webdriver.ChromeOptions()
    
    # Headers HTTP completos
    options.add_argument('--accept-language=pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
    options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    options.add_argument('--sec-ch-ua="Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"')
    options.add_argument('--sec-ch-ua-platform="Linux"')
    options.add_argument('--sec-ch-ua-mobile=?0')
    options.add_argument('--sec-fetch-dest=document')
    options.add_argument('--sec-fetch-mode=navigate')
    options.add_argument('--sec-fetch-site=none')
    options.add_argument('--sec-fetch-user=?1')
    options.add_argument('--upgrade-insecure-requests=1')
    
    # Configurações para simular um navegador normal
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-infobars')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # User agent de um navegador normal
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    
    # Remove flags de automação
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Configurações adicionais
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,  # Não carrega imagens
            'plugins': 2,  # Desabilita plugins
            'popups': 2,  # Bloqueia popups
            'notifications': 2  # Bloqueia notificações
        }
    }
    options.add_experimental_option('prefs', prefs)
    
    # Inicializa o driver usando o webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Executa JavaScript para ocultar que é automação
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        '''
    })
    
    return driver

if __name__ == "__main__":
    # URL de teste
    test_url = "https://www.puravida.com.br/collagen-flex-beauty-colageno-msm-70312"
    
    # Coleta dados do produto
    dados = scrape_product(test_url)
    
    if dados:
        # Cria DataFrame e salva em CSV
        df = pd.DataFrame([dados])
        df.to_csv('dados/produtos_info.csv', index=False)
        print("\nDados salvos em dados/produtos_info.csv") 