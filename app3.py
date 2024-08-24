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

def listar_visu():
    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        
        query = 'SELECT * FROM authors'
        cursor.execute(query)
        authors = cursor.fetchall()
        
        return jsonify(authors)
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)})


#VIEW AUTORES
@app.route('/view/authors', methods=["GET"])
def listar_autores():
    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        
        query = 'SELECT * FROM authors'
        cursor.execute(query)
        authors = cursor.fetchall()

        cursor.close()
        conn.close()

        
        return jsonify({'authors': authors}), 200
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500
    

#INSPEÇÃO UNITÁRIO
@app.route('/specion/authors/<int:id>', methods=["GET"])
def inspecAuthor(id):
    conn = get_db_conn()
    cursor = conn.cursor()
    query = 'SELECT * FROM authors WHERE id = %s'
    cursor.execute(query, (id,))
    results = cursor.fetchone()
    
    if results:
            return jsonify(results), 201
    else:
            return jsonify({'message': 'Author not found'}), 404
    


#POST
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

        
        listar_autors = listar_visu()

        cursor.close()
        conn.close()

        
        return jsonify({'message': 'Author criado', 'authors': listar_autors}), 201
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500




#DELETA AUTOR
@app.route('/del/authors/<int:id>', methods=["DEL"])
def delete_auth(id):
    conn = get_db_conn()
    cursor = conn.cursor()
    data = request.json

    if 'name' not in data or 'birthdate' not in data:
        return jsonify({'error': 'Dados insuficientes'}), 400
    
    try:
        cursor.execute('DELETE FROM authors WHERE id = %s', (id,))
        conn.commit()
        
        listar_autors = listar_visu()

        cursor.close()
        conn.close()

        
        return jsonify({'message': 'Author deletado', 'authors': listar_autors}), 201
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/view/')
def passsddd():
     pass
    






app.run(port=8000, host='localhost', debug=True)

