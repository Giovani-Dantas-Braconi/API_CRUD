from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'biblioteca'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/authors', methods=['GET', 'POST'])
def manage_authors():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM authors')
        authors = cursor.fetchall()
        connection.close()
        return jsonify(authors)
    
    elif request.method == 'POST':
        data = request.json
        cursor.execute('INSERT INTO authors (name, birthdate) VALUES (%s, %s)', 
                       (data['name'], data['birthdate']))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Author created'}), 201

@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        connection.close()
        return jsonify(categories)
    
    elif request.method == 'POST':
        data = request.json
        cursor.execute('INSERT INTO categories (name) VALUES (%s)', (data['name'],))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Category created'}), 201

@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT books.id, books.title, books.published_date, 
                   authors.name AS author_name, categories.name AS category_name
            FROM books
            JOIN authors ON books.author_id = authors.id
            JOIN categories ON books.category_id = categories.id
        ''')
        books = cursor.fetchall()
        connection.close()
        return jsonify(books)
    
    elif request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT INTO books (title, published_date, author_id, category_id)
            VALUES (%s, %s, %s, %s)
        ''', (data['title'], data['published_date'], data['author_id'], data['category_id']))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Book created'}), 201

@app.route('/authors/<int:id>', methods=['PUT', 'DELETE'])
def author_detail(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute('''
            UPDATE authors 
            SET name = %s, birthdate = %s
            WHERE id = %s
        ''', (data['name'], data['birthdate'], id))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Author updated'})
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM authors WHERE id = %s', (id,))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Author deleted'})

@app.route('/categories/<int:id>', methods=['PUT', 'DELETE'])
def category_detail(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute('''
            UPDATE categories 
            SET name = %s
            WHERE id = %s
        ''', (data['name'], id))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Category updated'})
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM categories WHERE id = %s', (id,))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Category deleted'})

@app.route('/books/<int:id>', methods=['PUT', 'DELETE'])
def book_detail(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute('''
            UPDATE books
            SET title = %s, published_date = %s, author_id = %s, category_id = %s
            WHERE id = %s
        ''', (data['title'], data['published_date'], data['author_id'], data['category_id'], id))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Book updated'})
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM books WHERE id = %s', (id,))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
