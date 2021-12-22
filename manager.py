from flask import Flask, json, send_file, request, make_response, jsonify

from Classes.Controller import Controller
from Classes.GraphGenerator import GraphGenerator
from Classes.Enricher import Enricher
from Classes.TDGenerator import TDGenerator
from Classes.FileTracker import FileTracker

app = Flask(__name__)

@app.route("/<id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manager(id):
    """
    Thing Manager Data Handler
    """
    controller = Controller(request, id)
    if request.method == 'GET':
        controller.get()
        return 'get'

    elif request.method == 'POST':
        graph_generator = GraphGenerator()
        # td_generator = TDGenerator()
        controller.post(graph_generator) # add td_generator
        return 'post'
    
    elif request.method == 'PUT':
        controller.put()
        return 'put'
    
    elif request.method == 'DELETE':
        controller.delete()
        return 'delete'

@app.route("/<id>", methods=['PUT'])
def manager_put(id):
    """
    Thing Manager Data Handler for PUT requests # Use type to know the serialization
    """
    controller = Controller(request, id)
    controller.put()
    return 'put'


    """ ProcessRDF Data (parametros : RDF, id, type) (PUT llama a este servicio)
    1. Almacenar el rdf en un named graph. Output: id del graph
    2. Consultar Thing Descriptions por si existe el identificador pasado como parametro dentro del dominio
    3. Extraer sujeto y tipo del id named graph... rdfs:label (modular como conjunto de queries)
    4. Llamar a ProcessTD
    """

    """ Process TD
    1. Por cada sujeto crear un TD --> 
        * ID fichero general (twin:platform:id_del_graph) --> si el id no es uuid
        * sujeto que nos permite acceder al fragmento del rdf
        * named_graph --> query de sparql (describe/construct)
    2. Si existe un TD con el id del fichero
        * Actualizar el TD con todos los sujetos del named graph y el named graph
        * Por cada TD del 5.1 actualizo con el endpoint del fichero
    3. Almacenar (Crear/Actualizar) los TDs en el TDD
    """

    """ Process Raw Data (POST llama a este servicio)
        1. Recibir el fichero, el id y el tipo
            1.1. Comprobar que el fichero no es rdf ni ninguna serialización de RDF
        2. Almacenar el fichero
        3. Llamar al generador de grafos
            3.1. Si es ifc --> UCL
            3.2. Si no --> Llamar a Helio (elegir el tipo de mappings)
        4. Crear TD con el ID del file y almacenarlo
        5. Llamar al ProcessRDF Data
    """


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