from datetime import datetime
from hashlib import pbkdf2_hmac
from secrets import token_hex
from hmac import compare_digest
from threading import RLock
from models import Venda, VendaItem, VendaDAO
from models import Cliente, Categoria, Produto, ClienteDAO, CategoriaDAO, ProdutoDAO


class Service:
    trava = RLock()
    @staticmethod
    def proximo_id(dao):
        objetos = dao.Listar()
        return max((o.get_id() for o in objetos), default=0) + 1

    @staticmethod
    def cliente_inserir(nome: str, email: str, fone: str, senha: str = "") -> None:
        email = email.strip().lower()
        if not nome.strip() or not email or not fone.strip() or not senha:
            raise ValueError("Preencha todos os campos, inclusive a senha.")
        if any(c.get_email() == email for c in ClienteDAO.Listar()):
            raise ValueError("E-mail já cadastrado.")
        ClienteDAO.Inserir(Cliente(Service.proximo_id(ClienteDAO), nome, email, fone, Service.hash_senha(senha)))

    @staticmethod
    def cliente_listar() -> list:
        return ClienteDAO.Listar()

    @staticmethod
    def cliente_listar_id(id: int):
        return ClienteDAO.Listar_Id(id)

    @staticmethod
    def cliente_atualizar(id: int, nome: str, email: str, fone: str) -> None:
        if ClienteDAO.Listar_Id(id) is None:
            raise ValueError('Cliente não encontrado.')
        atual = ClienteDAO.Listar_Id(id)
        email = email.strip().lower()
        if atual.get_email() == "admin" and email != "admin" or email == "admin" and atual.get_email() != "admin":
            raise ValueError("Não é possível alterar o perfil administrativo.")
        if any(c.get_email() == email and c.get_id() != id for c in ClienteDAO.Listar()):
            raise ValueError("E-mail já cadastrado.")
        ClienteDAO.Atualizar(Cliente(id, nome, email, fone, atual.get_senha()))

    @staticmethod
    def cliente_excluir(id: int) -> None:
        obj = ClienteDAO.Listar_Id(id)
        if obj is None:
            raise ValueError('Cliente não encontrado.')
        if obj.get_email() == "admin" or any(v.idCliente == id for v in VendaDAO.Listar()):
            raise ValueError("Cliente administrador ou com vendas não pode ser excluído.")
        ClienteDAO.Excluir(obj)

    @staticmethod
    def categoria_inserir(descricao: str) -> None:
        CategoriaDAO.Inserir(Categoria(Service.proximo_id(CategoriaDAO), descricao))

    @staticmethod
    def categoria_listar() -> list:
        return CategoriaDAO.Listar()

    @staticmethod
    def categoria_listar_id(id: int):
        return CategoriaDAO.Listar_Id(id)

    @staticmethod
    def categoria_atualizar(id: int, descricao: str) -> None:
        if CategoriaDAO.Listar_Id(id) is None:
            raise ValueError('Categoria não encontrada.')
        CategoriaDAO.Atualizar(Categoria(id, descricao))

    @staticmethod
    def categoria_excluir(id: int) -> None:
        obj = CategoriaDAO.Listar_Id(id)
        if obj is None:
            raise ValueError('Categoria não encontrada.')
        if any(p.get_idCategoria() == id for p in ProdutoDAO.Listar()):
            raise ValueError('Categoria possui produtos cadastrados.')
        CategoriaDAO.Excluir(obj)

    @staticmethod
    def produto_inserir(descricao: str, preco: float, estoque: int, idCategoria: int) -> None:
        Service.validar_produto(preco, estoque, idCategoria)
        ProdutoDAO.Inserir(Produto(Service.proximo_id(ProdutoDAO), descricao, preco, estoque, idCategoria))

    @staticmethod
    def produto_listar() -> list:
        return ProdutoDAO.Listar()

    @staticmethod
    def produto_listar_id(id: int):
        return ProdutoDAO.Listar_Id(id)

    @staticmethod
    def validar_produto(preco, estoque, idCategoria):
        if preco < 0 or estoque < 0:
            raise ValueError('Preço e estoque não podem ser negativos.')
        if CategoriaDAO.Listar_Id(idCategoria) is None:
            raise ValueError('Categoria não encontrada. Cadastre a categoria primeiro.')

    @staticmethod
    def produto_atualizar(id: int, descricao: str, preco: float, estoque: int, idCategoria: int) -> None:
        if ProdutoDAO.Listar_Id(id) is None:
            raise ValueError('Produto não encontrado.')
        Service.validar_produto(preco, estoque, idCategoria)
        ProdutoDAO.Atualizar(Produto(id, descricao, preco, estoque, idCategoria))

    @staticmethod
    def produto_excluir(id: int) -> None:
        obj = ProdutoDAO.Listar_Id(id)
        if obj is None:
            raise ValueError('Produto não encontrado.')
        ProdutoDAO.Excluir(obj)

    @staticmethod
    def produto_reajustar(percentual: float) -> None:
        if percentual < -100:
            raise ValueError('O desconto não pode ultrapassar 100%.')
        produtos = ProdutoDAO.Listar()
        for produto in produtos:
            produto.set_preco(round(produto.get_preco() * (1 + percentual / 100), 2))
        ProdutoDAO.objetos = produtos
        ProdutoDAO.Salvar()

    @staticmethod
    def hash_senha(senha, sal=None):
        sal = sal or token_hex(16)
        return sal + ':' + pbkdf2_hmac('sha256', senha.encode(), bytes.fromhex(sal), 200000).hex()

    @staticmethod
    def autenticar(email, senha):
        for c in ClienteDAO.Listar():
            if c.get_email() == email.strip().lower() and ':' in c.get_senha():
                if compare_digest(c.get_senha(), Service.hash_senha(senha, c.get_senha().split(':')[0])):
                    return c
        return None

    @staticmethod
    def abrir_conta(nome, email, fone, senha):
        if email.strip().lower() == 'admin':
            raise ValueError('E-mail reservado ao administrador.')
        Service.cliente_inserir(nome, email, fone, senha)

    @staticmethod
    def inicializar_admin():
        if not any(c.get_email() == 'admin' for c in ClienteDAO.Listar()):
            Service.cliente_inserir('Administrador', 'admin', '000', 'admin123')

    @staticmethod
    def itens_carrinho(carrinho):
        itens = []
        for id, quantidade in carrinho.items():
            p = ProdutoDAO.Listar_Id(id)
            if p is None or quantidade <= 0 or quantidade > p.get_estoque():
                raise ValueError('Produto indisponível ou quantidade superior ao estoque.')
            itens.append(VendaItem(id, p.get_descricao(), quantidade, p.get_preco()))
        return itens

    @staticmethod
    def comprar(idCliente, carrinho):
        with Service.trava:
            cliente = ClienteDAO.Listar_Id(idCliente)
            if cliente is None or cliente.get_email() == 'admin' or not carrinho:
                raise ValueError('Compra inválida.')
            itens = Service.itens_carrinho(carrinho)
            venda = Venda(Service.proximo_id(VendaDAO), idCliente, datetime.now().isoformat(timespec='seconds'), itens)
            produtos = ProdutoDAO.Listar()
            for p in produtos:
                if p.get_id() in carrinho:
                    p.set_estoque(p.get_estoque() - carrinho[p.get_id()])
            ProdutoDAO.objetos = produtos
            ProdutoDAO.Salvar()
            VendaDAO.Inserir(venda)
            return venda

    @staticmethod
    def vendas_listar():
        return VendaDAO.Listar()

    @staticmethod
    def minhas_compras(idCliente):
        return [v for v in VendaDAO.Listar() if v.idCliente == idCliente]
