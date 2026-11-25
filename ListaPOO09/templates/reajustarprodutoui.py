import streamlit as st
from service import Service


class ReajustarProdutoUI:
    @staticmethod
    def Main():
        st.header("Reajustar preços de produtos")
        ReajustarProdutoUI.Reajustar()

    @staticmethod
    def Reajustar():
        produtos = Service.produto_listar()
        if not produtos:
            st.info("Nenhum produto cadastrado.")
            return
        st.dataframe([p.to_dict() for p in produtos], hide_index=True)
        with st.form("reajuste"):
            percentual = st.number_input("Percentual (negativo para desconto)", min_value=-100.0, value=0.0, step=1.0)
            enviar = st.form_submit_button("Reajustar todos os preços")
        if enviar:
            try:
                Service.produto_reajustar(percentual)
                st.success("Preços reajustados!")
                st.dataframe([p.to_dict() for p in Service.produto_listar()], hide_index=True)
            except ValueError as erro:
                st.error(str(erro))
