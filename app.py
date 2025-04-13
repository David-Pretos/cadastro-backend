from flask import Flask, render_template, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  # Adicionado para resolver erro de CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Inicializa o CORS na aplicação Flask

# Configuração do Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Configuração do banco de dados
DATABASE = 'users.db'

# Inicializa o banco de dados e cria a tabela 'users' caso ela não exista
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE
                        )''')

# Rota para obter a hora atual
@app.route('/time')
def get_time():
    now = datetime.now()
    return jsonify({
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second
    })

# Rota para cadastrar um novo usuário
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'Nome e email são obrigatórios'}), 400
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email já existe'}), 400

# Rota para buscar todos os usuários
@app.route('/buscar_usuario', methods=['GET'])
def buscar_usuario():
    with sqlite3.connect(DATABASE) as conn:
        users = conn.execute('SELECT id, name, email FROM users').fetchall()
    return jsonify([{'id': row[0], 'name': row[1], 'email': row[2]} for row in users])

# Rota para deletar um usuário pelo ID
@app.route('/deletar_usuario/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    with sqlite3.connect(DATABASE) as conn:
        result = conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        if result.rowcount == 0:
            return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify({'message': 'Usuário deletado com sucesso'})

# Ponto de entrada principal da aplicação
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
