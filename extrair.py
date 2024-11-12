from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv



options = Options()
options.add_argument("blink-settings=imagesEnabled=false") 

driver = webdriver.Chrome(service=Service("./chromedriver.exe"), options=options)
driver.get("https://steamdb.info/sales/")
time.sleep(30)

def extrair_dados():
    produtos = []

    linhas = driver.find_elements(By.CSS_SELECTOR, "tr.app")
    for linha in linhas:
        nome = linha.find_element(By.CSS_SELECTOR, "a.b").text  # Nome do produto

        desconto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".price-discount"))
        ).text

        preco = linha.find_elements(By.CSS_SELECTOR, "td.dt-type-numeric")[2].text # Preço
        ranking = linha.find_elements(By.CSS_SELECTOR, "td.dt-type-numeric")[3].text  # Ranking
        release = linha.find_elements(By.CSS_SELECTOR, "td.dt-type-numeric")[4].text # Release
        
        time_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.timeago.dt-type-numeric"))
        )

        ends = time_elements[0].text  # Primeiro elemento "timeago" (ends)
        started = time_elements[1].text 


        produto = {
            "Nome": nome,
            "Desconto": desconto,
            "Preco": preco,
            "Ranking": ranking,
            "Release": release,
            "Ends": ends,
            "Started": started
        }
        produtos.append(produto)
    
    print(f"Total de produtos extraídos: {len(produtos)}")
    for produto in produtos:
        print(produto)  # Mostra cada produto extraído

    return produtos

todos_produtos = []

def salvar_em_csv(produtos):
    with open('steam_sales.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Nome", "Desconto", "Preco", "Ranking", "Release", "Ends", "Started"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()  # Escreve o cabeçalho

        for produto in produtos:
            writer.writerow(produto)  

while True:
    todos_produtos.extend(extrair_dados())
    try:
        proxima_pagina = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.dt-paging-button.next"))
        )

        if 'disabled' in proxima_pagina.get_attribute('class'):
            print("Última página alcançada.")
            break
        proxima_pagina.click()
        time.sleep(2)

    except Exception as e:
        print("Erro ou última página:", e)
        break

driver.quit()

# Salva os dados em um arquivo CSV
salvar_em_csv(todos_produtos)