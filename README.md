# Magic Preço Médio
## Descrição do projeto
Projeto de mineração de dados (web scraping), para extração do preço médio das cartas do jogo Magic no site ligamagic.com. Para posteriormente compor o preço de venda no Mercado Livre. 

## Funcionalidades do projeto

- `Funcionalidade 1`: captura do preço médio no site ligamagic.com
- `Funcionalidade 2`: cálculo do percentual da comissão do Mercado Livre
- `Funcionalidade 3`: geração da planilha Excel de saída com as colunas: nome em português, nome em inglês, edição, artista, raridade, valor médio, valor do mercado livre.

## Aplicação

![Magic Preço Médio](./img/gif_rapido.gif)

## Ferramentas utilizadas
- `Python`
- `Selenium`

## Acesso ao projeto

Você pode acessar o [código fonte do projeto](https://github.com/alan-vieira/preco_magic_card/blob/master/lista_magic_preco.py) ou [baixá-lo](https://github.com/alan-vieira/preco_magic_card/archive/refs/heads/master.zip).

## Abrir e rodar o projeto
Após baixado, para o funcionamento correto da aplicação as seguintes dependêcias deverão ser instaladas.

- `Pandas`
- `Selenium`
- `WebDriver`
- `ActionChains`
- `By`
- `NoSuchElementException`
- `Openpyxl`

E para complementar, o arquivo [chromedriver](https://chromedriver.chromium.org/downloads) deve ser baixado e instalado na raiz do seu sistema operacional.

Obs.: O chromedriver deve ser escolhido de acordo com a versão do seu navegador.

