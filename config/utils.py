import sys
import time
from datetime import datetime

def print_step(message):
    """Função auxiliar para imprimir mensagens de progresso formatadas"""
    print(f"\n{'='*80}")
    print(f">>> {message}")
    print('='*80)

def print_progress(message):
    """Função auxiliar para imprimir mensagens de progresso menores"""
    print(f"  → {message}")

def create_progress_bar(total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    """
    Cria uma barra de progresso personalizada
    """
    def update(current):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (current / float(total)))
        filled_length = int(length * current // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
        if current == total:
            print()

    return update

def format_time_remaining(seconds):
    """Formata o tempo restante em formato legível"""
    if seconds < 60:
        return f"{seconds:.0f} segundos"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutos"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} horas"

def estimate_time_remaining(current, total, elapsed_time):
    """Estima o tempo restante baseado no progresso atual"""
    if current == 0:
        return "Calculando..."
    
    rate = elapsed_time / current
    remaining_items = total - current
    remaining_time = remaining_items * rate
    
    return format_time_remaining(remaining_time)

def print_collection_status(current, total, item_name, start_time, url=""):
    """Imprime status detalhado da coleta"""
    elapsed = time.time() - start_time
    remaining = estimate_time_remaining(current, total, elapsed)
    percent = (current / total) * 100
    
    print_progress(f"Progresso: {current}/{total} {item_name} ({percent:.1f}%)")
    print_progress(f"Tempo decorrido: {format_time_remaining(elapsed)}")
    print_progress(f"Tempo estimado restante: {remaining}")
    if url:
        print_progress(f"URL atual: {url}")
    
    # Cria e atualiza a barra de progresso
    progress_bar = create_progress_bar(
        total,
        prefix=f'Processando {item_name}:',
        suffix='Completo',
        length=50
    )
    progress_bar(current)

def log_error(error_msg):
    """Registra erros em um arquivo de log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('dados/error_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {error_msg}\n") 