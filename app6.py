from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

DB = "projeto_facul"

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': DB
}

def get_db_conn():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None


#visualizar as tabelas, falta inspec
@app.route('/view/<table>', methods=["GET"])
def index(table):
    conn = get_db_conn()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM {table}')
        entity = cursor.fetchall()
        return jsonify(entity)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


#adicionar
@app.route('/add/<table>', methods=["POST"])
def add(table):
    conn = get_db_conn()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500

    data = request.get_json()
    try:
        cursor = conn.cursor()
        if table == "authors":
            cursor.execute('INSERT INTO authors (name, birthdate) VALUES (%s, %s)', 
                           (data['name'], data['birthdate']))
        
        elif table == "categories":
            cursor.execute('INSERT INTO categories (name) VALUES (%s)', (data['name'],))
        
        elif table == "books":
            cursor.execute('''
                INSERT INTO books (title, published_date, author_id, category_id)
                VALUES (%s, %s, %s, %s)
            ''', (data['title'], data['published_date'], data['author_id'], data['category_id']))
        
        else:
            return jsonify({'error': 'Table not supported'}), 400

        conn.commit()

        cursor.execute(f'SELECT * FROM {table}')
        entity = cursor.fetchall()
        return jsonify(entity)

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

#atualizar as infos
@app.route('/put/<table>/<int:id_table>', methods=["PUT"])
def alterar_infos(table, id_table):
    conn = get_db_conn()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500

    data = request.get_json()
    try:
        cursor = conn.cursor()
        if table == "authors":
            cursor.execute(f'''
                UPDATE {table} 
                SET name = %s, birthdate = %s
                WHERE id = %s
            ''', (data['name'], data['birthdate'], id_table))
        
        elif table == "categories":
            cursor.execute(f'''
                UPDATE {table} 
                SET name = %s
                WHERE id = %s
            ''', (data['name'], id_table))
        
        elif table == "books":
            cursor.execute(f'''
                UPDATE {table} 
                SET title = %s, published_date = %s, author_id = %s, category_id = %s
                WHERE id = %s
            ''', (data['title'], data['published_date'], data['author_id'], data['category_id'], id_table))

        else:
            return jsonify({'error': 'Table not supported'}), 400

        conn.commit()
        cursor.execute(f'SELECT * FROM {table}')
        entity = cursor.fetchall()
        return jsonify(entity)

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/del/<table>/<int:id_table>', methods=["DELETE"])
def del_entity(table,id_table):
    conn = get_db_conn()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500

    try:
        cursor = conn.cursor()
        if table == "authors":
            cursor.execute(f'''
                DELETE FROM {table} WHERE id = %s
        ''', (id_table,))
            conn.commit()

        elif table == "books":
            cursor.execute(f'''
                DELETE FROM {table} WHERE id = %s
        ''', (id_table,))
            conn.commit()
        
        elif table == "categories":
            cursor.execute(f'''
                DELETE FROM {table} WHERE id = %s
        ''', (id_table,))
            conn.commit()


        else:
            return jsonify({'error': 'Table not supported'}), 400


    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/inspec/<table>/<int:id_table>', methods=["GET"])
def inspec_item(table, id_table):
    conn = get_db_conn()
    if conn is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = conn.cursor()
        if table == "authors":
            cursor.execute(f'''
                SELECT * FROM {table} WHERE id = %s
            ''', (id_table,))
            
        elif table == "books":
            cursor.execute(f'''
                SELECT FROM {table} WHERE id = %s
            ''', (id_table,))
            
        elif table == "categories":
            cursor.execute(f'''
                SELECT FROM {table} WHERE id = %s
            ''', (id_table,))
              
    
    

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        visu = cursor.fetchone()
        conn.close()
        return jsonify(visu)


if __name__ == "__main__":
    app.run(port=8000, host='localhost', debug=True)
