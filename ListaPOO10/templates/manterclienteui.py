import streamlit as st
from service import Service


class ManterClienteUI:
    @staticmethod
    def Main():
        st.header("Cadastro de clientes")
        op = st.radio("Operação", ["Listar", "Inserir", "Atualizar", "Excluir"], horizontal=True)
        if op == "Listar":
            ManterClienteUI.Listar()
        elif op == "Inserir":
            ManterClienteUI.Inserir()
        elif op == "Atualizar":
            ManterClienteUI.Atualizar()
        else:
            ManterClienteUI.Excluir()

    @staticmethod
    def Listar():
        objetos = Service.cliente_listar()
        if objetos:
            st.dataframe([{k: v for k, v in obj.to_dict().items() if k != "senha"} for obj in objetos], hide_index=True)
        else:
            st.info("Nenhum registro cadastrado.")

    @staticmethod
    def Inserir():
        with st.form("cliente_inserir"):
            nome = st.text_input("Nome", value="")
            email = st.text_input("E-mail", value="")
            fone = st.text_input("Telefone", value="")
            senha = st.text_input("Senha", type="password")
            enviar = st.form_submit_button("Inserir")
        if enviar:
            if not nome.strip() or not email.strip() or not fone.strip():
                st.warning("Preencha todos os campos.")
                return
            try:
                Service.cliente_inserir(nome, email, fone, senha)
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))

    @staticmethod
    def Atualizar():
        objetos = Service.cliente_listar()
        if not objetos:
            st.info("Nenhum registro cadastrado.")
            return
        obj = st.selectbox("Selecione o registro", objetos, format_func=str)
        with st.form("cliente_atualizar"):
            nome = st.text_input("Nome", value=obj.get_nome())
            email = st.text_input("E-mail", value=obj.get_email())
            fone = st.text_input("Telefone", value=obj.get_fone())
            enviar = st.form_submit_button("Atualizar")
        if enviar:
            if not nome.strip() or not email.strip() or not fone.strip():
                st.warning("Preencha todos os campos.")
                return
            try:
                Service.cliente_atualizar(obj.get_id(), nome, email, fone)
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))

    @staticmethod
    def Excluir():
        objetos = Service.cliente_listar()
        if not objetos:
            st.info("Nenhum registro cadastrado.")
            return
        obj = st.selectbox("Selecione o registro", objetos, format_func=str)
        with st.form("cliente_excluir"):
            st.write(str(obj))
            confirmar = st.checkbox("Confirmo a exclusão")
            enviar = st.form_submit_button("Excluir")
        if enviar:
            if not confirmar:
                st.warning("Confirme a exclusão.")
                return
            try:
                Service.cliente_excluir(obj.get_id())
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))
