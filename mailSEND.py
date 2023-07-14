import streamlit as st
import webbrowser
from io import BytesIO
import requests
import pandas as pd
import webbrowser  

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def SendMAIL(assunto):
    # create message object instance 
    msg = MIMEMultipart()
     
    # setup the parameters of the message 
    password = "ptqyoxzsevhenysh"
    msg['From'] = "prof.massakigmail.com"
    msg['To'] = "massaki.igarashi@gmail.com"
    msg['Subject'] = str(assunto)
    #file = "Python.pdf"
    # attach image to message body 
    #msg.attach(MIMEText(open(file).read()))     
    
    # create server 
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail 
    server.login(msg['From'], password)         
    # send the message via the server. 
    server.sendmail(msg['From'], msg['To'], msg.as_string("MENSAGEM TESTE"))
    server.quit()

st.set_page_config(
     page_title="e-mail TESTE",
     page_icon=":date:",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'mailto:prof.massaki@gmail.com',
         'Report a bug': "mailto:prof.massaki@gmail.com",
         'About': "#### Desenvolvedor: prof. Massaki de O. Igarashi"
     }
 )


if st.button('ENVIAR'): 
    #webbrowser.open(url)
    SendMAIL("Mensagem Teste")
    web = webbrowser.get('chrome')  
    web.open(url)      
    