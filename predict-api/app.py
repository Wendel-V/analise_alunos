from operator import le
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import os


import pickle
## carregando o modelo para o código
with open("predict-api/utils/model.pickle","rb") as f:
    modelo_carregado = pickle.load(f)

app = Flask(__name__)

app_infos = dict(version='1.0', title='Predict API',
        description='API que prevê o conteudo ideal para um aluno',
        contact_email='wendeline2@gmail.com', doc='/documentacao',
        prefix='/eee')


rest_app = Api(app, **app_infos)


db_model = rest_app.model('Variáveis usadas no modelo', 
	{'idade': fields.String,
  'sexo_fem': fields.String,
  'sexo_masc': fields.String,
  'sexo_na': fields.String,
  'ano': fields.String,
  'numirmaos': fields.String,
  'lelivros': fields.String,
  'lehqs': fields.String,
  'ouvemusicas': fields.String,
  've filmes e series': fields.String,
  'ler ou ver filmes e series': fields.String,
  'materia preferida': fields.String,
  'rede social preferida': fields.String,
  'horas diarias no cel': fields.String,
  'tipo de video no yt': fields.String,
  'tipo de jogo preferido': fields.String,
  'tempo médio para responder cada questão': fields.String}
  )


#ENDPOINTS

#EXEMPLO VIDEO = [15.0, 0.0, 1.0, 0.0, 6.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 1.0, 3.0, 4.0, 2.0, 77.07399999999998]
#EXEMPLO TEXTO = [16.0, 1.0, 0.0, 0.0, 7.0, 1.0, 1.0, 0.0, 1.0, 1.0, 2.0, 2.0, 1.0, 3.0, 2.0, 1.0, 91.73]
#EXEMPLO IMAGEM = [13.0, 1.0, 0.0, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 3.0, 1.0, 3.0, 70.188]
nome_do_endpoint = rest_app.namespace('Previsao de conteúdo para aluno',
                                      description='Insira os dados.')
@nome_do_endpoint.route("/")
class Classe_que_contem_funcoes(Resource):
    @rest_app.expect(db_model)


    def post(self):
        #array = request.json['array']
        idade = request.json['idade']
        sfem = request.json['sexo_fem']
        smasc = request.json['sexo_masc']
        sna = request.json['sexo_na']
        anoint = request.json['ano']
        numirmaosint = request.json['numirmaos']
        lelivros = request.json['lelivros']
        lehqs = request.json['lehqs']
        ouvemusicas = request.json['ouvemusicas']
        vefilmeserie = request.json['ve filmes e series']
        lerouverfilmeserieint = request.json['ler ou ver filmes e series']
        materiaint = request.json['materia preferida']
        redesocialint = request.json['rede social preferida']
        horascelint = request.json['horas diarias no cel']
        videoytint = request.json['tipo de video no yt']
        jogosint = request.json['tipo de jogo preferido']
        tmedio = request.json['tempo médio para responder cada questão']
        #APLICANDO O ALGORITMO
        array = np.array([idade, sfem, smasc, sna, anoint, numirmaosint, lelivros, lehqs, ouvemusicas, vefilmeserie, lerouverfilmeserieint, materiaint, redesocialint, horascelint, videoytint, jogosint, tmedio], dtype='float')
        #array = np.array(array, dtype = 'float')
        #array_do_usuario = [16.0, 0.0, 1.0, 0.0, 2.0, 1.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 3.0, 1.0, 3.0, 90.291999999999994]
        #array_do_usuario = [17.0, 1.0, 0.0, 0.0, 7.0, 0.0, 1.0, 0.0, 1.0, 1.0, 2.0, 5.0, 2.0, 3.0, 2.0, 4.0, 56.03599999999999]

        array = pd.Series(array)
        array = pd.DataFrame(array).T

        colunas = {0:'idade', 1:'sfem', 2:'smasc', 3:'sna', 4:'anoint', 5:'numirmaosint', 6:'lelivros',
              7:'lehqs', 8:'ouvemusicas', 9:'vefilmeserie', 10:'lerouverfilmeserieint',
              11:'materiaint', 12:'redesocialint', 13:'horascelint', 14:'videoytint', 15:'jogosint',
              16:'tmedio'}

        array = array.rename(columns = colunas)


        pred = modelo_carregado.predict(array)[0]
        
        if pred == 0 : result = 'VIDEO'
        elif pred == 1 : result = 'TEXTO'
        else : result = 'IMAGEM'

        return {
                'idade':idade,
                'sexo_fem' : sfem,
                'sexo_masc': smasc,
                'sexo_na': sna,
                'ano': anoint,
                'numirmaos': numirmaosint,
                'lelivros': lelivros,
                'lehqs': lehqs,
                'ouvemusicas': ouvemusicas,
                've filmes e series': vefilmeserie,
                'ler ou ver filmes e series': lerouverfilmeserieint,
                'materia preferida': materiaint,
                'rede social preferida': redesocialint,
                'horas diarias no cel': horascelint,
                'tipo de video no yt': videoytint,
                'tipo de jogo preferido': jogosint,
                'tempo médio para responder cada questão': tmedio,

                'PREDITO' : f'O conteúdo ideal para este aluno é {result}'
            }
    def get(self):
        return {
            "status": 'teste',
        }



if __name__ == "__main__":
  debug = True # com essa opção como True, ao salvar, o "site" recarrega automaticamente.
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=debug)

