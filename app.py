from flask import Flask, render_template, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint 
import sqlite3
from datetime import datetime

app = Flask(__name__)

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
    # Retorna a hora, minuto e segundo atuais
    now = datetime.now()
    return {
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second
    }

# Rota para cadastrar um novo usuário
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    # Extrai os dados do usuário da requisição
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        # Retorna um erro se o nome ou email estiverem ausentes
        return jsonify({'error': 'Nome e email são obrigatórios'}), 400
    try:
        # Insere o novo usuário no banco de dados
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    except sqlite3.IntegrityError:
        # Trata o erro de email duplicado
        return jsonify({'error': 'Email já existe'}), 400

# Rota para buscar todos os usuários
@app.route('/buscar_usuario', methods=['GET'])
def buscar_usuario():
    # Recupera todos os usuários do banco de dados
    with sqlite3.connect(DATABASE) as conn:
        users = conn.execute('SELECT id, name, email FROM users').fetchall()
    # Retorna a lista de usuários em formato JSON
    return jsonify([{'id': row[0], 'name': row[1], 'email': row[2]} for row in users])

# Rota para deletar um usuário pelo ID
@app.route('/deletar_usuario/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    # Deleta o usuário com o ID especificado no banco de dados
    with sqlite3.connect(DATABASE) as conn:
        result = conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        if result.rowcount == 0:
            # Retorna um erro se o usuário não for encontrado
            return jsonify({'error': 'Usuário não encontrado'}), 404
    # Retorna uma mensagem de sucesso
    return jsonify({'message': 'Usuário deletado com sucesso'})

# Ponto de entrada principal da aplicação
if __name__ == '__main__':
    # Inicializa o banco de dados e executa o aplicativo Flask
    init_db()
    app.run(debug=True)