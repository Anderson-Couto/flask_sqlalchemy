from models import Pessoas, Usuarios, Atividades

# Insere dados na tabela pessoa
def insere_pessoas():
    pessoa1 = Pessoas(nome='Usuario1',idade=25)
    pessoa2 = Pessoas(nome='Usuario2',idade=42)
    pessoa3 = Pessoas(nome='Usuario3',idade=37)
    pessoa1.save()
    pessoa2.save()
    pessoa3.save()

# Insere dados na tabela atividades
def insere_atividades():
    atividade1 = Atividades(nome='Ir ao mercado',pessoa_id=1)
    atividade2 = Atividades(nome='Ir ao shopping',pessoa_id=1)
    atividade3 = Atividades(nome='Terminar o projeto',pessoa_id=2)
    atividade4 = Atividades(nome='Cozinhar',pessoa_id=2)
    atividade5 = Atividades(nome='Contratar um novo plano',pessoa_id=2)
    atividade6 = Atividades(nome='Praticar exercicios',pessoa_id=3)
    atividade1.save()
    atividade2.save()
    atividade3.save()
    atividade4.save()
    atividade5.save()
    atividade6.save()


# Realiza consulta na tabela Pessoas
def consulta_todas_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)

# Realiza consulta na tabela Atividades
def consulta_todas_atividades():
    atividades = Atividades.query.all()
    print(atividades)

# Insere usuários para acessar as requisições 
def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()


# Realiza consulta na tabela Usuarios
def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

if __name__ == '__main__':
    #---------------------#
    insere_pessoas()
    consulta_todas_pessoas()
    #---------------------#
    insere_atividades()
    consulta_todas_atividades()
    #---------------------#
    insere_usuario('admin', 'admin')
    consulta_todos_usuarios

