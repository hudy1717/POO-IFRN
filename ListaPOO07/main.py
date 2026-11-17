from service import Service


class UI:
    @staticmethod
    def Menu():
        print('\n--- SISTEMA DE COMÉRCIO ELETRÔNICO ---')
        print('1 - Listar clientes       2 - Inserir cliente')
        print('3 - Atualizar cliente     4 - Excluir cliente')
        print('5 - Listar categorias     6 - Inserir categoria')
        print('7 - Atualizar categoria   8 - Excluir categoria')
        print('9 - Listar produtos      10 - Inserir produto')
        print('11 - Atualizar produto   12 - Excluir produto')
        print('13 - Reajustar preços     0 - Sair')
        return int(input('Informe a opção: '))

    @staticmethod
    def listar(objetos):
        if not objetos:
            print('Nenhum registro cadastrado.')
        for obj in objetos:
            print(obj.ToString())

    @staticmethod
    def Cliente_Inserir():
        Service.cliente_inserir(input('Nome: '), input('Email: '), input('Fone: '))

    @staticmethod
    def Cliente_Listar():
        UI.listar(Service.cliente_listar())

    @staticmethod
    def Cliente_Atualizar():
        id = int(input('ID: '))
        Service.cliente_atualizar(id, input('Novo nome: '), input('Novo email: '), input('Novo fone: '))

    @staticmethod
    def Cliente_Excluir():
        Service.cliente_excluir(int(input('ID: ')))

    @staticmethod
    def Categoria_Inserir():
        Service.categoria_inserir(input('Descrição: '))

    @staticmethod
    def Categoria_Listar():
        UI.listar(Service.categoria_listar())

    @staticmethod
    def Categoria_Atualizar():
        Service.categoria_atualizar(int(input('ID: ')), input('Nova descrição: '))

    @staticmethod
    def Categoria_Excluir():
        Service.categoria_excluir(int(input('ID: ')))

    @staticmethod
    def Produto_Inserir():
        descricao = input('Descrição: ')
        preco = float(input('Preço: ').replace(',', '.'))
        estoque = int(input('Estoque: '))
        categoria = int(input('ID da categoria: '))
        Service.produto_inserir(descricao, preco, estoque, categoria)

    @staticmethod
    def Produto_Listar():
        UI.listar(Service.produto_listar())

    @staticmethod
    def Produto_Atualizar():
        id = int(input('ID: '))
        descricao = input('Nova descrição: ')
        preco = float(input('Novo preço: ').replace(',', '.'))
        estoque = int(input('Novo estoque: '))
        categoria = int(input('Novo ID da categoria: '))
        Service.produto_atualizar(id, descricao, preco, estoque, categoria)

    @staticmethod
    def Produto_Excluir():
        Service.produto_excluir(int(input('ID: ')))

    @staticmethod
    def Produto_Reajustar():
        percentual = float(input('Percentual (negativo para promoção): ').replace(',', '.'))
        Service.produto_reajustar(percentual)

    @staticmethod
    def Main():
        operacoes = {
            1: UI.Cliente_Listar, 2: UI.Cliente_Inserir,
            3: UI.Cliente_Atualizar, 4: UI.Cliente_Excluir,
            5: UI.Categoria_Listar, 6: UI.Categoria_Inserir,
            7: UI.Categoria_Atualizar, 8: UI.Categoria_Excluir,
            9: UI.Produto_Listar, 10: UI.Produto_Inserir,
            11: UI.Produto_Atualizar, 12: UI.Produto_Excluir,
            13: UI.Produto_Reajustar,
        }
        while True:
            try:
                op = UI.Menu()
                if op == 0:
                    print('Programa finalizado.')
                    break
                if op not in operacoes:
                    print('Opção inválida!')
                    continue
                operacoes[op]()
                print('Operação concluída!')
            except ValueError as erro:
                print(f'Entrada inválida: {erro}')
            except (KeyboardInterrupt, EOFError):
                print('\nPrograma finalizado.')
                break


if __name__ == '__main__':
    UI.Main()
