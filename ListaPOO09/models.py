import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


class Cliente:
    def __init__(self, id: int, nome: str, email: str, fone: str):
        self.__id, self.__nome, self.__email, self.__fone = id, nome, email, fone

    def get_id(self): return self.__id
    def set_id(self, id): self.__id = id
    def get_nome(self): return self.__nome
    def set_nome(self, nome): self.__nome = nome
    def get_email(self): return self.__email
    def set_email(self, email): self.__email = email
    def get_fone(self): return self.__fone
    def set_fone(self, fone): self.__fone = fone
    def ToString(self): return f'ID: {self.__id} | Nome: {self.__nome} | Email: {self.__email} | Fone: {self.__fone}'
    def __str__(self): return self.ToString()
    def to_dict(self): return {'id': self.__id, 'nome': self.__nome, 'email': self.__email, 'fone': self.__fone}
    @staticmethod
    def from_dict(d): return Cliente(d['id'], d['nome'], d['email'], d['fone'])


class Categoria:
    def __init__(self, id: int, descricao: str):
        self.__id, self.__descricao = id, descricao

    def get_id(self): return self.__id
    def set_id(self, id): self.__id = id
    def get_descricao(self): return self.__descricao
    def set_descricao(self, descricao): self.__descricao = descricao
    def ToString(self): return f'ID: {self.__id} | Descrição: {self.__descricao}'
    def __str__(self): return self.ToString()
    def to_dict(self): return {'id': self.__id, 'descricao': self.__descricao}
    @staticmethod
    def from_dict(d): return Categoria(d['id'], d['descricao'])


class Produto:
    def __init__(self, id: int, descricao: str, preco: float, estoque: int, idCategoria: int):
        self.__id, self.__descricao, self.__preco = id, descricao, preco
        self.__estoque, self.__idCategoria = estoque, idCategoria

    def get_id(self): return self.__id
    def set_id(self, id): self.__id = id
    def get_descricao(self): return self.__descricao
    def set_descricao(self, descricao): self.__descricao = descricao
    def get_preco(self): return self.__preco
    def set_preco(self, preco): self.__preco = preco
    def get_estoque(self): return self.__estoque
    def set_estoque(self, estoque): self.__estoque = estoque
    def get_idCategoria(self): return self.__idCategoria
    def set_idCategoria(self, idCategoria): self.__idCategoria = idCategoria
    def ToString(self): return f'ID: {self.__id} | Descrição: {self.__descricao} | Preço: R$ {self.__preco:.2f} | Estoque: {self.__estoque} | Categoria: {self.__idCategoria}'
    def __str__(self): return self.ToString()
    def to_dict(self): return {'id': self.__id, 'descricao': self.__descricao, 'preco': self.__preco, 'estoque': self.__estoque, 'idCategoria': self.__idCategoria}
    @staticmethod
    def from_dict(d): return Produto(d['id'], d['descricao'], d['preco'], d['estoque'], d['idCategoria'])


class DAO:
    objetos = []
    arquivo = ''
    modelo = None

    @classmethod
    def Abrir(cls):
        try:
            with open(cls.arquivo, 'r', encoding='utf-8') as f:
                cls.objetos = [cls.modelo.from_dict(d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            cls.objetos = []

    @classmethod
    def Salvar(cls):
        with open(cls.arquivo, 'w', encoding='utf-8') as f:
            json.dump([o.to_dict() for o in cls.objetos], f, ensure_ascii=False, indent=4)

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        cls.objetos.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.objetos

    @classmethod
    def Listar_Id(cls, id):
        for obj in cls.Listar():
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj):
        cls.Abrir()
        for i, atual in enumerate(cls.objetos):
            if atual.get_id() == obj.get_id():
                cls.objetos[i] = obj
                cls.Salvar()
                return

    @classmethod
    def Excluir(cls, obj):
        cls.Abrir()
        cls.objetos = [atual for atual in cls.objetos if atual.get_id() != obj.get_id()]
        cls.Salvar()


class ClienteDAO(DAO):
    arquivo = BASE / 'clientes.json'
    modelo = Cliente


class CategoriaDAO(DAO):
    arquivo = BASE / 'categorias.json'
    modelo = Categoria


class ProdutoDAO(DAO):
    arquivo = BASE / 'produtos.json'
    modelo = Produto
