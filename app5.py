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



@app.route('/view/<table>', methods=["GET"])
def index(table):
    conn = get_db_conn()
    cursor = get_db_conn.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    entity = cursor.fetchall()
    conn.close()  # Certifique-se de fechar a conexão
    return jsonify(entity)
    
    
@app.route('/add/<table>', methods=["POST"])
def add(table):
    conn = get_db_conn()
    data = request.get_json()
    if table == "authors":
        cursor.execute('INSERT INTO authors (name, birthdate) VALUES (%s, %s)', 
                       (data['name'], data['birthdate']))
        conn.commit()
        conn.close()
        
    elif table == "categories":
        cursor = conn.cursor()
        cursor.execute('INSERT INTO categories (name) VALUES (%s)', (data['name'],))
        conn.commit()
        conn.close()
    
    elif table == "book":
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, published_date, author_id, category_id)
            VALUES (%s, %s, %s, %s)
        ''', (data['title'], data['published_date'], data['author_id'], data['category_id']))
        conn.commit()
        conn.close()
    
    else:
        if not data:
            return jsonify({'error': 'Não tem dados no request'}), 400

    cursor = get_db_conn.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    entity = cursor.fetchall()
    conn.close()
    return jsonify(entity)
    
#put das tabelas e individuos
@app.route('/put/<table>/<int:id_table>', methods=["PUT"])
def alterar_infos(table,id_table):
    conn = get_db_conn()
    cursor = conn.cursor()
    data = request.get_json()
    if table == "authors":
        cursor.execute(f'''
            UPDATE {table} 
            SET name = %s, birthdate = %s
            WHERE id = %s
        ''', (data['name'], data['birthdate'], id))
        conn.commit()
        conn.close()
        
    elif table == "categories":
        cursor.execute(f"""
            UPDATE {table} 
            SETSET name = %s
            WHERE {id_table} = %s
        """, (data['name'], id))
        conn.commit()
        conn.close()
        
    elif table == "books":
        pass
    



    
    


app.run(port=8000, host='localhost', debug=True)
