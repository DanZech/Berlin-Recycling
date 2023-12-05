import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
import time

load_dotenv()

# Configurações do WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximizar a janela do navegador
# chrome_options.add_argument("--headless") # Descomente para rodar sem abrir o navegador
# chrome_options.add_argument("--no-sandbox")  # Bypass OS security model


# Especifique o diretório de download desejado
prefs = {"download.default_directory": "//mnt/c/Users/daniz/OneDrive/Documentos/Berlin-Recycling"}
chrome_options.add_experimental_option("prefs", prefs)

# Adicionando o caminho do chromedriver ao PATH
os.environ['PATH'] += r"D:\SeleniumDrivers\chrome-win64\chrome-win64"
driver = webdriver.Chrome(options=chrome_options)

try:
    print("Abrindo a página de login...")
    driver.get('https://kundenportal.berlin-recycling.de/Login.aspx')

    # Espera explícita para o campo de email ficar visível
    print("Aguardando o campo de email ficar disponível...")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "userField")))

    email_field = driver.find_element(By.ID, "userField")
    password_field = driver.find_element(By.ID, "passwordField")

    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')

    print("Preenchendo as credenciais...")
    email_field.send_keys(EMAIL)
    password_field.send_keys(PASSWORD)

    login_button = driver.find_element(By.ID, "LogBtn")
    login_button.click()

    # Espera explícita para algum elemento da página seguinte, indicando sucesso no login
    print("Aguardando login ser realizado...")

    # confirma o login pelo elemento presente após o login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Home')]"))
    )
    print("Login realizado com sucesso!")
   
    print("Procurando pelo botão 'Show all'...")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-listAllEvents-button")))
    show_all_button = driver.find_element(By.CLASS_NAME, "fc-listAllEvents-button")
    print("Botão 'Show all' encontrado.")
    driver.execute_script("arguments[0].click();", show_all_button)  # Clique usando JavaScript
    print("Botão 'Show all' clicado.")

    print("Procurando pelo botão 'ICAL'...")

   # Localizando o botão iCal pelo atributo title e clicando nele
    ical_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i[title='ICAL']"))
    )

    # Rolar a tela até o botão iCal
    driver.execute_script("arguments[0].scrollIntoView(true);", ical_button)
    time.sleep(2)  # Pequena pausa para garantir que a rolagem foi concluída

    ical_button.click()
    print("Botão iCal clicado.")

    
except NoSuchElementException as e:
    print("Erro ao localizar um elemento: ", e)
except TimeoutException as e:
    print("Tempo de espera excedido: ", e)
finally:
    # Manter o navegador aberto até que o usuário decida fechar
    input("Pressione ENTER para fechar o navegador...")

    # Fechar o navegador
    # driver.quit()