import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

nome_lista = []
edicao_lista = []
valor_medio_lista = []
valor_final_lista = []
carta_dic = {}

# leitura do arquivo excel
df = pd.read_excel('excel/Magic_ML.xlsx')
# print(data["nome_portugues"][0], data["xpath"][0])

# abrindo o site
driver = webdriver.Firefox(executable_path='c:/geckodriver.exe')
driver.get("https://ligamagic.com/")
time.sleep(15)

# efetuando busca no site
for i in range(len(df["nome_portugues"])):
    elemento_entrada = driver.find_element_by_id("mainsearch")
    elemento_entrada.send_keys(df["nome_portugues"][i])
    elemento_entrada.submit()
    time.sleep(5)

    action = ActionChains(driver)

    # tem duas cartas?
    if df["busca_carta"][i] == 2:
        carta = driver.find_element_by_xpath("/html/body/main/div[2]/div[4]/div/div[1]/div/div[1]/a").click()

    # selecionar a edição
    edicao_menu = driver.find_element_by_xpath(df["xpath"][i])
    action.move_to_element(edicao_menu).click().perform()

    # pegar o valor médio da carta
    valor_medio_srt = driver.find_element_by_xpath("//*[@id='precos-medio']").text
    nome = driver.find_element_by_xpath("/html/body/main/div[4]/div[1]/div/div[4]/div[1]/div[1]/p[1]").text
    edicao = driver.find_element_by_xpath("/html/body/main/div[4]/div[1]/div/div[4]/div[4]/div[1]/p/font/a").text

    # converssão do valor médio de string para ponto flutuante

    # separa o R$ da string, pega a parte numérica,
    # troca a vírgula por ponto e convert o resultado em ponto flutuante
    valor_medio = float(((valor_medio_srt.split(" "))[1]).replace(",", "."))

    # calculo de porcentagem e valor final do produto
    if valor_medio >= 99:
        porcentagem_ml = ((11.5 / 100) * valor_medio)
    else:
        porcentagem_ml = ((11.5 / 100) * valor_medio) + 5

    valor_final = round((porcentagem_ml + valor_medio), 2)

    # criação das listas
    nome_lista.append(nome)
    edicao_lista.append(edicao)
    valor_medio_lista.append(valor_medio)
    valor_final_lista.append(valor_final)

# criação do dicionário
carta_dic = {'Nome': nome_lista,
             'Edicao': edicao_lista,
             'Valor medio': valor_medio_lista,
             'Valor final': valor_final_lista}

# criação do dataframe
df2 = pd.DataFrame(carta_dic, columns=['Nome', 'Edicao', 'Valor medio', 'Valor final'])

print(df2)

# criação do arquivo excel
escrever = pd.ExcelWriter('excel/saida.xlsx', engine='xlsxwriter')
# conversão do dataframe para excel
df2.to_excel(escrever, sheet_name='Plan1', index=False)
# fechamento do arquivo excel
escrever.save()

# fechando o site
time.sleep(10)
driver.close()
