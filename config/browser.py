import os
import platform
import shutil
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from rich.console import Console
from rich.panel import Panel
import traceback

console = Console()

def get_chrome_options(headless: bool = False) -> webdriver.ChromeOptions:
    """
    Configura as opções do Chrome para melhor compatibilidade.
    """
    options = webdriver.ChromeOptions()
    
    # Configurações básicas de compatibilidade
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-features=VizDisplayCompositor')
    
    # Configurações para simular um navegador normal
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    
    # User agent de um navegador normal
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    
    # Remove flags de automação
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications': 2})
    
    # Modo headless se solicitado
    if headless:
        options.add_argument('--headless=new')
    
    return options

def get_firefox_options(headless: bool = False) -> webdriver.FirefoxOptions:
    """
    Configura as opções do Firefox para melhor compatibilidade.
    """
    options = webdriver.FirefoxOptions()
    
    # Configurações básicas
    options.set_preference('browser.tabs.remote.autostart', False)
    options.set_preference('browser.tabs.remote.autostart.2', False)
    
    # Configurações para simular um navegador normal
    options.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0')
    
    # Modo headless se solicitado
    if headless:
        options.add_argument('--headless')
    
    return options

def find_browser_binary(browser_names: list[str]) -> Optional[str]:
    """
    Procura o binário do navegador nos caminhos do sistema.
    """
    for name in browser_names:
        path = shutil.which(name)
        if path:
            console.print(f"[blue]Encontrado binário para {name}: {path}[/blue]")
            return name
    return None

