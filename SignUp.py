import streamlit as st
import webbrowser
from io import BytesIO
import requests
import pandas as pd
import webbrowser  
import smtplib
import sqlite3 
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
    
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
     
# DB Management
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS usuarios(id INT, name TEXT, mail TEXT, team TEXT, password TEXT, habilitado TEXT)')
c.execute('SELECT * FROM usuarios ORDER BY name')
data = c.fetchall()
n = len(data) + 1          
st.write("n = " + str(n))
if n >1:
    db = pd.DataFrame(data)
    db.columns = ['ID', 'NOME', 'MAIL', 'EQUIPE', 'SENHA', 'HABILITADO']    
    st.dataframe(db)

# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS usuarios(id INT, name TEXT, mail TEXT, team TEXT, password TEXT, habilitado TEXT)')

def add_userdata(ID, name, mail,equipe, password, habilitado):
	c.execute('INSERT INTO usuarios(id, name, mail, team, password, habilitado) VALUES (?, ?, ?, ?, ?, ?)',(ID, name, mail, equipe, password, habilitado))
	conn.commit()

def login_user(mail,password):
	c.execute('SELECT * FROM usuarios WHERE mail =? AND password = ?',(mail,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM usuarios')
	data = c.fetchall()
	return data   
 
st.title("HACKATHON ACT & MACKENZIE 2023")
st.subheader("CADASTRO DE USUÁRIO")
new_id = st.text_input("ID: ", int(n))
new_name = st.text_input("Nome: ")
new_user = st.text_input("e-mail")
#new_team = st.selectbox('Selecione a Equipe:',('Equipe01', 'Equipe02', 'Equipe03', 'Equipe04', 'Equipe05', 'Equipe06', 'Equipe07', 'Equipe08', 'Equipe09','Equipe10'))
new_team = "Equipe01"
new_password = st.text_input("Senha: ",type='password')
new_hab = "-"
#user_result = view_all_users()
#db = pd.DataFrame(user_result,columns=["NOME", "MAIL", "EQUIPE", "SENHA", "HABILITADO"])
#st.dataframe(b)   
 
if st.button("Signup"):
	create_usertable()
	add_userdata(new_id, new_name, new_user, new_team, make_hashes(new_password), new_hab)
	st.success("Conta cadastrada com sucesso")        
	st.info("Para logar acesse página de Login")    
       
if st.button(" _DELETAR_ "):
    c = conn.cursor()
    c.execute('DELETE FROM usuarios')
    conn.commit()            
    st.write('Dados DELETADOS com sucesso!')    
    