from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import undetected_chromedriver as uc 
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
import time
import pprint
import smtplib
from email.message import EmailMessage


#---------------DEFINA SEU EMAIL E SENHA ALIEXPRESS --------------------------

email = 'exemplo@outlook.com'
senha = 'exemplo'

#a
#---------------DEFINA SEU EMAIL E SENHA EMAIL --------------------------

seu_email_email = 'exemplo@outlook.com'
sua_senha_email = 'exemplo'


#Defina um destinatario
destinatario_email = "exemplo@outlook.com"






# Função para esperar até que o elemento seja visível ou até um tempo limite
def wait_for_element(by, value, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))
            return element
        except TimeoutException: # type: ignore
            pass
        time.sleep(0.5)  # Espera por 0.5 segundo antes de tentar novamente
    raise TimeoutError(f"Elemento {value} não encontrado após {timeout} segundos.")

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1300,900','--incognito','--headless']
    for argument in arguments: 
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException, # type: ignore
            ElementNotVisibleException, # type: ignore
            ElementNotSelectableException, # type: ignore
        ]
    )
    return driver, wait

def digitar_naturalmente(texto,elemento):
    for letra in texto:
        elemento.send_keys(letra)
        sleep(random.randint(1,5)/30)

def fechar_popup():
    try:
        fechar_popup_elemento = wait_for_element(By.CLASS_NAME,'pop-close-btn', timeout=10)
        fechar_popup_elemento.click()
        print('Pop up fechado com primeiro seletor')
    
    except TimeoutError as e:
        print(f'Erro Timeout: {e}')
    
    try:
        fechar_popup_elemento = wait_for_element(By.XPATH,'/html/body/div[9]/div/div/div[4]/img', timeout=10)
        fechar_popup_elemento.click()
        print('Pop up fechado com segundo seletor')
    
    except TimeoutError as e:
        print(f'Erro Timeout: {e}')


def switch_to_iframe(driver, iframe_id):
    try:
        # Encontrar o IFRAME usando ID
        driver.switch_to.frame(iframe_id)
        return True  # Retorna True se a mudança para o iframe foi bem-sucedida

    except Exception as e:
        return False  # Retorna False se houver uma exceção ao mudar para o iframe

def inserir_email(email):
    try:
        #Encontrando, clicando e inserindo email no campo de login
        entrada_email = wait_for_element(By.XPATH,'//input[@id="fm-login-id"]')
        entrada_email.click()
        sleep(1)
        digitar_naturalmente(email,entrada_email)
        sleep(1)
    except:
        campo_email_2 = wait_for_element(By.XPATH,'//input[@class="cosmos-input"]')
        campo_email_2.click()
        sleep(1)
        digitar_naturalmente(email,campo_email_2)
        sleep(1)
        try:
            clik_intermediario = wait_for_element(By.XPATH,'//span[@class="nfm-multiple-email-prefix"]')
            clik_intermediario.click()
            sleep(1)
        except:
            pass
        click_continuar = wait_for_element(By.XPATH,"//span[text()='Continuar']")
        click_continuar.click()
        sleep(1)

def inserir_senha(senha):
    #Encontrando, clicando e inserindo senha no campo de senha
    entrada_senha = wait_for_element(By.XPATH,'//input[@aria-label="Senha"]')
    entrada_senha.click()
    sleep(1)
    digitar_naturalmente(senha,entrada_senha)
    sleep(3)

def hover_usuario():
    
    campo_usuario = wait_for_element(By.XPATH,"//div[@class='my-account--menuItem--1GDZChA']")
    campo_usuario.click()
    sleep(1)

#---------------Navegar até o site--------------------------------
driver, wait = iniciar_driver()
driver = uc.Chrome()
driver.get('https://pt.aliexpress.com')
sleep(1)
#-----------------------------------------------------------------

#---------------Fechando o pop up automático----------------------
fechar_popup()
#-----------------------------------------------------------------

#---------------Clicando na aba de usuário------------------------
hover_usuario()
#-----------------------------------------------------------------

#---------------Clicando em entrar na conta-----------------------
campo_entrar_na_conta = wait_for_element(By.CLASS_NAME,'my-account--signin--RiPQVPB')
campo_entrar_na_conta.click()
sleep(1)
#-----------------------------------------------------------------

#---------------Clicando e inserindo email-------------------------
inserir_email(email)
#-----------------------------------------------------------------

#---------------Clicando e inserindo senha-------------------------
inserir_senha(senha)
#-----------------------------------------------------------------

#---------------Clicando em entrar após inserir as infos----------
#Encontrando e clicando no botão de entrar
botton_entrar = wait_for_element(By.XPATH,'//button[@aria-label="Entrar"]')
botton_entrar.click()
sleep(1)
#-----------------------------------------------------------------

#-------------Resolvendo slide to verification---------------------
def resolver_slide_to_verify():
    if switch_to_iframe(driver, "baxia-dialog-content"):
        sleep(2)
        # Iniciando o ActionChains
        chain = ActionChains(driver)
        # Encontrando o elemento inicial do slide
        slide = driver.find_element(By.XPATH, '//span[@id="nc_1_n1z"]')
        sleep(2)
        # Clicando e arrastando o slide
        chain.click_and_hold(slide).move_by_offset(400, 0).release().perform()

