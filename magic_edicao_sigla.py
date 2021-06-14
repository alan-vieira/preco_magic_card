# Programa para pegar o nome da edição de a sigla do jogo mágic #

# instalando bibliotecas do Python
from random import randint
from time import sleep
import pandas as pd

# scraping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# alimentando a variável com a url
url = 'https://www.ligamagic.com/?view=cards/edicoes'

# algumas configurações para o webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path='c:/chromedriver.exe', options=chrome_options)

# acessando o site
driver.get(url)

# permitir todos os cookies
driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/button").click()

# loop para criar o dicionário
ed = []
sl = []

while True:
    sleep(randint(2, 4))

    # pegando o html da página
    html = driver.page_source
    soup2 = BeautifulSoup(html, 'html.parser')

    # pegando o elemento específico do html
    out = [option.text for option in soup2.select('#tab-edc td')]

    # pegando apenas a edição e a sigla
    ed_temp = []
    sl_temp = []

    a = 0
    b = 1

    for i in range(len(out)):
        if a and b > len(out):
            break
        ed_temp.append(out[a])
        sl_temp.append(out[b])

        a += 6
        b += 6

    # passando o vetor temporário para o vetor final
    for i in range(len(ed_temp)):
        ed.append(ed_temp[i])
        sl.append(sl_temp[i])

    # clicando no botão próximo
    botao = driver.find_element_by_xpath("//*[@id='tab-edc_próximo']").get_attribute("class")
    if botao == "paginate_button próximo":
        driver.find_element(By.CSS_SELECTOR, "a#tab-edc_próximo.paginate_button.próximo").click()
    else:
        break

# salvando em um dicionário
edicao_dic = {'edicao': ed, 'sigla': sl}

# passando de um dicionário para um dataframe
edicao_df = pd.DataFrame().from_dict(edicao_dic)

# visualizando o dataframe
print(edicao_df)

# visualizando informações do dataframe
edicao_df.info()

edicao_df.to_csv("excel/output.csv", index=False)