def detect_browsers() -> list[str]:
    """
    Detecta quais navegadores estão instalados no sistema.
    """
    console.print("[yellow]Iniciando detecção de navegadores...[/yellow]")
    console.print(f"Sistema operacional: {platform.system()} {platform.release()}")
    
    sistema = platform.system().lower()
    navegadores_encontrados = []
    
    if sistema == "linux":
        console.print("[yellow]Procurando navegadores no Linux...[/yellow]")
        
        # Chrome/Chromium no Linux
        console.print("Procurando Chrome/Chromium...")
        chrome_binary = find_browser_binary(["google-chrome", "chromium", "chromium-browser"])
        if chrome_binary:
            navegadores_encontrados.append("chrome")
            console.print(f"[green]✓ {chrome_binary} encontrado[/green]")
            
        # Firefox no Linux
        console.print("Procurando Firefox...")
        if find_browser_binary(["firefox"]):
            navegadores_encontrados.append("firefox")
            console.print("[green]✓ Firefox encontrado[/green]")
            
        # Edge no Linux
        console.print("Procurando Edge...")
        if find_browser_binary(["microsoft-edge"]):
            navegadores_encontrados.append("edge")
            console.print("[green]✓ Edge encontrado[/green]")
                    
    elif sistema == "windows":
        console.print("[yellow]Procurando navegadores no Windows...[/yellow]")
        # Caminhos comuns de navegadores no Windows
        program_files = [os.environ.get("PROGRAMFILES", "C:\\Program Files"),
                        os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")]
        
        browsers_windows = {
            "chrome": ["\\Google\\Chrome\\Application\\chrome.exe"],
            "firefox": ["\\Mozilla Firefox\\firefox.exe"],
            "edge": ["\\Microsoft\\Edge\\Application\\msedge.exe"]
        }
        
        for browser, paths in browsers_windows.items():
            console.print(f"Procurando {browser}...")
            for program_path in program_files:
                for path in paths:
                    full_path = program_path + path
                    if os.path.exists(full_path):
                        navegadores_encontrados.append(browser)
                        console.print(f"[green]✓ {browser} encontrado em: {full_path}[/green]")
                        break
    
    return navegadores_encontrados

def setup_driver(browser_preference: Optional[str] = None, headless: bool = False) -> Tuple[webdriver.Remote, str]:
    """
    Configura e retorna o WebDriver apropriado baseado na preferência ou disponibilidade.
    
    Args:
        browser_preference: Navegador preferido ('chrome', 'firefox' ou 'edge')
        headless: Se True, executa o navegador em modo headless
        
    Returns:
        Tuple contendo o driver configurado e o nome do navegador usado
    """
    navegadores_disponiveis = detect_browsers()
    
    if not navegadores_disponiveis:
        raise RuntimeError("Nenhum navegador compatível encontrado no sistema!")
    
    # Se não houver preferência, usa o primeiro navegador disponível
    browser_to_use = browser_preference if browser_preference in navegadores_disponiveis else navegadores_disponiveis[0]
    
    console.print(Panel(f"[green]Configurando driver para: {browser_to_use}[/green]"))
    
    try:
        if browser_to_use == "chrome":
            console.print("Configurando Chrome/Chromium...")
            options = get_chrome_options(headless)
            
            # Detecta o binário do Chrome/Chromium
            chrome_binary = find_browser_binary(["google-chrome", "chromium", "chromium-browser"])
            if chrome_binary:
                binary_path = shutil.which(chrome_binary)
                if binary_path:  # Verifica se binary_path não é None
                    console.print(f"Usando binário: {binary_path}")
                    options.binary_location = binary_path
            
            console.print("Instalando ChromeDriver...")
            try:
                # Tenta instalar o ChromeDriver de forma mais robusta
                driver_path = ChromeDriverManager().install()
                # Verifica se o arquivo é executável
                if not os.path.isfile(driver_path):
                    raise RuntimeError(f"ChromeDriver não encontrado em: {driver_path}")
                if not os.access(driver_path, os.X_OK):
                    console.print("[yellow]Adicionando permissão de execução ao ChromeDriver...[/yellow]")
                    os.chmod(driver_path, 0o755)
                
                console.print(f"ChromeDriver instalado em: {driver_path}")
                service = ChromeService(driver_path)
                console.print("Iniciando Chrome WebDriver...")
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as chrome_error:
                console.print(f"[red]Erro ao configurar ChromeDriver:[/red] {str(chrome_error)}")
                # Tenta limpar a pasta do webdriver_manager
                wdm_path = os.path.expanduser("~/.wdm")
                if os.path.exists(wdm_path):
                    console.print("[yellow]Limpando cache do webdriver_manager...[/yellow]")
                    shutil.rmtree(wdm_path, ignore_errors=True)
                raise
            
        elif browser_to_use == "firefox":
            console.print("Configurando Firefox...")
            options = get_firefox_options(headless)
            
            console.print("Instalando GeckoDriver...")
            service = FirefoxService(GeckoDriverManager().install())
            console.print("Iniciando Firefox WebDriver...")
            driver = webdriver.Firefox(service=service, options=options)
            
        elif browser_to_use == "edge":
            console.print("Configurando Edge...")
            console.print("Instalando EdgeDriver...")
            service = EdgeService(EdgeChromiumDriverManager().install())
            console.print("Iniciando Edge WebDriver...")
            driver = webdriver.Edge(service=service)
            
        else:
            raise ValueError(f"Navegador não suportado: {browser_to_use}")
        
        console.print(f"[green]✓[/green] Driver do {browser_to_use} configurado com sucesso!")
        return driver, browser_to_use
        
    except Exception as e:
        console.print(f"[red]Erro ao configurar o driver para {browser_to_use}:[/red]")
        console.print(f"[red]{str(e)}[/red]")
        console.print("[yellow]Stack trace:[/yellow]")
        console.print(traceback.format_exc())
        
        # Se falhar com o navegador preferido, tenta o próximo disponível
        if browser_preference and len(navegadores_disponiveis) > 1:
            outros_navegadores = [b for b in navegadores_disponiveis if b != browser_preference]
            console.print(f"\n[yellow]Tentando com o próximo navegador disponível: {outros_navegadores[0]}[/yellow]")
            return setup_driver(outros_navegadores[0], headless)
        raise

def get_browser_driver(preferred_browser: Optional[str] = None, headless: bool = False) -> Tuple[webdriver.Remote, str]:
    """
    Função principal para obter um driver de navegador configurado.
    
    Args:
        preferred_browser: Navegador preferido ('chrome', 'firefox' ou 'edge')
        headless: Se True, executa o navegador em modo headless
        
    Returns:
        Tuple contendo o driver configurado e o nome do navegador usado
    """
    console.print("\n[bold]Detectando navegadores instalados...[/bold]")
    navegadores = detect_browsers()
    
    if not navegadores:
        raise RuntimeError("Nenhum navegador compatível encontrado!")
    
    console.print("Navegadores encontrados:", ", ".join(navegadores))
    
    return setup_driver(preferred_browser, headless)

if __name__ == "__main__":
    # Exemplo de uso
    try:
        console.print("[bold yellow]Iniciando teste do WebDriver...[/bold yellow]")
        # Tenta primeiro com Firefox, que geralmente é mais estável no Linux
        driver, browser_name = get_browser_driver("firefox", headless=True)
        console.print(f"\n[green]Teste concluído com sucesso usando {browser_name}![/green]")
        driver.quit()
    except Exception as e:
        console.print(f"\n[red]Erro durante o teste:[/red] {str(e)}")
        console.print("[yellow]Stack trace completo:[/yellow]")
        console.print(traceback.format_exc()) 