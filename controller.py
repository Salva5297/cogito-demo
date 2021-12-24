from flask import Flask, json, send_file, request, make_response, jsonify

from Classes.Services.Main_Service import Service
from Classes.Services.GraphGeneratorService import GraphGenerator
from Classes.Enricher import Enricher
from Classes.Services.TDService import TDService
from Classes.FileTracker import FileTracker

app = Flask(__name__)

@app.route("/<id>", methods=['GET'])
def controller_get(id):
    """
    Thing Manager Data Handler for GET requests
    """
    service = Service(request, id)
    service.get()
    return 'get'

@app.route("/<id>", methods=['POST'])
def controller_post(id):
    """
    Thing Manager Data Handler for POST requests
    """
    service = Service(request, id)
    service.post()
    return 'post'

@app.route("/<id>", methods=['PUT'])
def controller_put(id):
    """
    Thing Manager Data Handler for PUT requests # Use type to know the serialization
    """
    service = Service(request, id)
    service.put()
    return 'put'

@app.route("/<id>", methods=['DELETE'])
def controller_delete(id):
    """
    Thing Manager Data Handler for DELETE requests
    """
    return 'delete'


@app.route("/<subject>/data", methods=['POST']) # Probably it will not be necessary
def enrich_data(subject):
    return 'enrich_data: ' + subject
 

@app.route("/<subject>/meta", methods=['POST'])
def enrich_meta(subject):
    service = Service(request, id)
    enricher = Enricher(subject)
    service.post_enrichment(enricher)
    return 'enrich_meta: ' + subject


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)