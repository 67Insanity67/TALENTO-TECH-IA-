import streamlit as st  
from groq import Groq 

st.set_page_config(page_title="Pale Luna", page_icon="9️⃣", layout="centered") 

nombre = st.text_input("¿Cuál es tu nombre?")

if st.button("Saludar"): 
    st.subheader(f"Hola {nombre}! es un gusto verte")  

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'] 


def configurar_pagina():
    st.title("proyecto de Lucas Badii") 
    st.sidebar.title("Pale Luna")
    elegirModelo = st.sidebar.selectbox('Selecciona un modelo', options=MODELOS, index=0)
    return elegirModelo 

def crear_usuario_groq():
    claveSecreta = st.secrets["CLAVE_API"] 
    return Groq(api_key=claveSecreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create( 
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True 
    )

def inicializar_estado():
    if "mensajes" not in st.session_state: 
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})


def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]): 
            st.markdown(mensaje["content"])

def area_chat():
    chat_container = st.container() 
    with chat_container:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "" 
    for frase in chat_completo: 
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content 
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina() 


    clienteUsuario = crear_usuario_groq() 
    inicializar_estado()


    mensaje = st.chat_input("Escribí tu mensaje: ") 


    area_chat() 
    if mensaje: 
        actualizar_historial("user", mensaje, "🧑‍💻") 


        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) 


        if chat_completo:
            with st.chat_message("assistant"):  
                respuesta_generada = st.write_stream(generar_respuesta(chat_completo)) 
                actualizar_historial("assistant", respuesta_generada, "🌚")



if __name__ == "__main__":
    main()