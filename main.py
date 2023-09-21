import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox


# Função para iniciar o driver
def start_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1300,1000']
    for argument in arguments:
        chrome_options.add_argument(argument)

    # Configurações experimentais
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
driver.get('https://lista.mercadolivre.com.br/informatica/armazenamento/discos-acessorios/hds-ssds/ssd_Frete_Full_NoIndex_True#applied_filter_id%3Dshipping_highlighted_fulfillment%26applied_filter_name%3DTipo+de+envio%26applied_filter_order%3D1%26applied_value_id%3Dfulfillment%26applied_value_name%3DFull%26applied_value_order%3D1%26applied_value_results%3D2552%26is_custom%3Dfalse')
while True:
    sleep(5)
    # Carregar todos elementos da tela movendo até o final da página
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(2)
    # Pegar todos os elementos da tela
    titulos = driver.find_elements(By.XPATH, "//*[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//h2")
    links = driver.find_elements(By.XPATH, "//*[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//a")
    precos = driver.find_elements(By.XPATH, "//div[@class='ui-search-price ui-search-price--size-medium shops__price']//span[@class='andes-money-amount ui-search-price__part shops__price-part ui-search-price__part--medium andes-money-amount--cents-superscript']//span[@class='andes-money-amount__fraction']")
    # Guardar em um arquivo CSV
    for titulo, link, preco in zip(titulos, links, precos):
        with open('preco.csv', 'a', encoding='utf-8', newline='') as arquivo:
            link_processado = link.get_attribute('href')
            arquivo.write(f'{titulo.text};R${preco.text},00;{link_processado}{os.linesep}')
    # Fazer isso para todas as páginas
    try:
        botao_seguinte = driver.find_element(
            By.XPATH, "//*[@class='andes-pagination__button andes-pagination__button--next shops__pagination-button']/a")
        sleep(2)
        botao_seguinte.click()
    except:
    # Após o término da automação, exiba a caixa de diálogo
        messagebox.showinfo('Fim', 'Chegamos na última página, Automação finalizada com sucesso!')
        break
        input('Pressione ENTER para sair')
        driver.quit()

