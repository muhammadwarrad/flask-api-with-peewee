from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('states', user='postgres', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class States(BaseModel):
  name = CharField()
  capital = CharField()
  population = IntegerField()
  

db.connect()
db.drop_tables([States])
db.create_tables([States])

States(name='New Jersey',capital ='Trenton', population=90457).save()
States(name='Arizona ',capital ='Phoenix', population=1600000).save()
app = Flask(__name__)

@app.route('/States/', methods=['GET', 'POST'])
@app.route('/States/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(States.get(States.id == id)))
    else:
        States_list = []
        for States in States.select():
            States_list.append(model_to_dict(States))
        return jsonify(States_list)

  if request.method =='PUT':
    body = request.get_json()
    States.update(body).where(States.id == id).execute()
    return "States " + str(id) + " has been updated."

  if request.method == 'POST':
    new_States = dict_to_model(States, request.get_json())
    new_States.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    States.delete().where(States.id == id).execute()
    return "States " + str(id) + " deleted."

app.run(debug=True, port=9000)
