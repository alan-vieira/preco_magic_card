# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.3] - 2026-09-23

### 🛠️ Corrigido
- Ajuste no type hint da função de cálculo de comissão para refletir corretamente o retorno `float`.

### ✨ Melhorado
- Estrutura do script principal encapsulada em função `main()` com bloco `if __name__ == "__main__":` para evitar execução acidental em imports.
- Modernização dos caminhos de arquivos utilizando `pathlib.Path` no lugar de strings literais.
- Refinamento no tratamento de fallback de nomes de cartas e mensagens de log.

###  Documentação
- README.md e CHANGELOG.md revisados para refletir o amadurecimento do projeto e as boas práticas aplicadas.

## [1.0.2] - 2026-09-16

### ✨ Qualidade de Código (Code Quality)
- **Formatação Black:** Código formatado automaticamente seguindo PEP 8 (linha de 88 chars, aspas duplas, trailing commas)
- **Ordenação isort:** Imports organizados por categoria (stdlib → third-party → local) com seções claras
- **Type Hints Completos:** Todas as funções possuem anotações de tipo (args, return, variáveis locais)
- **Docstrings Google Style:** Documentação padronizada em todas as funções (Args, Returns, Raises, Example)
- **Pylint 10/10:** Código passa em análise estática rigorosa sem warnings/errors

### 🔧 Refatoração Interna
- Reorganização dos imports (stdlib → third-party → local)
- Variáveis tipadas explicitamente (`list[dict[str, Any]]`, `pd.DataFrame`)
- Função `comissao_ml` com assinatura tipada e docstring completa
- Função `separar_edicao_ano` com type hints de Tuple
- Remoção de comentários redundantes, código auto-documentado

### 🛡️ Robustez
- Type hints permitem detecção precoce de bugs via static analysis
- Docstrings facilitam manutenção e onboarding
- Estrutura preparada para testes unitários futuros

---

## [1.0.1] - 2026-09-16

### ✨ Funcionalidades (Features)
- **Pipeline de Scraping com Playwright:** Migração completa do Selenium para o Playwright, resultando em execução mais rápida, estável e com melhor manejo de esperas assíncronas.
- **Extração Polimórfica de Edições:** Lógica inteligente que detecta automaticamente se a carta possui múltiplas edições (interage com o slider) ou se é uma edição única (extrai diretamente da tela principal).
- **Engenharia de Dados com Regex:** Implementação de expressão regular para separar dinamicamente a string da edição (ex: "Sexta Edição Classica (1999)") em duas colunas distintas: `edicao` (nome) e `ano` (inteiro).
- **Sanitização de Tipos de Dados:** Conversão robusta de strings de moeda brasileira (ex: `"R$ 1.023,00"`) para o tipo `float` (`1023.00`), permitindo cálculos matemáticos e ordenação no Pandas.
- **Motor de Regras de Negócio (Mercado Livre):** Cálculo automático e preciso do preço de venda sugerido (11,5% de comissão para valores ≥ R$ 79,00; 11,5% + taxa fixa de R$ 5,00 para valores < R$ 79,00).
- **Merge Inteligente (ETL):** Fusão dos dados raspados com a planilha original do usuário, preservando todas as colunas de entrada e enriquecendo-as com os dados de mercado.
- **Automação de LGPD:** Clique automático e seguro no banner de cookies, com verificação de existência para evitar `TimeoutError`.

### 🛡️ Resiliência e Tratamento de Erros
- **Padrão `.all()` do Playwright:** Substituição de loops `while True` baseados em índices frágeis por iteração direta sobre a lista de elementos, eliminando erros `TargetClosedError` e `Timeout`.
- **Fallback de Nomes:** Se o XPath específico para o nome da carta falhar, o sistema usa silenciosamente os nomes fornecidos no arquivo Excel de entrada como backup.
- **Isolamento de Falhas:** Cada campo extraído possui seu próprio bloco de tratamento de erro. Se um campo falhar, o script registra o erro, preenche com "N/A" e continua, em vez de abortar a execução total.

### 🐛 Correções (Bug Fixes)
- **Compatibilidade de Merge:** Resolvido conflito de chaves causado por variações de digitação (ex: "Máscara de Mercádia" no input vs "Máscaras de Mercádia" no site) através de normalização de strings.
- **Limpeza de Chaves:** Aplicação de `.str.strip()` nas colunas de merge para evitar falhas silenciosas causadas por espaços em branco acidentais.
- **Otimização de Timeout:** Redução do timeout de espera por elementos de nome de 30s para 3s, acelerando drasticamente o fallback.

### 🔧 Refatoração e Higiene do Projeto
- **Padronização do Entry Point:** Renomeado `teste_rapido.py` para `magic_preco_medio.py`, estabelecendo o nome definitivo do script principal.
- **Limpeza de Código Morto:** Removidos arquivos obsoletos e legados (`teste.py`, `magic_preco_medio.ipynb`, versões antigas do script) para reduzir ruído no repositório.
- **Proteção de Dados:** Atualizado o `.gitignore` para ignorar automaticamente os arquivos de saída gerados (`precos_capturados.xlsx`, `cartas_com_precos_atualizados.xlsx`), mantendo versionado apenas o template de entrada.
- **Documentação de Nível Profissional:** Reescrita completa do `README.md` e `CHANGELOG.md` com badges, estrutura de projeto, regras de negócio detalhadas e guias de instalação.
- **Qualidade de Código:** Aplicação de PEP 8, adição de Type Hints e Docstrings no estilo Google em todas as funções para melhorar a legibilidade e manutenção futura.

---

## 📜 Histórico (Versões Depreciadas)

> ⚠️ **Atenção:** As versões abaixo representam a base de código legada (Selenium) e não recebem mais atualizações. Elas são mantidas apenas para referência histórica do ponto de partida da refatoração.

### [v1.0-legacy] - 2026-09-15
- **Status:** Arquivado. Funcionalidade de scraping quebrada devido a alterações não anunciadas no layout do DOM do LigaMagic.
- **Tecnologias:** Selenium WebDriver 4.6.1, Pandas 1.5.2, WebDriver Manager 3.8.5.
- **Funcionalidades Originais:** Extração básica de preços, cálculo de taxas do ML e geração de relatório único em Excel.

### [v0.1-alpha] - 2022-11-15
- **Status:** Arquivado.
- **Descrição:** Primeiro lançamento conceitual do projeto com implementação inicial do scraper, cálculo básico de precificação e arquivo de exemplo com 11 cartas.

---

## 🔗 Links Úteis
- [Releases no GitHub](https://github.com/alan-vieira/preco_magic_card/releases)
- [Branch v1.0.2](https://github.com/alan-vieira/preco_magic_card/tree/v1.0.2)
- [Branch v1.0.1](https://github.com/alan-vieira/preco_magic_card/tree/v1.0.1)
- [Branch v1.0-legacy](https://github.com/alan-vieira/preco_magic_card/tree/v1.0-legacy)