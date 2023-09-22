import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tkinter import messagebox


# Função para iniciar o driver
def start_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1300,1000']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        # Desabilita a confirmação de download
        'download.prompt_for_download': False,
        # Desabilita notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permite múltiplos downloads
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(options=chrome_options)

    return driver


# Inicializando o driver
driver = start_driver()
driver.get('') ## <- Faça a pesquisa do produto deejado no site do mercado livre e cole o link aqui
while True:
    sleep(5)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(2)
    # Pegar todos os elementos da tela
    titulos = driver.find_elements(By.XPATH, "//*[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//h2")
    links = driver.find_elements(By.XPATH, "//*[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//a")
    precos = driver.find_elements(By.XPATH, "//div[@class='ui-search-price ui-search-price--size-medium shops__price']//span[@class='andes-money-amount ui-search-price__part shops__price-part ui-search-price__part--medium andes-money-amount--cents-superscript']//span[@class='andes-money-amount__fraction']")
    # Guardar em um arquivo CSV
    for titulo, link, preco in zip(titulos, links, precos):
        with open('precos.csv', 'a', encoding='utf-8', newline='') as arquivo:
            link_processado = link.get_attribute('href')
            arquivo.write(f'{titulo.text};R${preco.text},00;{link_processado}{os.linesep}')
    try:
        botao_seguinte = driver.find_element(
            By.XPATH, "//*[@class='andes-pagination__button andes-pagination__button--next shops__pagination-button']/a")
        sleep(2)
        botao_seguinte.click()
    except:
        messagebox.showinfo('Fim', 'Chegamos na última página, Automação finalizada com sucesso!')
        break

input('Pressione ENTER para sair')
driver.quit()

