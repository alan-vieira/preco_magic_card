# busca o preço médio de todas as edições das cartas informada na lista

import time
from random import randint
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

nome_portugues_lista = []
nome_ingles_lista = []
edicao_lista = []
artista_lista = []
raridade_lista = []
valor_medio_srt_lista = []

valor_medio_lista = []
valor_final_lista = []
valor_ml_lista = []
cartas_web_dic = {}

# leitura do arquivo excel
minhas_cartas_df = pd.read_excel('excel/lista_cartas_magic_com_edicao.xlsx')

# eliminar as duplicatas da lista e salvar em um novo dataframe
cartas_unica_df = minhas_cartas_df.drop_duplicates(subset='nome_portugues', keep="first").reset_index(drop=True)

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

# abrindo o site
driver = webdriver.Chrome(executable_path='c:/chromedriver.exe', options=chrome_options)

# efetuando busca no site
for i in range(len(minhas_cartas_df["nome_portugues"])):
    driver.get("https://www.ligamagic.com/?view=cards/card&card=%s&aux=%s"
               % (minhas_cartas_df["nome_ingles"][i], minhas_cartas_df["nome_portugues"][i]))
    sleep(randint(2, 4))

    action = ActionChains(driver)

    # selecionar a edição
    edcard = 0

    while True:
        try:
            edicao_menu = driver.find_element(By.CSS_SELECTOR, "#edcard_%i > img:nth-child(1)" % edcard)
            action.move_to_element(edicao_menu).click().perform()

        except NoSuchElementException:
            break
        else:
            edcard += 1

        # pegar o valor médio da carta
        nome_portugues = cartas_unica_df["nome_portugues"][i]
        nome_ingles = cartas_unica_df["nome_ingles"][i]
        edicao = driver.find_element(By.XPATH, '//*[@id="ed-nome"]/a').text
        artista = driver.find_element(By.XPATH, '//*[@id="ed-artista"]/a').text
        raridade = driver.find_element(By.XPATH, '//*[@id="ed-raridade"]/a').text
        valor_medio_srt = driver.find_element(By.XPATH, '//*[@id="card-info"]/div[5]/div[2]/div/div[4]').text

        # converssão do valor médio de string para ponto flutuante #
        # separa o R$ da string, pega a parte numérica,
        # troca a vírgula por ponto e convert o resultado em ponto flutuante
        valor_medio = valor_medio_srt.split(" ")[1].replace(".", "")
        valor_medio = valor_medio.replace(",", ".")
        valor_medio = float(valor_medio)

        # calculo de porcentagem (ml) e valor final do produto
        if valor_medio >= 79:
            porcentagem_ml = ((12 / 100) * valor_medio)
        else:
            porcentagem_ml = ((12 / 100) * valor_medio) + 5

        valor_ml = round((porcentagem_ml + valor_medio), 2)

        # exibir nome e edição
        print('%i. %s | %s | %s | %s | %s | %s' % (
            edcard, nome_portugues, nome_ingles, edicao, artista, raridade, valor_medio))

        # criação das listas
        nome_portugues_lista.append(nome_portugues)
        nome_ingles_lista.append(nome_ingles)
        edicao_lista.append(edicao)
        artista_lista.append(artista)
        raridade_lista.append(raridade)
        valor_medio_lista.append(valor_medio)
        valor_ml_lista.append(valor_ml)

# criação do dicionário
cartas_web_dic = {'nome_portugues': nome_portugues_lista,
                  'nome_ingles': nome_ingles_lista,
                  'edicao': edicao_lista,
                  'artista': artista_lista,
                  'raridade': raridade_lista,
                  'valor_medio': valor_medio_lista,
                  'valor_ml': valor_ml_lista}

# criação do dataframe
cartas_web_df = pd.DataFrame().from_dict(cartas_web_dic)

# interseção das duas tabelas
cartas_final_df = pd.merge(minhas_cartas_df, cartas_web_df, how='left', on=('nome_portugues', 'nome_ingles', 'edicao'))

# teste se deu tudo certo
if len(minhas_cartas_df["nome_portugues"]) == len(cartas_final_df["nome_portugues"]):
    print('Ok!')
else:
    print('Deu errado!')

# geração do arquivo final
cartas_final_df.to_excel("excel/cartas_magic_output.xlsx")
print(cartas_final_df)

# fechando o site
time.sleep(10)
driver.close()
