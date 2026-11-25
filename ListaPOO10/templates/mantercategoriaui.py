import streamlit as st
from service import Service


class ManterCategoriaUI:
    @staticmethod
    def Main():
        st.header("Cadastro de categorias")
        op = st.radio("Operação", ["Listar", "Inserir", "Atualizar", "Excluir"], horizontal=True)
        if op == "Listar":
            ManterCategoriaUI.Listar()
        elif op == "Inserir":
            ManterCategoriaUI.Inserir()
        elif op == "Atualizar":
            ManterCategoriaUI.Atualizar()
        else:
            ManterCategoriaUI.Excluir()

    @staticmethod
    def Listar():
        objetos = Service.categoria_listar()
        if objetos:
            st.dataframe([obj.to_dict() for obj in objetos], hide_index=True)
        else:
            st.info("Nenhum registro cadastrado.")

    @staticmethod
    def Inserir():
        with st.form("categoria_inserir"):
            descricao = st.text_input("Descrição", value="")
            enviar = st.form_submit_button("Inserir")
        if enviar:
            if not descricao.strip():
                st.warning("Preencha todos os campos.")
                return
            try:
                Service.categoria_inserir(descricao)
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))

    @staticmethod
    def Atualizar():
        objetos = Service.categoria_listar()
        if not objetos:
            st.info("Nenhum registro cadastrado.")
            return
        obj = st.selectbox("Selecione o registro", objetos, format_func=str)
        with st.form("categoria_atualizar"):
            descricao = st.text_input("Descrição", value=obj.get_descricao())
            enviar = st.form_submit_button("Atualizar")
        if enviar:
            if not descricao.strip():
                st.warning("Preencha todos os campos.")
                return
            try:
                Service.categoria_atualizar(obj.get_id(), descricao)
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))

    @staticmethod
    def Excluir():
        objetos = Service.categoria_listar()
        if not objetos:
            st.info("Nenhum registro cadastrado.")
            return
        obj = st.selectbox("Selecione o registro", objetos, format_func=str)
        with st.form("categoria_excluir"):
            st.write(str(obj))
            confirmar = st.checkbox("Confirmo a exclusão")
            enviar = st.form_submit_button("Excluir")
        if enviar:
            if not confirmar:
                st.warning("Confirme a exclusão.")
                return
            try:
                Service.categoria_excluir(obj.get_id())
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))
