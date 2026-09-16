# 🃏 Magic Preço Médio

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/alan-vieira/preco_magic_card/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.47+-green.svg)](https://playwright.dev/python/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://www.pylint.org/)

Sistema de inteligência de mercado para precificação de cartas de Magic: The Gathering.

## 📖 Visão Geral

Este projeto automatiza a coleta de preços médios de cartas de **Magic: The Gathering** no site **LigaMagic** e processa esses dados para gerar uma estratégia de precificação competitiva no **Mercado Livre**, considerando automaticamente as taxas de comissão da plataforma.

## 🎯 Objetivo

- Extrair preços de referência do mercado brasileiro (LigaMagic)
- Calcular preços de venda otimizados para o Mercado Livre
- Gerar relatórios detalhados com informações de edição, artista, raridade e ano

## 🚀 Funcionalidades

- **🔍 Web Scraping Inteligente**: Navegação automatizada com **Playwright** para extração de dados em tempo real
- 💰 **Cálculo Automático de Taxas**: Aplicação das comissões do Mercado Livre (11.5% + taxa fixa quando aplicável)
- 📊 **Pipeline de Dados Completo**:
  - Leitura de arquivos Excel (.xlsx)
  - Processamento com Pandas
  - Separação automática de edição e ano via Regex
  - Merge inteligente com planilha original
  - Exportação de relatórios consolidados
- 🎨 **Informações Detalhadas**: Captura de edição, artista, raridade e valores de mercado
- 🛡️ **Resiliência**: Fallback automático para cartas de edição única e tratamento de erros por campo
- ✨ **Código de Qualidade**: Formatação PEP 8, Type Hints e Docstrings Google Style

## 📂 Estrutura do Projeto

```text
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
```

## 🔧 Pré-requisitos

- **Python 3.9** ou superior
- **Google Chrome** instalado (usado pelo Playwright)
- **Conexão com internet** (para scraping do LigaMagic)

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/alan-vieira/preco_magic_card.git
cd preco_magic_card
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
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

O script exibirá no console o progresso da extração (o navegador abrirá visivelmente, pois `headless=False`):

```text
============================================================
Processando: Tutor Vampírico (Vampiric Tutor)
============================================================
Acessando: Tutor Vampírico (Vampiric Tutor)...
🔍 Encontrados 17 botões de edição no slider.
✅ Tutor Vampírico | Sexta Edição Classica (1999) | R$ 415,62
...
✅ 17 edições capturadas para Tutor Vampírico
```

### 4. Resultado

Ao final, dois arquivos serão gerados em `excel/`:

**`precos_capturados.xlsx`** — Dados brutos com todas as edições encontradas (52 registros no total):

| Coluna | Descrição |
|--------|-----------|
| `nome_portugues` | Nome em português |
| `nome_ingles` | Nome em inglês |
| `edicao_completa` | Edição completa (com ano) |
| `edicao` | Edição (sem ano, extraída via Regex) |
| `ano` | Ano de lançamento (extraído via Regex) |
| `raridade` | Raridade da carta |
| `artista` | Artista da ilustração |
| `preco` | Preço formatado (R$) |
| `preco_float` | Preço numérico |
| `valor_ml` | Preço com comissão ML |

**`cartas_com_precos_atualizados.xlsx`** — Merge com sua lista original (11 registros, apenas a edição correspondente):

| Coluna | Descrição |
|--------|-----------|
| `nome_portugues` | Nome em português |
| `nome_ingles` | Nome em inglês |
| `edicao` | Edição (sem ano) |
| `edicao_completa` | Edição completa (com ano) |
| `ano` | Ano de lançamento |
| `raridade` | Raridade |
| `artista` | Artista |
| `preco` | Preço formatado |
| `preco_float` | Preço numérico |
| `valor_ml` | Preço com comissão ML |

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
- `valor_medio`: Preço médio extraído do LigaMagic (`preco_float`)
- `valor_ml`: Preço sugerido para venda no Mercado Livre

### Exemplo de Saída

| nome_portugues | edicao | preco | preco_float | valor_ml |
|---|---|---|---|---|
| Tutor Vampírico | Sexta Edição Classica | R$ 415,62 | 415.62 | 463.42 |
| Desenterrar | O Legado de Urza | R$ 18,83 | 18.83 | 26.00 |

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.9+ | Linguagem principal |
| Playwright | 1.47+ | Automação de navegador (substituiu o Selenium) |
| Pandas | 2.2.3 | Manipulação de dados e merge |
| OpenPyXL | 3.1.5 | Leitura/escrita de arquivos Excel |
| Black | 24.0+ | Formatação automática de código |
| isort | 5.13+ | Ordenação de imports |
| Pylint | 3.0+ | Análise estática de código |

## 🔍 Qualidade de Código

Este projeto segue rigorosamente os padrões de qualidade da indústria:

- **PEP 8**: Formatação padrão do Python
- **Black**: Formatação automática e consistente
- **isort**: Ordenação inteligente de imports
- **Pylint**: Análise estática para detectar code smells
- **Type Hints**: Anotações de tipo em todas as funções
- **Docstrings**: Documentação no estilo Google em todas as funções

### Verificação de Qualidade

```bash
# Formatar código
black magic_preco_medio.py

# Ordenar imports
isort magic_preco_medio.py

# Analisar qualidade
python -m pylint magic_preco_medio.py
```

## ⚠️ Importante

- **Tempo de execução**: O script inclui delays para não sobrecarregar o servidor do LigaMagic.
- **Atualizações do site**: O LigaMagic pode alterar seu layout, o que pode exigir atualização dos seletores.
- **Headless mode**: O navegador roda em modo visível (`headless=False`) por padrão para facilitar o acompanhamento.
- **Duplicatas**: O script remove cartas duplicadas (mesmo nome português), mantendo apenas a primeira ocorrência.
- **Fallback**: Se o XPath do nome falhar, o script usa os nomes da lista original como backup.

## 📚 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

## 👤 Autor

**Alan Vieira** — *Engenheiro de Telecomunicações & Especialista em Dados*

- [LinkedIn](https://www.linkedin.com/in/alansilvavieira)
- [GitHub](https://github.com/alan-vieira)

---

*Made with ❤️ by Magic players, for Magic players*