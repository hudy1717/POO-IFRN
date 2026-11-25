import streamlit as st
from service import Service
from templates.manterclienteui import ManterClienteUI
from templates.mantercategoriaui import ManterCategoriaUI
from templates.manterprodutoui import ManterProdutoUI
from templates.reajustarprodutoui import ReajustarProdutoUI
from templates.contaui import ContaUI
from templates.compraui import CompraUI


class IndexUI:
    @staticmethod
    def Main():
        st.set_page_config(page_title='Comércio Eletrônico')
        Service.inicializar_admin()
        st.title('Sistema de Comércio Eletrônico')
        if 'usuario' not in st.session_state:
            st.session_state.usuario = None
        if 'carrinho' not in st.session_state:
            st.session_state.carrinho = {}
        cliente = Service.cliente_listar_id(st.session_state.usuario)
        if cliente is None:
            st.session_state.usuario = None
            st.session_state.carrinho = {}
            paginas = {'Entrar no sistema': ContaUI.Entrar, 'Abrir conta': ContaUI.Abrir}
        else:
            st.sidebar.write('Olá, ' + cliente.get_nome())
            if st.sidebar.button('Sair do sistema'):
                st.session_state.usuario = None
                st.session_state.carrinho = {}
                st.rerun()
            if cliente.get_email() == 'admin':
                paginas = {'Clientes': ManterClienteUI.Main, 'Categorias': ManterCategoriaUI.Main,
                           'Produtos': ManterProdutoUI.Main, 'Reajustar preços': ReajustarProdutoUI.Main,
                           'Listar as vendas': lambda: CompraUI.Pedidos(True)}
            else:
                paginas = {'Listar produtos': CompraUI.ListarProdutos, 'Inserir produto no carrinho': CompraUI.Inserir,
                           'Visualizar o carrinho': CompraUI.Carrinho, 'Comprar o carrinho': lambda: CompraUI.Carrinho(True),
                           'Listar minhas compras': CompraUI.Pedidos}
        opcao = st.sidebar.selectbox('Menu', list(paginas))
        paginas[opcao]()


if __name__ == '__main__':
    IndexUI.Main()
