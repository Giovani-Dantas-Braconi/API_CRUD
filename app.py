from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
    {
        "id" : 1,
        "titulo" : "O tigre triste",
        "autor" : "Eu mesmo" 
    },

    {
        "id" : 2,
        "titulo" : "a garrafa vazia",
        "autor" : "minha home"

    },

    {
        "id" : 3,
        "titulo" : "o remédio esquecido",
        "autor" : "meu pai"
    }
]

#select
@app.route('/view_livros', methods=["GET"])
def obterlivros():
    return jsonify(livros)


#visualização especifica atráves do id 
@app.route('/info_livro/<int:id>', methods=["GET"])
def infoslivro(id):
    for livro_instance in livros:
        if livro_instance.get('id') == id:
            return jsonify(livro_instance) 


#editar o livro atraves do id 
@app.route('/editar_livro/<int:id>', methods=['PUT'])
def editar_livro(id):
    livro_alterado = request.get_json()
    for i, instancia in enumerate(livros):
        if instancia.get('id') == id:
            livros[i].update(livro_alterado)
            return jsonify(livros[i])
        

@app.route('/add_novo', methods=["POST"])
def add_livro():
    novo_livro = request.get_json()
    livros.append(novo_livro)
    return jsonify(livros)



@app.route('/excluir_livro/<int:id>', methods=["DELETE"])
def excluir_livro(id):
    for i, livro in enumerate(livros):
        if livro.get('id') == id:
            del livros[i]
        
    return jsonify(livros)



app.run(port=8000, host='localhost', debug=True)



#  Criação da API Flask
# Crie um aplicativo Flask com os seguintes endpoints:

# Autores

# GET /authors: Lista todos os autores.
# POST /authors: Cria um novo autor.
# PUT /authors/<id>: Atualiza informações de um autor existente.
# DELETE /authors/<id>: Remove um autor.

# Categorias
# GET /categories: Lista todas as categorias.
# POST /categories: Cria uma nova categoria.
# PUT /categories/<id>: Atualiza informações de uma categoria existente.
# DELETE /categories/<id>: Remove uma categoria.

# Livros
# GET /books: Lista todos os livros, incluindo detalhes do autor e da categoria.
# POST /books: Cria um novo livro.
# PUT /books/<id>: Atualiza informações de um livro existente.
# DELETE /books/<id>: Remove um livro.