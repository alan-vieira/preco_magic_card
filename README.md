# 🃏 Magic Preço Médio: Automação de Precificação & Scraping

[![GitHub release](https://img.shields.io/github/release/alan-vieira/preco_magic_card.svg)](https://github.com/alan-vieira/preco_magic_card/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Playwright 1.47+](https://img.shields.io/badge/playwright-1.47+-green.svg)](https://playwright.dev/python/)

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

- **🔍 Web Scraping Inteligente**: Navegação automatizada com **Playwright** para extração de dados em tempo real
- **💰 Cálculo Automático de Taxas**: Aplicação das comissões do Mercado Livre (11.5% + taxa fixa quando aplicável)
- **📊 Pipeline de Dados Completo**:
  - Leitura de arquivos Excel (.xlsx)
  - Processamento com Pandas
  - Exportação de relatórios consolidados (3 arquivos de saída)
- **🎨 Informações Detalhadas**: Captura de edição, artista, raridade e valores de mercado
- **🏷️ Separação Inteligente**: Separação automática de edição e ano via Regex
- **🔄 Merge Inteligente**: Fusão resiliente com planilha original, lidando com variações de formato

---

## 📂 Estrutura do Projeto

```
preco_magic_card/
├── excel/                          # Pasta de dados
│   ├── lista_cartas_magic_com_edicao.xlsx    # Arquivo de entrada (versionado)
│   ├── precos_capturados.xlsx                # Dados brutos do scraping (ignorado no git)
│   └── cartas_com_precos_atualizados.xlsx    # Arquivo final consolidado (ignorado no git)
├── magic_preco_medio.py            # Script principal
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação
├── CHANGELOG.md                    # Histórico de mudanças
├── LICENSE.md                      # Licença MIT
├── .gitignore                      # Arquivos ignorados pelo Git
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

### 4. Instale os navegadores do Playwright

```bash
playwright install chromium
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
| `edicao` | Nome da edição (sem ano) |

### 2. Execute o script

```bash
python magic_preco_medio.py
```

### 3. Acompanhe a execução

O script exibirá no console o progresso da extração (navegador visível por padrão - `headless=False`):

```
============================================================
Processando: Tutor Vampírico (Vampiric Tutor)
============================================================
Acessando: Tutor Vampírico (Vampiric Tutor)...
🔍 Encontrados 5 botões de edição no slider.
✅ Tutor Vampírico | Sexta Edição Clássica | R$ 281,35
✅ Tutor Vampírico | O Legado de Urza | R$ 234,50
...
============================================================

Total de registros capturados: 52
```

### 4. Resultado

Ao final, **3 arquivos** serão gerados/atualizados na pasta `excel/`:

| Arquivo | Descrição |
|---------|-----------|
| `precos_capturados.xlsx` | **Dados brutos** - 52 registros com todas as edições capturadas (nome PT/EN, edição completa, raridade, artista, preço, preco_float, valor_ml) |
| `cartas_com_precos_atualizados.xlsx` | **Arquivo final** - Merge inteligente com a planilha original (11 cartas × edições), colunas: nome_portugues, nome_ingles, edicao, ano, artista, raridade, valor_medio, valor_ml |
| `lista_cartas_magic_com_edicao.xlsx` | **Entrada** - Mantido versionado (não modificado) |

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

### Exemplo de Saída (cartas_com_precos_atualizados.xlsx)

| nome_portugues | nome_ingles | edicao | ano | artista | raridade | valor_medio | valor_ml |
|---|---|---|---|---|---|---|---|
| Tutor Vampírico | Vampiric Tutor | Sexta Edição Clássica | 1999 | Gary Leach | Rara | 281.35 | 313.71 |
| Desenterrar | Unearth | O Legado de Urza | 1999 | Don Hazeltine | Comum | 4.56 | 10.11 |

---

## 🏷️ Separação de Edição e Ano (Regex)

O script separa automaticamente o nome da edição do ano de lançamento usando expressão regular:

**Entrada:** `"Sexta Edição Clássica (1999)"`  
**Saída:** `edicao = "Sexta Edição Clássica"`, `ano = 1999`

**Regex utilizado:** `r'\((\d{4})\)\s*$'`

Isso permite o merge inteligente mesmo quando a planilha original contém apenas o nome da edição sem o ano.

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.9+ | Linguagem principal |
| **Playwright** | **1.47+** | **Automação de navegador (substituiu Selenium)** |
| Pandas | 2.2.3 | Manipulação de dados |
| OpenPyXL | 3.1.5 | Leitura/escrita de arquivos Excel |
| NumPy | 1.23.5+ | Operações numéricas (dependência do Pandas) |

---

## ⚠️ Importante

- **Tempo de execução**: O script inclui delays aleatórios entre requisições para não sobrecarregar o servidor do LigaMagic
- **Atualizações do site**: O LigaMagic pode alterar seu layout, o que pode exigir atualização dos seletores CSS/XPath
- **Modo visível**: O navegador roda com `headless=False` por padrão (visível). Para modo headless, altere `headless=True` no código
- **Duplicatas**: O script remove cartas duplicadas (mesmo nome português), mantendo apenas a primeira ocorrência
- **Arquivos de saída**: `precos_capturados.xlsx` e `cartas_com_precos_atualizados.xlsx` são gerados automaticamente e estão no `.gitignore`

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