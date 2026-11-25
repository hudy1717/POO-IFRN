import streamlit as st
from templates.manterclienteui import ManterClienteUI
from templates.mantercategoriaui import ManterCategoriaUI
from templates.manterprodutoui import ManterProdutoUI
from templates.reajustarprodutoui import ReajustarProdutoUI


class IndexUI:
    @staticmethod
    def Main():
        st.set_page_config(page_title="Comércio Eletrônico")
        st.title("Sistema de Comércio Eletrônico")
        opcao = st.sidebar.selectbox("Menu", ["Início", "Clientes", "Categorias", "Produtos", "Reajustar preços"])
        if opcao == "Clientes":
            ManterClienteUI.Main()
        elif opcao == "Categorias":
            ManterCategoriaUI.Main()
        elif opcao == "Produtos":
            ManterProdutoUI.Main()
        elif opcao == "Reajustar preços":
            ReajustarProdutoUI.Main()
        else:
            st.write("Selecione uma opção no menu lateral.")


if __name__ == "__main__":
    IndexUI.Main()
