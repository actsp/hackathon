import streamlit as st
import webbrowser
from io import BytesIO
import requests
import pandas as pd
import numpy as np
import webbrowser  
import smtplib
import sqlite3 
import time

from datetime import datetime
from datetime import date
import pytz
datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
t = datetime_br.strftime('%d:%m:%Y %H:%M:%S %Z %z')
d = date.today()

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib

conn = sqlite3.connect('usuarios.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS usuarios(id INT, name TEXT, mail TEXT, team TEXT, password TEXT, habilitado TEXT)')
c.execute(""" SELECT * FROM usuarios""")
data = c.fetchall()

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
    
def exibe_dados_cadastrados():
    # DB Management
    n = len(data) + 1          
    #st.write("n = " + str(n))
    if n >1:
        db = pd.DataFrame(data)
        db.columns = ['ID', 'NOME', 'MAIL', 'EQUIPE', 'SENHA', 'HABILITADO']    
        #st.dataframe(db)
        NOME =  str(db['NOME'][0])
        MAIL =  str(db['MAIL'][0])
        EQUIPE = str(db['EQUIPE'][0])
        HAB =  str(db['HABILITADO'][0])  
        return (MAIL, NOME, EQUIPE, HAB)
 
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usuarios(id INT, name TEXT, mail TEXT, team TEXT, password TEXT, habilitado TEXT)')

def add_userdata(name, email,password):
	c.execute('INSERT INTO usuarios(name, mail,password) VALUES (?, ?,?)',(name, email, password))
	conn.commit()

def login_user(email,password):
	c.execute('SELECT * FROM usuarios WHERE mail =? AND password = ?',(email,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM usuarios')
	data = c.fetchall()
	return data
       
def pesquisar_dados(email):
    # lendo os dados
    c.execute(""" SELECT * FROM usuarios WHERE mail = ?""", (email,))
    rows = c.fetchmany(size=1)
    db = pd.DataFrame(rows)
    db.columns = ['ID', 'NOME', 'MAIL', 'EQUIPE', 'SENHA', 'HABILITADO']     
    #st.dataframe(db) 
    st.success("Olá, {}".format(str(db['NOME'][0]) + ', seu login está Habilitado!'))
    hab =  str(db['HABILITADO'][0])        
    #with st.expander("Formulário para envio de dúvidas"):        
    if hab == 'S':
        return True
    else:
        return False

TITULO = '<p style="font-family:tahoma; color:blue; font-size: 26px;">MVP da Plataforma p/ o Evento Hackathon de Inovação 2023</p>'
st.markdown(TITULO, unsafe_allow_html=True)
SUB_TITULO = '<p style="font-family:tahoma; color:orange; font-size: 22px;">Inscrições até: 17/09/23 / Classificados: 05/10/23 / Final: 26/10/23</p>'
st.markdown(SUB_TITULO, unsafe_allow_html=True)
mystyle = '''
          <style>
          p {
             text-align: justify;
            }
          </style>
          '''
st.markdown(mystyle, unsafe_allow_html=True)
with st.container():
    st.write("Dados para login de usuário:")
    st.info("************ Digite seu usuário e senha e em seguida tecle ENTER para logar! ************")
    col1, col2 = st.columns((1, 1))    
    with col1:
        MAIL = st.text_input("e-mail")
    with col2:        
        password = st.text_input("Password",type='password')

def main():
    st.sidebar.image("logo.jpg")   
    st.sidebar.subheader("A Inventividade em prol da inclusão!")
    st.sidebar.info("Para fomentar a criação de ideias inovadoras que promovam a inclusão de pessoas com deficiência visual, apoiado nas tecnologias assistivas.")
    st.sidebar.write("ÁUDIO EXPLICATIVO: ")
    video_file = open('hackathon23.mp4', 'rb')
    video_bytes = video_file.read()        
    st.sidebar.video(video_bytes) 
    st.sidebar.write("Plataforma desenvolvida por: ")
    st.sidebar.info("Professor Massaki de O. Igarashi")    
    #if st.button("LOGAR"):
    if password:
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(MAIL,check_hashes(password,hashed_pswd))
        if result and pesquisar_dados(MAIL):
            #st.success("Login Habilitado!")            
            resp = exibe_dados_cadastrados()
            mail = str(resp[0])
            name = str(resp[1])
            team = str(resp[2])
            hab  = str(resp[3])
            tab1, tab2, tab3 = st.tabs(["Vídeo", "Regulamento", "Enviar Dúvidas"])
            with tab1:
                url1 = "https://www.youtube.com/watch?v=BUGjZ1hZ10Q"
                st.video(url1)
            with tab2:
                st.info("""
                        ### ***1. DEFINIÇÕES***
                        1.1 O “HACKATHON INOVAÇÃO – ACT & MACKENZIE CAMPINAS”, edição 2023, será um 2º evento, cujo evento piloto (1º Hackathon de Inovação Mackenzie Week) foi realizado de 19 a 23 de setembro de 2022, no Centro de Ciências e Tecnologia - CCT/ Mackenzie Campinas – SP e cuja data coincidiu com a tradicional Semana Mackenzie Aberto (“Mack Week”), onde estudantes matriculados no ensino médio (1º, 2º ou 3º ano) de uma escola parceira puderam inscrever, de forma independente, suas equipes e ideias inovadoras.
                        """    
                        )   
                st.write("""         
                        1.2	Será um concurso de ideias da cidade de Campinas – SP e cidades próximas 
                        """    
                        )                         
                
                st.write("""         
                        1.3	O concurso terá o objetivo de fomentar ideias inovadoras que promovam a inclusão de pessoas com deficiência visual tendo como recurso de apoio as TAs.
                        """    
                        ) 
                st.write("""         
                        1.4	Os projetos/ideias apresentadas devem ser inovadores, criativos, podem envolver também transformação digital /Tecnologia de Informação e Comunicação – TIC e também incluir como entrega um Mínimo Produto Viável  .
                        """    
                        )
                
                st.write("""         
                        1.5	Os projetos/ideias apresentadas devem ser acessíveis e, portanto, ter um baixo custo de aquisição de matérias prima e implementação, considerando que o público-alvo serão pessoas de baixa renda.
                        """    
                        )              
                st.write("""         
                        1.6	As inscrições serão abertas para todas as pessoas interessadas na temática, incluindo pessoas com deficiência visual, independentemente de serem estudantes universitários. 
                        """    
                        )  
                st.write("""         
                        1.7	Embora o Hackathon se encerre com a premiação dos participantes, a depender da viabilidade das propostas apresentadas, estas poderão compor futuramente as ações e estratégias do Programa Mobilização para Autonomia.
                        """    
                        )  
                st.write("""         
                        1.8	A presente metodologia irá compor o regulamento que irá reger o “HACKATHON INOVAÇÃO – ACT & MACKENZIE CAMPINAS”, edição 2023, nas dependências do Centro de Ciências e Tecnologia – CCT/Mackenzie Campinas e demais escolas parceiras.
                        """    
                        )  
                st.write("""         
                        1.9	Os prazos e as datas constantes neste regulamento poderão ser alterados por decisão da Equipe de Gestão e Acompanhamento do evento, que disso dará nota publicamente, através do website, via e-mail para o endereço de correio eletrônico de cada participante indicado no âmbito da inscrição e também através da coordenação da Escola do inscrito.                 
                        """    
                        )  
        else:
            st.warning("Senha incorreta ou Usuário não habilitado. Informe a organização do evento!")
            st.write("_mail to: informacoes@evento.com.br")        
if __name__ == '__main__':
	main()