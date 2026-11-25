import streamlit as st
from service import Service


class ContaUI:
    @staticmethod
    def Entrar():
        st.header('Entrar no sistema')
        with st.form('login'):
            email = st.text_input('E-mail')
            senha = st.text_input('Senha', type='password')
            enviar = st.form_submit_button('Entrar')
        if enviar:
            cliente = Service.autenticar(email, senha)
            if cliente is None:
                st.error('E-mail ou senha incorretos.')
            else:
                st.session_state.usuario = cliente.get_id()
                st.session_state.carrinho = {}
                st.rerun()

    @staticmethod
    def Abrir():
        st.header('Abrir conta')
        with st.form('conta'):
            nome = st.text_input('Nome')
            email = st.text_input('E-mail')
            fone = st.text_input('Telefone')
            senha = st.text_input('Senha', type='password')
            enviar = st.form_submit_button('Cadastrar')
        if enviar:
            try:
                Service.abrir_conta(nome, email, fone, senha)
                st.success('Conta criada. Entre pelo menu lateral.')
            except ValueError as e:
                st.error(str(e))
