from flask import Flask, request
from flask.globals import request
from flask_restful import Resource, Api
from models import Atividades, Pessoas, Usuarios
import json
from sqlalchemy.exc import StatementError
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verificacao(login, senha):
    print('Validando Usuário')
    if not (login, senha):
        print('Erro ao logar')
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa nao encontrada'
            }
        except KeyError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa nao encontrada'
            }
        return response

    def put(self, id):
        try:
            pessoa = Pessoas.query.filter_by(id=id).first()
            dados = json.loads(request.data)
            if 'nome' in dados:
                pessoa.nome = dados['nome']
            if 'idade' in dados:
                pessoa.idade = dados['idade']
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa nao encontrada'
            }
        except KeyError:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa nao encontrada'
            }
        return response

    def delete(self, id):
        try:
            pessoa = Pessoas.query.filter_by(id=id).first()
            pessoa.delete()
            mensagem = f'Pessoa {pessoa.nome} excluída com sucesso'
            response = {
                'status': 'sucesso',
                'mensagem': mensagem
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa nao encontrada'
            }
        except KeyError:
            response = {
                'status': 'erro',
                'mensagem': 'Pessoa nao encontrada'
            }
        return response

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response

    def post(self):
        try:
            dados = json.loads(request.data)
            pessoa =  Pessoas(nome=dados['nome'], idade=dados['idade'])
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
        except AttributeError:
            mensagem = 'Dados invalidos'
            response = {
                'status': 'erro',
                'mensagem': mensagem
            }
        except KeyError:
            mensagem = 'Dados invalidos'
            response = {
                'status': 'erro',
                'mensagem': mensagem
            }
        return response

class AtividadePorPessoa(Resource):
    @auth.login_required
    def get(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()
        atividades = Atividades.query.filter_by(pessoa=pessoa)
        response = [{'id': i.id, 'nome': i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        return response

class ListaAtividades(Resource):
    @auth.login_required
    def get(self):
        try:
            atividades = Atividades.query.all()
            response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome}  for i in atividades]
            
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Atividades nao foram encontradas'
            }
        
        return response

    def post(self):
        try:
            dados = json.loads(request.data)
            pessoa = Pessoas.query.filter_by(id=dados['pessoa_id']).first()
            atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
            if 'status' in dados:
                atividade.status = dados['status']
            atividade.save()
            response = {
                'id':atividade.id,
                'pessoa':atividade.pessoa.nome,
                'nome':atividade.nome,
                'status': atividade.status
            }
        except StatementError:
            response = {
                'status': 'erro',
                'mensagem': 'Dado invalido'
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Dados nao encontrados'
            }
        except KeyError:
            response = {
                'status': 'erro',
                'mensagem': 'Dados nao encontrados'
            }
        return response

class Atividade(Resource):
    @auth.login_required
    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        try:
            response = {
                'id':atividade.id,
                'pessoa':atividade.pessoa.nome,
                'nome':atividade.nome,
                'status': atividade.status
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Atividade nao encontrada'
            }
        except KeyError:
            response = {
                'status': 'error',
                'mensagem': 'Atividade nao encontrada'
            }
        return response

    def delete(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            atividade.delete()
            mensagem = f'Atividade {atividade.nome} excluída com sucesso'
            response = {
                'status': 'sucesso',
                'mensagem': mensagem
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Atividade nao encontrada'
            }
        except KeyError:
            response = {
                'status': 'erro',
                'mensagem': 'Atividade nao encontrada'
            }
        return response

    def put(self, id):
        try:
            atividade = Atividades.query.filter_by(id=id).first()
            dados = json.loads(request.data)
            if 'status' in dados:
                atividade.status = dados['status']
            atividade.save()
            response = {
                'id': atividade.id,
                'nome': atividade.nome,
                'pessoa':atividade.pessoa.nome,
                'status': atividade.status
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Atividade nao encontrada'
            }
        except KeyError:
            response = {
                'status': 'erro',
                'mensagem': 'Atividade nao encontrada'
            }
        except StatementError:
            response = {
                'status': 'erro',
                'mensagem': 'Dado invalido'
            }
        return response


api.add_resource(Pessoa, '/pessoa/<int:id>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(AtividadePorPessoa, '/pessoa/<int:id>/atividades/')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(Atividade, '/atividades/<int:id>/')


if __name__ == "__main__":
    app.run(debug=True)