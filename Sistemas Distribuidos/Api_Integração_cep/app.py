from flask import Flask, jsonify, request
import requests
import re

app = Flask(__name__)

def validar_cep(cep):
    """Remove caracteres não numéricos e valida o CEP"""
    cep_limpo = re.sub(r'\D', '', cep)
    return cep_limpo if len(cep_limpo) == 8 else None

@app.route('/', methods=['GET'])
def index():
    """Rota principal com informações da API"""
    return jsonify({
        'mensagem': 'API de Integração ViaCEP',
        'endpoints': {
            'GET /cep/<cep>': 'Busca endereço por CEP',
            'GET /endereco/<uf>/<cidade>/<logradouro>': 'Busca CEP por endereço'
        }
    })

@app.route('/cep/<cep>', methods=['GET'])
def buscar_cep(cep):
    """Busca endereço por CEP"""
    try:
        cep_validado = validar_cep(cep)
        
        if not cep_validado:
            return jsonify({
                'erro': True,
                'mensagem': 'CEP inválido. Deve conter 8 dígitos.'
            }), 400
        
        response = requests.get(f'https://viacep.com.br/ws/{cep_validado}/json/')
        dados = response.json()
        
        if 'erro' in dados:
            return jsonify({
                'erro': True,
                'mensagem': 'CEP não encontrado.'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'dados': dados
        })
    
    except Exception as e:
        return jsonify({
            'erro': True,
            'mensagem': 'Erro ao buscar CEP',
            'detalhes': str(e)
        }), 500

@app.route('/endereco/<uf>/<cidade>/<logradouro>', methods=['GET'])
def buscar_endereco(uf, cidade, logradouro):
    """Busca CEP por endereço"""
    try:
        if len(uf) != 2:
            return jsonify({
                'erro': True,
                'mensagem': 'UF inválida. Deve ter 2 caracteres.'
            }), 400
        
        if len(logradouro) < 3:
            return jsonify({
                'erro': True,
                'mensagem': 'Logradouro deve ter pelo menos 3 caracteres.'
            }), 400
        
        url = f'https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/'
        response = requests.get(url)
        dados = response.json()
        
        if not dados or len(dados) == 0:
            return jsonify({
                'erro': True,
                'mensagem': 'Nenhum endereço encontrado.'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'quantidade': len(dados),
            'dados': dados
        })
    
    except Exception as e:
        return jsonify({
            'erro': True,
            'mensagem': 'Erro ao buscar endereço',
            'detalhes': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)