import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate

from model import Bank, db

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost/{os.getenv("DB_NAME")}'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/banks', methods=['POST', 'GET'])
@cross_origin()
def handle_banks():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            new_bank = Bank(title=data['title'], count_of_clients=data['count_of_clients'],
                            description=data['description'],
                            image=data['image'])
            db.session.add(new_bank)
            db.session.commit()
            return {"message": f"your amazing {new_bank.title} successfully added"}
        else:
            return {"error": "pls use json format"}
    elif request.method == "GET":
        banks = Bank.query.all()
        results = [
            {
                "id": bank.id,
                "title": bank.title,
                "count_of_clients": bank.count_of_clients,
                "description": bank.description,
                "image": bank.image
            } for bank in banks
        ]
        return jsonify(results)


@app.route('/banks/<int:id>', methods=['PUT', 'DELETE'])
@cross_origin()
def handle_bank(id):
    if request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            new_bank = Bank(title=data['title'], count_of_clients=data['count_of_clients'],
                            description=data['description'],
                            image=data['image'])
            Bank.query.filter_by(id=id).update(
                {"title": new_bank.title, "count_of_clients": new_bank.count_of_clients,
                 "description": new_bank.description,
                 "image": new_bank.image})
            db.session.commit()
            return {"message": "Bank successfully updated"}
        return {"message": "incorrect input data"}
    elif request.method == 'DELETE':
        bank_to_delete = Bank.query.get(id)
        if bank_to_delete:
            db.session.delete(bank_to_delete)
            db.session.commit()
            return {"message": f"{bank_to_delete.title} deleted :("}
        else:
            return {"message": "Bank not found"}


if __name__ == '__main__':
    app.run(debug=True)
