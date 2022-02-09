#=================================================
# Author: Izael Magalhaes
# CyberSecurity Analyst
# Script para validar se o site possui formulario de politica de privacidade e cookies
# 08-02-2022
# izaelbm.com.br
# Version 2.0
#=================================================

# Importando bibliotecas
from cgitb import text
from http import cookies
import json
from lib2to3.pgen2 import driver
import os
import pickle
from selenium import webdriver
from datetime import datetime

#removendo arquivos temporarios
# os.remove("./relatorio.txt")
# os.remove("./log.json")
# os.remove("./cookies.pkl")

#Instanciando o Driver
navegador = webdriver.Chrome()

#capturando a data atual
dataAtual = datetime.today().strftime('%Y-%m-%d')
        
with open("./fqdns.txt") as file:
    for fqdn in file:
       
        #chamando a URL
        navegador.get(fqdn)

        #apagando os cookies
        navegador.delete_all_cookies

        #validando se encontra o botao do cookie
        try:
            #Clicando no botao de aceite de cookie
            navegador.find_element_by_xpath('//*[@id="cookie-notice"]/div[2]/button').click()
            
        except :
            print("erro")
            
        #extraindo cookies do navegador
        pickle.dump( navegador.get_cookies() , open("cookies.pkl","wb"))

        #lendo os cookies salvos
        cookies = pickle.load(open("cookies.pkl","rb"))

        #criando um json com os cookies capturados
        with open('./log.json', 'w') as outfile:
            json.dump(cookies, outfile, indent=4, separators=(',', ':'))

        #listando os cookies para validação
        with open('./log.json') as array_cookies:
            data_cookies = json.load(array_cookies)

        #procurando cookie
        for dta in data_cookies:
            if "cmp" not in dta['name']:
                status = "NOK"
            else:
                status = "OK"
                break
        
        #validando se encontrou o cookie
        if status == "OK":
            arq = open('relatorio.txt', 'a')
            arq.write(dta['domain'] + " - [ OK ]" + " - " + dataAtual + "\n")
            arq.close()
        else:
            arq = open('relatorio.txt', 'a')
            arq.write(dta['domain'] + " - [ NOK ]" + " - " + dataAtual + "\n")
            arq.close()
                
print("Script Finalizou...")

#fechando o navegador
navegador.quit()    
