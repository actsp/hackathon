import streamlit as st
import webbrowser
from io import BytesIO
import requests
import pandas as pd
import webbrowser  
import smtplib
import sqlite3 

import time
from datetime import datetime
from datetime import date
import pytz
from collections import defaultdict

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

datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
t = datetime_br.strftime('%d:%m:%Y %H:%M:%S %Z %z')
d = date.today()

connection = sqlite3.connect('usuarios.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios(idUSER TEXT, name TEXT, mail TEXT, team TEXT, password TEXT)")

cursor.execute("""SELECT * FROM usuarios;""")
nrows = cursor.fetchall()
n = len(nrows) +1          
st.write("n = " + str(n))
#connection.close() 

#st.success('Seu pedido está pronto!', icon="✅")
#with st.spinner('Wait for it...'):
#    time.sleep(5)
#st.success('Done!')

def exibir_dados():
    # lendo os dados
    cursor.execute("""
    SELECT * FROM usuarios;
    """)
    rows = cursor.fetchall()
    if len(rows) != 0:
        db = pd.DataFrame(rows)
        db.columns = ['ID' , 'NOME' , 'MAIL' , 'EQUIPE' , 'SENHA']
        st.dataframe(db)   
        st.write(len(db)) 
    else:
        st.write("Sem dados!")
def pesquisar_dados(nome):
    # lendo os dados
    cursor.execute(""" SELECT * FROM usuarios WHERE name = ?""", (nome,))
    rows = cursor.fetchmany(size=1)
    db = pd.DataFrame(rows)
    db.columns = ['ID' , 'NOME' , 'MAIL' , 'EQUIPE' , 'SENHA']
    #st.sidebar.dataframe(db)   
    return db

st.title("HACKATHON ACT & MACKENZIE 2023")
st.subheader("CADASTRO DE USUÁRIO")
new_name = st.text_input("Nome: ")
new_mail = st.text_input("e-mail")
new_team = st.selectbox('Selecione a Equipe:',('Equipe01', 'Equipe02', 'Equipe03', 'Equipe04', 'Equipe05', 'Equipe06', 'Equipe07', 'Equipe08', 'Equipe09','Equipe10'))
new_password = st.text_input("Senha: ",type='password')

with st.sidebar:         
    NOME = st.text_input('NOME:')
    if st.button("PESQUISAR"):
        #pesquisar_dados(NOME)
        st.sidebar.dataframe(pesquisar_dados(NOME))

    if st.button(" _DELETAR_ "):
        with connection:
            # excluindo um registro da tabela
            if DESC:
                cursor.execute("""DELETE FROM usuarios WHERE name = ?
                """, (NOME,))
                connection.commit() 
                st.write('Dados DELETADOS com sucesso.')
                time.sleep(500)
                st.write(' ')
                #connection.close()
                exibir_dados()   
 
tab1, tab2, tab3 = st.tabs(["Cadastrar", "Base Dados", "PESQ"])
with tab1:
    if st.button("SALVAR"):
        with connection:
            # inserindo dados na tabela
            cursor.execute("""
            INSERT INTO usuarios (idUSER,  name, mail, team, password )
            VALUES (?,?,?,?,?)
            """, (str(n), new_name, new_mail, new_team, make_hashes(new_password)))
        connection.commit() 
        st.write('Dados inseridos com sucesso.')
        #connection.close() 
        
    if st.button("ATUALIZAR"):
        new_ID = st.text_input("idUSER: ")
        with connection:
            # atualizando dados na tabela
            cursor.execute("""
            UPDATE usuarios SET idUSER=?, name=?, mail=?, team=?, password=?
            WHERE name = ? """, (new_ID, new_name, new_mail, new_team, new_password, new_name))
        connection.commit() 
        st.write('Dados atualizados com sucesso.')
        #connection.close()
        
with tab2:  
    exibir_dados()    

with tab3:
    Pesq_data = st.text_input('Nome a consultar: ', "Massaki de Oliveira Igarashi")
    connection = sqlite3.connect('usuarios.db')
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM usuarios WHERE name = ?""", (Pesq_data,))    
    rows = cursor.fetchall()
    if len(rows) != 0:
        db = pd.DataFrame(rows)
        db.columns = ['ID' , 'NOME' , 'MAIL' , 'EQUIPE' , 'SENHA']
        st.dataframe(db)        
        #edited_df = st.data_editor(db, num_rows="dynamic")
        #favorite_command = edited_df.loc[edited_df["EQUIPE"].idxmax()]["NOME"]
        #st.markdown(f"EQUIPE MAIOR = **{favorite_command}** 🎈")        
    else:
        st.write("Sem dados!")