import streamlit as st
from service import Service


class ManterProdutoUI:
    @staticmethod
    def Main():
        st.header("Cadastro de produtos")
        op = st.radio("Operação", ["Listar", "Inserir", "Atualizar", "Excluir"], horizontal=True)
        if op == "Listar":
            ManterProdutoUI.Listar()
        elif op == "Inserir":
            ManterProdutoUI.Inserir()
        elif op == "Atualizar":
            ManterProdutoUI.Atualizar()
        else:
            ManterProdutoUI.Excluir()

    @staticmethod
    def Listar():
        objetos = Service.produto_listar()
        if objetos:
            st.dataframe([obj.to_dict() for obj in objetos], hide_index=True)
        else:
            st.info("Nenhum registro cadastrado.")

    @staticmethod
    def Inserir():
        categorias = Service.categoria_listar()
        if not categorias:
            st.warning("Cadastre uma categoria primeiro.")
            return
        with st.form("produto_inserir"):
            descricao = st.text_input("Descrição", value="")
            preco = st.number_input("Preço", min_value=0.0, value=float(0.0), step=0.01)
            estoque = st.number_input("Estoque", min_value=0, value=0, step=1)
            categoria = st.selectbox("Categoria", categorias, index=0, format_func=lambda c: c.get_descricao())
            idCategoria = categoria.get_id()
            enviar = st.form_submit_button("Inserir")
        if enviar:
            if not descricao.strip():
                st.warning("Preencha todos os campos.")
                return
            try:
                Service.produto_inserir(descricao, preco, estoque, idCategoria)
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))

    @staticmethod
    def Atualizar():
        objetos = Service.produto_listar()
        if not objetos:
            st.info("Nenhum registro cadastrado.")
            return
        obj = st.selectbox("Selecione o registro", objetos, format_func=str)
        categorias = Service.categoria_listar()
        if not categorias:
            st.warning("Cadastre uma categoria primeiro.")
            return
        with st.form("produto_atualizar"):
            descricao = st.text_input("Descrição", value=obj.get_descricao())
            preco = st.number_input("Preço", min_value=0.0, value=float(obj.get_preco()), step=0.01)
            estoque = st.number_input("Estoque", min_value=0, value=obj.get_estoque(), step=1)
            categoria = st.selectbox("Categoria", categorias, index=next((i for i, c in enumerate(categorias) if c.get_id() == obj.get_idCategoria()), 0), format_func=lambda c: c.get_descricao())
            idCategoria = categoria.get_id()
            enviar = st.form_submit_button("Atualizar")
        if enviar:
            if not descricao.strip():
                st.warning("Preencha todos os campos.")
                return
            try:
                Service.produto_atualizar(obj.get_id(), descricao, preco, estoque, idCategoria)
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))

    @staticmethod
    def Excluir():
        objetos = Service.produto_listar()
        if not objetos:
            st.info("Nenhum registro cadastrado.")
            return
        obj = st.selectbox("Selecione o registro", objetos, format_func=str)
        with st.form("produto_excluir"):
            st.write(str(obj))
            confirmar = st.checkbox("Confirmo a exclusão")
            enviar = st.form_submit_button("Excluir")
        if enviar:
            if not confirmar:
                st.warning("Confirme a exclusão.")
                return
            try:
                Service.produto_excluir(obj.get_id())
                st.success("Operação concluída!")
            except ValueError as erro:
                st.error(str(erro))
