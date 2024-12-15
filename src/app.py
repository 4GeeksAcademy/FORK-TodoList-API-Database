"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# AHORA MEDIANTE LOS ENDPOINTS VAMOS A AGREGAR EL USUARIO A LA BASE DE DATOS REAL     


# Endpoint - Crear Usuario en la base de datos
@app.route('/users/<string:username>', methods=['POST'])
def add_new_user(username=None):
    user = User()
    # Filtrando si el name la clase User == a username...

    # Forma - 1 
    user_true = user.query.filter_by(name=username).first()
    
    # Si user_true es real ( name si es == username) 
    if user_true is not None:

        return jsonify({
            "rejected" : "user already exists" 
        }), 400
        
    # Es decir en cualquier otro caso (Si no es igual, pues crea otro usuario..)
    else:
        # Estos 2 codigos para agregar el username al la database
        user.name = username
        user.gender = 'MALE'
        db.session.add(user)

        try:
            db.session.commit()
            return jsonify({
                "id" : user.id,
                "name" : user.name
            })
        except Exception as error:
            return jsonify(error), 500
            
            
            

# Endpoint - Borrar Usuario en la base de datos
@app.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username=None):
    # Forma - 2 
    user = User.query.filter_by(name=username).first()

    if user is None:
        return jsonify({
            "detail" : f"User {username} doesn't exists"
        })

    else:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify ([], 204)
        except Exception as error:
            return jsonify(error), 500
    
                         
                         
# Endpoint - Consultar Usuario en la base de datos
@app.route('/users/<string:username>', methods=['GET'])
def consultar_user(username=None):
    user = User.query.filter_by(name=username).one_or_none() #Similar al first() (Pero devuelve solo uno o None)

    if user is None:
        return jsonify({
            "detail" : f"user {username} doesn't exists"
        })

    return jsonify(user.serializable()), 200


# Endpoint consultar Todos los Usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User()
    # Query.all devuelve todo el contenido de una tabla
    users = users.query.all()
    return jsonify({
        "users" : list(map(lambda unit : unit.serializable_users() , users))
    })


# Endpoint Agregar una tarea to-do 
@app.route('/todos/<string:username>', methods=['POST'])
def agregar_todo(username=None):
    # Recuerda que esto es el objeto que recibo por parte del usuario al hacer POST
    body = request.json
 
    user = User.query.filter_by(name=username).one_or_none()
    
    todos = Todos()

    if body.get("label") is None:
        return jsonify("Tu body debe conteneder un label"), 400
    
    if body.get("is_done") is None:
        return jsonify("Tu body debe conteneder un is_done"), 400
 
    todos.label = body['label'] 
    todos.is_done = body.get('is_done')
    todos.user_id = user.id
    db.session.add(todos)

    try:
        db.session.commit()
        return jsonify('Tarea guardada exitosamente'), 201
    except Exception as error:
        # En caso se guarde muchas tareas pero entre muchas  uno falla, se borra todo y no se guarda nada
        db.session.rollback()
        return jsonify(error.args), 500


# Endpoint Modificar una tarea
@app.route('/todos/<int:theid>', methods=['PUT'])
def modificar_tarea(theid):
    body = request.json
     # Opcion 1  
    # todo_edit = Todos.query.filter_by(id=theid).first() 
    # Opcion 2
    todo_edit = Todos.query.get(theid)

    if body.get("label") is None:
        return jsonify("Tu body debe conteneder un label"), 400
    
    if body.get("is_done") is None:
        return jsonify("Tu body debe conteneder un is_done"), 400

    if todo_edit is None:
        return jsonify({
            "message" : f"No existe una tarea con el id {theid}"
        }), 404
    else:
        try:
            todo_edit.label = body["label"]
            todo_edit.is_done = body["is_done"]

            db.session.commit()
            return jsonify(todo_edit.serializable()), 201 

        except Exception as error:
            return jsonify(error.args), 500 


# Endpoint Eliminar una Tarea
@app.route('/todos/<int:theid>', methods=['DELETE'])
def borrar_tarea(theid):
    todo = Todos.query.get(theid)

    if todo is None: 
        return jsonify({"message" : f"{theid} doesn't exists"}), 404
    else:
        try:
            db.session.delete(todo)
            db.session.commit()
            return jsonify([]), 204
        except Exception as error:
            return jsonify("Error, intentelo mas tarde")


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
