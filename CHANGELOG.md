# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [v1.0-legacy] - 2026-09-15

### 📌 Status
- **Versão legada** - Funcionalidade de scraping quebrada devido a alterações no layout do LigaMagic
- Marca o ponto de partida para refatoração completa

### ✅ Funcionalidades
- Extração de preços do LigaMagic via Selenium
- Cálculo automático de taxas do Mercado Livre (11.5% + R$5,00 para valores < R$79,00)
- Geração de relatório em Excel com informações detalhadas das cartas
- Suporte a múltiplas edições por carta
- Captura de: nome (PT/EN), edição, artista, raridade e preço médio

### 🔧 Técnicas
- Web scraping com Selenium WebDriver
- Processamento de dados com Pandas
- Leitura/escrita de arquivos Excel (.xlsx)
- Navegação em modo headless

### 📦 Dependências Principais
- selenium==4.6.1
- pandas==1.5.2
- webdriver-manager==3.8.5
- numpy==1.23.5
- openpyxl==3.0.10

### ⚠️ Problemas Conhecidos
- Seletores CSS/XPath desatualizados devido a mudanças no layout do LigaMagic
- Necessária refatoração completa do módulo de scraping

---

## [v0.1-alpha] - 2022-11-15

### 🚀 Primeiro Lançamento
- Implementação inicial do scraper
- Cálculo básico de precificação
- Exportação para Excel
- Arquivo de exemplo com 11 cartas

---

## Links

- [v1.0-legacy](https://github.com/alan-vieira/preco_magic_card/tree/v1.0-legacy)
- [Releases](https://github.com/alan-vieira/preco_magic_card/releases)