resolver_slide_to_verify()
#-----------------------------------------------------------------

#---------------Fechando o pop up automático----------------------
sleep(6)
fechar_popup()
#-----------------------------------------------------------------

#---------------Clicando na aba de usuário------------------------
hover_usuario()
#-----------------------------------------------------------------

#---------------Clicando na aba de pedidos------------------------
lista_hover = wait_for_element(By.XPATH,"//span[@class='my-account--menuText--1km-qni']", timeout=10)
lista_hover.click()


pedidos_eviados =wait_for_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[4]', timeout=10)
pedidos_eviados.click()
sleep(2)
#-----------------------------------------------------------------


#---------------Obtendo quantidade de pedidos enviados-----------------
num_pedidos = driver.find_elements(By.XPATH,'//div[@class="order-item"]')
quantidade_pedidos = len(num_pedidos)

#Criando variaveis nulas para serem preenchidas a frente
id_final = []
pedidos = []



if quantidade_pedidos > 0:
    pedidos = (f"Atualmente você tem {quantidade_pedidos} pedidos enviados")
#-----------------Buscando o id de cada pedido-----------------------

    for ped_unico in range(1, quantidade_pedidos + 1):
        busca_id = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[{ped_unico}]/div[1]/div[2]/div/div[2]')
        id_texto = busca_id.text
        id_numeros = re.search(r'\d+', id_texto).group()
        id_final.append(id_numeros)

    # Agora associamos os IDs com os textos dos pedidos
    pedidos_dicionario = {}

    #Agora vamos rodas outro loop para obter texto de cada pedido

    for txt_unico in range(1, quantidade_pedidos + 1):
        try:
            # Buscando o texto do item do pedido
            busca_texto = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[{txt_unico}]/div[3]/div[1]/div/div[1]/a/span')
            texto_item = busca_texto.text
        except:
            # Caso não seja possível encontrar o texto, insire um texto padrão
            texto_item = f'Pedido {txt_unico} sem descrição disponível'

        id_atual = id_final[txt_unico - 1]
        pedidos_dicionario[id_atual] = texto_item
else:
    pedidos = ("No momento voce nao tem pedidos enviados")


#-------Agora com id e info sobre cada pedido vamos ao rastreamento de cada item

for pedido_id, descricao in pedidos_dicionario.items():
    driver.get(f'https://www.aliexpress.com/p/tracking/index.html?_addShare=no&_login=yes&tradeOrderId={pedido_id}')
    sleep(3)
    try:
        rastreio_encripto = wait_for_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div/div/span', timeout=10)
        rastreio = rastreio_encripto.text  # Obter o número de rastreamento
    except TimeoutException: # type: ignore # type: ignore
        rastreio = "Número de rastreio não encontrado"

    pedidos_dicionario[pedido_id] = {
        'descricao': descricao,
        'rastreamento': rastreio}

#------------Agora vamos ao status de rastreio de cada pedido -----------------------------------------------------

for pedido_id, info in pedidos_dicionario.items():
    try:
        rastreamento = info['rastreamento']  # Número de rastreamento
        driver.get(f'https://www.muambator.com.br/pacotes/{rastreamento}/detalhes/')
        sleep(2)
        status_envio_encriptado = wait_for_element(By.XPATH,'//*[@class="situacao-header"]', timeout=10)
        status_envio = status_envio_encriptado.text
        
    except TimeoutException: # type: ignore
        status_envio = 'Status do rastreio nao encontrado'

    pedidos_dicionario[pedido_id]['status_envio'] = status_envio


#--Printando oq temos ate agora
print(pedidos)
pprint.pprint(pedidos_dicionario, indent=2)


#--Ate aki tudo certo agora vamos a criacao e e envio desse relatorio por email
        
def enviar_email(destinatario, assunto, corpo):
    # Configurações do e-mail
    remetente = seu_email_email
    senha = sua_senha_email  

    mensagem = EmailMessage()
    mensagem.set_content(corpo)
    mensagem['Subject'] = assunto
    mensagem['From'] = remetente
    mensagem['To'] = destinatario

    with smtplib.SMTP('smtp.office365.com', 587) as servidor:  # Substitua smtp.example.com pelo servidor SMTP do seu e-mail
        servidor.starttls()  # Segurança
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)
        print("E-mail enviado com sucesso!") 


#- Construindo a mensagem
mensagem = ""

for pedido_id, info in pedidos_dicionario.items():
    mensagem += f"ID do Pedido: {pedido_id}\n"
    mensagem += f"Descrição: {info['descricao']}\n"
    mensagem += f"Rastreamento: {info['rastreamento']}\n"
    mensagem += f"Status de Envio: {info['status_envio']}\n"
    mensagem += "-" * 50 + "\n"  # Separador para cada pedido


#- Enviando o email

destinatario = destinatario_email
assunto = 'Relatório de Pedidos'
corpo = ""


enviar_email(destinatario, assunto, mensagem)

#  fim da automação 
driver.close()
 