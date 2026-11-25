import streamlit as st
from service import Service


class CompraUI:
    @staticmethod
    def ListarProdutos():
        st.header('Produtos disponíveis')
        produtos = Service.produto_listar()
        if produtos:
            st.dataframe([p.to_dict() for p in produtos], hide_index=True)
        else:
            st.info('Nenhum produto cadastrado.')

    @staticmethod
    def Inserir():
        st.header('Inserir produto no carrinho')
        produtos = [p for p in Service.produto_listar() if p.get_estoque() > 0]
        if not produtos:
            st.info('Nenhum produto disponível.')
            return
        p = st.selectbox('Produto', produtos, format_func=str)
        quantidade = st.number_input('Quantidade', min_value=1, max_value=p.get_estoque(), step=1)
        if st.button('Adicionar'):
            carrinho = st.session_state.carrinho.copy()
            id = p.get_id()
            carrinho[id] = carrinho.get(id, 0) + quantidade
            try:
                Service.itens_carrinho(carrinho)
                st.session_state.carrinho = carrinho
                st.success('Produto adicionado.')
            except ValueError as e:
                st.error(str(e))

    @staticmethod
    def Carrinho(comprar=False):
        st.header('Comprar o carrinho' if comprar else 'Meu carrinho')
        carrinho = st.session_state.carrinho
        if not carrinho:
            st.info('Carrinho vazio.')
            return
        try:
            itens = Service.itens_carrinho(carrinho)
            st.dataframe([i.to_dict() for i in itens], hide_index=True)
            st.write(f'Total: R$ {sum(i.preco * i.quantidade for i in itens):.2f}')
            if comprar and st.button('Confirmar compra'):
                venda = Service.comprar(st.session_state.usuario, carrinho)
                st.session_state.carrinho = {}
                st.success(f'Compra {venda.get_id()} realizada!')
                return
        except ValueError as e:
            st.error(str(e))
        if st.button('Esvaziar carrinho'):
            st.session_state.carrinho = {}
            st.rerun()

    @staticmethod
    def Pedidos(admin=False):
        st.header('Vendas' if admin else 'Minhas compras')
        vendas = Service.vendas_listar() if admin else Service.minhas_compras(st.session_state.usuario)
        if not vendas:
            st.info('Nenhum pedido registrado.')
        for v in vendas:
            with st.expander(f'Pedido {v.id} | {v.data} | R$ {v.total():.2f}'):
                if admin:
                    st.write(f'Cliente: {v.idCliente}')
                st.dataframe([i.to_dict() for i in v.itens], hide_index=True)
