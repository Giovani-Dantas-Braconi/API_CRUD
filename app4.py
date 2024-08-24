from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

DB = "projeto_facul"



db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': '',  
    'database': f'{DB}'  
}


def get_db_conn():
    conn = mysql.connector.connect(**db_config)
    return conn



@app.route('/post/authors', methods=["POST"])
def adicionar_novo():
    conn = get_db_conn()
    cursor = conn.cursor()
    data = request.json

    if 'name' not in data or 'birthdate' not in data:
        return jsonify({'error': 'Dados insuficientes'}), 400
    
    try:
        
        query = 'INSERT INTO authors (name, birthdate) VALUES (%s, %s)'
        cursor.execute(query, (data['name'], data['birthdate']))
        conn.commit()
        
        cursor.close()
        conn.close()

        
        return jsonify({'message': 'Author criado'}), 201
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500





app.run(port=8000, host='localhost', debug=True)
