from flask import Flask, json, send_file, request, make_response, jsonify

from Classes.Controller import Controller
from Classes.GraphGenerator import GraphGenerator
from Classes.Enricher import Enricher

app = Flask(__name__)



@app.route("/<id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manager(id):
    if request.method == 'GET':
        controller = Controller(request, id)
        controller.get()
        return 'get'

    elif request.method == 'POST':
        controller = Controller(request, id)
        graph_generator = GraphGenerator()
        controller.post(graph_generator)
        return 'post'
    
    elif request.method == 'PUT':
        controller = Controller(request, id)
        controller.put()
        return 'put'
    
    elif request.method == 'DELETE':
        controller = Controller(request, id)
        controller.delete()
        return 'delete'

@app.route("/<subject>/data", methods=['POST']) # Probably it will not be necessary
def enrich_data(subject):
    return 'enrich_data: ' + subject

@app.route("/<subject>/meta", methods=['POST'])
def enrich_meta(subject):
    controller = Controller(request, id)
    enricher = Enricher(subject)
    controller.post_enrichment(enricher)
    return 'enrich_meta: ' + subject


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)