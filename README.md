# 🃏 Magic Preço Médio: Automação de Precificação & Scraping

[![GitHub release](https://img.shields.io/github/release/alan-vieira/preco_magic_card.svg)](https://github.com/alan-vieira/preco_magic_card/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> Sistema de inteligência de mercado para precificação de cartas de Magic: The Gathering

---

## 📖 Visão Geral

Este projeto automatiza a coleta de preços médios de cartas de **Magic: The Gathering** no site **LigaMagic** e processa esses dados para gerar uma estratégia de precificação competitiva no **Mercado Livre**, considerando automaticamente as taxas de comissão da plataforma.

### 🎯 Objetivo

- Extrair preços de referência do mercado brasileiro (LigaMagic)
- Calcular preços de venda otimizados para o Mercado Livre
- Gerar relatórios detalhados com informações de edição, artista e raridade

---

## 🚀 Funcionalidades

- **🔍 Web Scraping Inteligente**: Navegação automatizada com Selenium para extração de dados em tempo real
- **💰 Cálculo Automático de Taxas**: Aplicação das comissões do Mercado Livre (11.5% + taxa fixa quando aplicável)
- **📊 Pipeline de Dados Completo**:
  - Leitura de arquivos Excel (.xlsx)
  - Processamento com Pandas
  - Exportação de relatórios consolidados
- **🎨 Informações Detalhadas**: Captura de edição, artista, raridade e valores de mercado

---

## 📂 Estrutura do Projeto

```
preco_magic_card/
├── excel/                          # Pasta de dados
│   ├── lista_cartas_magic_com_edicao.xlsx    # Arquivo de entrada (exemplo)
│   └── cartas_magic_output.xlsx              # Arquivo de saída (gerado)
├── magic_preco_medio.py            # Script principal
├── magic_preco_medio.ipynb         # Notebook Jupyter (versão interativa)
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação
├── LICENSE.md                      # Licença MIT
└── img/                            # Assets visuais
    ├── gif_rapido.gif              # Demonstração animada
    ├── lista_cartas.JPG            # Exemplo de entrada
    └── saida_cartas.JPG            # Exemplo de saída
```

---

## 🔧 Pré-requisitos

- **Python 3.9** ou superior
- **Google Chrome** instalado
- **Conexão com internet** (para scraping do LigaMagic)

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/alan-vieira/preco_magic_card.git
cd preco_magic_card
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🔧 Como Usar

### 1. Prepare sua lista de cartas em formato Excel

Coloque o arquivo na pasta `excel/` com o nome: `lista_cartas_magic_com_edicao.xlsx`

**Colunas necessárias:**

| Coluna | Descrição |
|--------|-----------|
| `nome_portugues` | Nome da carta em português |
| `nome_ingles` | Nome da carta em inglês |
| `edicao` | Nome da edição |

### 2. Execute o script

```bash
python magic_preco_medio.py
```

Ou use o notebook interativo:
```bash
jupyter notebook magic_preco_medio.ipynb
```

### 3. Acompanhe a execução

O script exibirá no console o progresso da extração:
```
1. Tutor Vampírico | Vampiric Tutor | Sexta Edição Clássica | Gary Leach | Rara | R$ 281,35
2. Proteção Oscilante | Flickering Ward | Tempestade | ... | ... | ...
...
```

### 4. Resultado

Ao final, o arquivo `excel/cartas_magic_output.xlsx` será gerado com as colunas adicionais:

| Coluna | Descrição |
|--------|-----------|
| `artista` | Artista da carta |
| `raridade` | Raridade (Comum, Incomum, Rara, Mítica) |
| `valor_medio` | Preço médio extraído do LigaMagic |
| `valor_ml` | Preço sugerido para venda no Mercado Livre |

---

## 🧮 Lógica de Precificação

O cálculo do preço de venda no Mercado Livre segue a seguinte regra:

### Para valores ≥ R$ 79,00:
```
valor_ml = valor_medio + (valor_medio × 0.115)
```

### Para valores < R$ 79,00:
```
valor_ml = valor_medio + (valor_medio × 0.115) + 5.00
```

**Onde:**
- `valor_medio`: Preço médio extraído do LigaMagic
- `valor_ml`: Preço sugerido para venda no Mercado Livre

### Exemplo de Saída

| nome_portugues | nome_ingles | edicao | artista | raridade | valor_medio | valor_ml |
|---|---|---|---|---|---|---|
| Tutor Vampírico | Vampiric Tutor | Sexta Edição Clássica | Gary Leach | Rara | 281.35 | 315.11 |
| Desenterrar | Unearth | O Legado de Urza | Don Hazeltine | Comum | 4.56 | 10.11 |

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.9+ | Linguagem principal |
| Selenium | 4.6.1 | Automação de navegador |
| Pandas | 1.5.2 | Manipulação de dados |
| WebDriver Manager | 3.8.5 | Gerenciamento automático do ChromeDriver |
| OpenPyXL | 3.0.10 | Leitura/escrita de arquivos Excel |

---

## ⚠️ Importante

- **Tempo de execução**: O script inclui delays aleatórios (2-4 segundos) entre requisições para não sobrecarregar o servidor do LigaMagic
- **Atualizações do site**: O LigaMagic pode alterar seu layout, o que pode exigir atualização dos seletores CSS/XPath
- **Headless mode**: O navegador roda em modo invisível por padrão. Para ver a execução, remova a flag `--headless` no código
- **Duplicatas**: O script remove cartas duplicadas (mesmo nome português), mantendo apenas a primeira ocorrência

---

## 📚 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

---

## 👤 Autor

**Alan Vieira** — *Engenheiro de Telecomunicações & Especialista em Dados*

- [LinkedIn](https://www.linkedin.com/in/alansilvavieira)
- [GitHub Portfólio](https://github.com/alan-vieira)

---

*Made with ❤️ by Magic players, for Magic players*