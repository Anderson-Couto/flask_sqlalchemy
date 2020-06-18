from flask import Flask, request
from flask.globals import request
from flask_restful import Resource, Api
from models import Atividades, Pessoas
import json

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):
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
        return response

class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response

    def post(self):
        dados = json.loads(request.data)
        pessoa =  Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        return response

    def post(self):
        dados = json.loads(request.data)
        pessoa = Pessoas.query.filter_by(id=dados['pessoa_id']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'id':atividade.id,
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome
        }
        return response


api.add_resource(Pessoa, '/pessoa/<int:id>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')





if __name__ == "__main__":
    app.run(debug=True)