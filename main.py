from flask import Flask, request, render_template, jsonify
import database

app = Flask(__name__)
database.init_db()

@app.route('/')
def index():
    leituras = database.listar_leituras(limite=10)
    return render_template('index.html', leituras=leituras)

@app.route('/leituras', methods=['GET', 'POST'])
def gerenciar_leituras():
    if request.method == 'POST':
        dados = request.get_json(silent=True)
        if not dados or 'temperatura' not in dados or 'umidade' not in dados:
            return jsonify({'erro': 'JSON inválido ou dados faltando'}), 400
        
        id_novo = database.inserir_leitura(
            dados['temperatura'],
            dados['umidade'],
            dados.get('pressao')
        )
        return jsonify({'id': id_novo, 'status': 'criado'}), 201
        
    elif request.method == 'GET':
        listar_todas = database.listar_leituras(limite=100)
        return render_template('historico.html', leituras=listar_todas)

@app.route('/leituras/<int:id_leitura>', methods=['GET'])
def detalhe_leitura(id_leitura):
    leitura = database.buscar_leitura(id_leitura)
    if not leitura:
        return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify(leitura)

@app.route('/leituras/<int:id_leitura>/atualizar', methods=['PUT', 'POST'])
def atualizar_leitura(id_leitura):
    if request.is_json:
        dados = request.get_json(silent=True)
    else:
        dados = request.form
        
    sucesso = database.atualizar_leitura(id_leitura, dados)
    if sucesso:
        return jsonify({'status': 'atualizado'})
    return jsonify({'erro': 'Falha ao atualizar'}), 400

@app.route('/leituras/<int:id_leitura>/deletar', methods=['DELETE', 'POST'])
def deletar_leitura(id_leitura):
    sucesso = database.deletar_leitura(id_leitura)
    if sucesso:
        return jsonify({'status': 'deletado'})
    return jsonify({'erro': 'Não encontrado'}), 404

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    stats = database.estatisticas_leituras()
    return jsonify(stats)

@app.route('/editar/<int:id_leitura>')
def pagina_editar(id_leitura):
    leitura = database.buscar_leitura(id_leitura)
    if not leitura:
        return "Leitura não encontrada", 404
    return render_template('editar.html', leitura=leitura)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

