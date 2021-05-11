import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

#leitura do arquivo excel
data = pd.read_excel('c:/Users/Alan/Documents/magic/Magic.xlsx')
#print(data["nome_portugues"][0])

#abrindo o site
driver = webdriver.Firefox(executable_path='C:\geckodriver.exe')
driver.get("https://ligamagic.com/")
time.sleep(15)

cont = 0
for i in range(len(data["nome_portugues"])):
    #efetuando busca no site
    elemento_entrada = driver.find_element_by_id("mainsearch")
    elemento_entrada.send_keys(data["nome_portugues"][i])
    elemento_entrada.submit()
    time.sleep(7)
    elemento_entrada = driver.find_element_by_id("mainsearch").clear()
    cont += 1
    print(cont)