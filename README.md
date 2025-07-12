# 🥗 Scraping Pura Vida

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://selenium-python.readthedocs.io/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-orange.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Sistema automatizado de web scraping para coleta de dados nutricionais de produtos Pura Vida, com interface interativa, coleta incremental e processamento inteligente de dados.

## 📋 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🚀 Instalação](#-instalação)
- [💻 Como Usar](#-como-usar)
- [📊 Estrutura dos Dados](#-estrutura-dos-dados)
- [🛠️ Tecnologias](#️-tecnologias)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🤝 Contribuindo](#-contribuindo)
- [📄 Licença](#-licença)

## ✨ Funcionalidades

### 🎯 Principais Recursos
- **Interface Interativa**: Menu CLI com opções intuitivas e feedback visual
- **Coleta Incremental**: Sistema que permite continuar de onde parou
- **Detecção Automática**: Suporte a múltiplos navegadores (Chrome, Firefox, Edge)
- **Processamento Inteligente**: Extração robusta de dados nutricionais
- **Modo Teste**: Coleta rápida de 10 produtos para validação
- **Exportação Flexível**: Dados salvos em JSON e CSV

### 🔧 Recursos Técnicos
- **Web Scraping Avançado**: Selenium + BeautifulSoup para máxima compatibilidade
- **Tratamento de Erros**: Sistema robusto de recuperação e logging
- **Progresso Visual**: Barras de progresso e estimativas de tempo
- **Deduplicação**: Evita dados duplicados automaticamente
- **Formatação Padrão**: Dados nutricionais padronizados com unidades

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Git

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/sidnei-almeida/scraping_pura_vida.git
cd scraping_pura_vida
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Executando o Programa

```bash
python main.py
```

### Menu Principal

O programa oferece um menu interativo com as seguintes opções:

```
🥗 SCRAPING PURA VIDA - COLETOR DE DADOS NUTRICIONAIS
═══════════════════════════════════════════════════════════

1. 🔍 Coletar URLs dos Produtos
2. 📊 Coletar Dados dos Produtos
3. 🚀 Coleta Completa (URLs + Dados)
4. 🧪 Modo Teste (10 produtos)
5. 📁 Listar Arquivos Gerados
6. 🗑️ Limpar Dados
7. ℹ️ Informações do Programa
8. ❌ Sair

Escolha uma opção: _
```

### Opções Disponíveis

#### 1. 🔍 Coletar URLs dos Produtos
- Coleta URLs de todos os produtos disponíveis
- Salva em `dados/product_urls.json`
- Mostra progresso em tempo real

#### 2. 📊 Coletar Dados dos Produtos
- Extrai dados nutricionais das URLs coletadas
- Salva em `dados/dados_nutricionais.csv`
- Processamento incremental

#### 3. 🚀 Coleta Completa
- Executa coleta de URLs + dados em sequência
- Ideal para primeira execução

#### 4. 🧪 Modo Teste
- Coleta apenas 10 produtos da primeira página
- Salva em `teste.json` e `teste.csv`
- Perfeito para testes rápidos

#### 5. 📁 Listar Arquivos
- Mostra arquivos gerados com tamanhos
- Útil para verificar resultados

#### 6. 🗑️ Limpar Dados
- Remove arquivos de dados
- Limpa cache e logs

## 📊 Estrutura dos Dados

### Dados Nutricionais (CSV)

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| NOME_PRODUTO | Nome do produto | "Pura Fiber - Maçã" |
| CALORIAS (kcal) | Valor energético | 120 |
| PROTEINAS (g) | Proteínas | 15.5 |
| CARBOIDRATOS (g) | Carboidratos totais | 8.2 |
| GORDURAS_TOTAIS (g) | Gorduras totais | 2.1 |
| GORDURAS_SATURADAS (g) | Gorduras saturadas | 0.5 |
| GORDURAS_TRANS (g) | Gorduras trans | 0.0 |
| FIBRAS (g) | Fibras alimentares | 5.8 |
| SODIO (mg) | Sódio | 150 |
| INGREDIENTES | Lista de ingredientes | "Fibras de maçã, vitamina C..." |

### URLs dos Produtos (JSON)

```json
{
  "urls": [
    "https://puravida.com.br/produto/fiber-maca",
    "https://puravida.com.br/produto/whey-protein",
    ...
  ],
  "total_coletadas": 150,
  "data_coleta": "2024-01-15 14:30:00"
}
```

## 🛠️ Tecnologias

### Core
- **Python 3.8+**: Linguagem principal
- **Selenium**: Automação de navegador
- **BeautifulSoup**: Parsing HTML
- **Pandas**: Manipulação de dados

### Interface
- **Rich**: Interface CLI rica e colorida
- **Progress**: Barras de progresso
- **Emojis**: Feedback visual intuitivo

### Utilitários
- **WebDriver Manager**: Gerenciamento automático de drivers
- **JSON/CSV**: Formatos de saída
- **Logging**: Sistema de logs

## 📁 Estrutura do Projeto

```
scraping_pura_vida/
├── 📁 config/
│   ├── browser.py          # Configurações do navegador
│   ├── url_collector.py    # Coletor de URLs
│   └── utils.py            # Utilitários gerais
├── 📁 dados/
│   ├── product_urls.json   # URLs coletadas
│   └── dados_nutricionais.csv  # Dados nutricionais
├── 📁 venv/                # Ambiente virtual
├── 📄 main.py              # Programa principal
├── 📄 template_main.py     # Template de interface
├── 📄 requirements.txt     # Dependências
└── 📄 README.md           # Este arquivo
```

## 🤝 Contribuindo

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### Padrões de Código
- Use **docstrings** para funções
- Mantenha o **design do template_main.py**
- Adicione **emojis** para feedback visual
- Use **type hints** quando possível

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

**Sidnei Almeida**
- 📧 Email: sidnei.almeida1806@gmail.com
- 💼 LinkedIn: [Sidnei Almeida](https://www.linkedin.com/in/saaelmeida93/)
- 🐙 GitHub: [@sidnei-almeida](https://github.com/sidnei-almeida)

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela!**

</div>
