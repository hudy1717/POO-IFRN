from models import Cliente, Categoria, Produto, ClienteDAO, CategoriaDAO, ProdutoDAO


class Service:
    @staticmethod
    def proximo_id(dao):
        objetos = dao.Listar()
        return max((o.get_id() for o in objetos), default=0) + 1

    @staticmethod
    def cliente_inserir(nome: str, email: str, fone: str) -> None:
        ClienteDAO.Inserir(Cliente(Service.proximo_id(ClienteDAO), nome, email, fone))

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
        ClienteDAO.Atualizar(Cliente(id, nome, email, fone))

    @staticmethod
    def cliente_excluir(id: int) -> None:
        obj = ClienteDAO.Listar_Id(id)
        if obj is None:
            raise ValueError('Cliente não encontrado.')
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
