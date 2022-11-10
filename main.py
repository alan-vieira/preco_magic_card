import time
from time import sleep

from random import randint

import pandas as pd

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from webdriver_manager.chrome import ChromeDriverManager


# transformando o arquivo excel em dataframe
cartas_df = pd.read_excel('excel/lista_cartas_magic_com_edicao.xlsx')

# eliminando as duplicatas (cartas com o mesmo nome e edições diferentes)
cartas_df = cartas_df.drop_duplicates(
    subset='nome_portugues', keep="first").reset_index(drop=True)


# algumas configurações para o webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')

# instanciando a versão do webdriver que será instalada na máquina local
service = Service(ChromeDriverManager().install())

# instanciando o webdriver
driver = webdriver.Chrome(service=service, options=chrome_options)


nome_portugues_lista = []
nome_ingles_lista = []
edicao_lista = []
artista_lista = []
raridade_lista = []
valor_medio_srt_lista = []

cartas_web_dic = []

# efetuando busca no site
for portugues, ingles in zip(cartas_df['nome_portugues'], cartas_df['nome_ingles']):

    driver.get(f"https://www.ligamagic.com/?view=cards/card&card={portugues}&aux={ingles}")

    sleep(randint(2, 4))

    action = ActionChains(driver)

    # selecionar a edição
    edcard = 0

    while True:
        try:
            edicao_menu = driver.find_element(
                By.CSS_SELECTOR, f"#edcard_{edcard}> img:nth-child(1)")
            action.move_to_element(edicao_menu).click().perform()

        except NoSuchElementException:
            break
        else:
            edcard += 1

        # pegar o valor médio da carta
        nome_portugues = portugues
        nome_ingles = ingles
        edicao = driver.find_element(By.XPATH, '//*[@id="ed-nome"]/a').text
        artista = driver.find_element(By.XPATH, '//*[@id="ed-artista"]/a').text
        raridade = driver.find_element(
            By.XPATH, '//*[@id="ed-raridade"]/a').text
        valor_medio_srt = driver.find_element(
            By.XPATH, '//*[@id="card-info"]/div[5]/div[2]/div/div[4]').text

        # exibir nome e edição
        print(f"{edcard}. {nome_portugues} | {nome_ingles} | {edicao} | {artista} | {raridade} | {valor_medio_srt}")

        # criação do dicionário
        cartas_web_dic.append({
            'nome_portugues': nome_portugues,
            'nome_ingles': nome_ingles,
            'edicao': edicao,
            'artista': artista,
            'raridade': raridade,
            'valor_medio_srt': valor_medio_srt
        })


# corversão do dicionário para dataframe
cartas_web_df = pd.DataFrame().from_dict(cartas_web_dic)


# fechando o site
time.sleep(10)
driver.close()


# transformando o valor médio string para float
cartas_web_df['valor_medio'] = list(
    map(
        lambda x: x.split(" ")[1].replace(".", "").replace(",", "."),
        cartas_web_df['valor_medio_srt']))

cartas_web_df['valor_medio'] = list(
    map(
        lambda x: float(x),
        cartas_web_df['valor_medio']))


# calculando a comissão do mercado livre
def comissao_ml(valor_medio) -> int:
    '''calculo de porcentagem (ml) e valor final do produto'''
    if valor_medio >= 79:
        porcentagem_ml = ((12 / 100) * valor_medio)
    else:
        porcentagem_ml = ((12 / 100) * valor_medio) + 5

    valor_ml = round((porcentagem_ml + valor_medio), 2)

    return valor_ml


cartas_web_df['valor_ml'] = list(
    map(
        lambda x: comissao_ml(x),
        cartas_web_df['valor_medio']))


# interseção das duas tabelas (para retornar apenas as edições de interece)
cartas_final_df = pd.merge(cartas_df, cartas_web_df, how='left', on=(
    'nome_portugues', 'nome_ingles', 'edicao'))


# teste para saber se foi realmente retoranda a lista desejada
if len(cartas_df["nome_portugues"]) == len(cartas_final_df["nome_portugues"]):
    print('Ok!')
else:
    print('Deu errado!')


# geração do arquivo final
cartas_final_df.to_excel("excel/cartas_magic_output.xlsx")
print(cartas_final_df)
