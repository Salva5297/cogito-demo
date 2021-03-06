import tempfile
import os
import subprocess
from flask import request, make_response, jsonify

from Classes.Services.RDF_Service import TripleStore_Service


class Service:
    def __init__(self, request_data, id):
        self.request = request_data # request sent to the api
        self.id = id # id of TD and graph
        self.uploaded_file = None # uploaded file
        self.file_type = None # type of the file
        self.type_name = None # type/name
        self.graph = None # rdf graph generated from file provided or rdf file provided by the request
        self.triple_store_credentials = {'username': 'dba', 'password': 'mysecret'} # credentials for triple store
        self.graph_generator = None # graph generator
        self.response = {} # response sent to the client
        self.sparql_query = None # sparql query for get statement


    def get(self):
        """
        Get statement
        """
        self.request.get_data()
        self.response = {'status': 'success'} # TODO: create get method

    def post(self, graph_generator):
        """
        Post file, generate graph and TDs and store them inside their respectives databases
        """
        if "file" not in request.files:
            return make_response(jsonify({"response": "No file part"}))
        self.file_type = self.request.args.get('file_type','') # retrieve file type
        self.uploaded_file = self.request.files['file'].read() # retrieve uploaded file
        self.graph_generator = graph_generator # execute graph generator class and generate graph
        self.generate_graph = True # change generate_graph to True because in this step we need to generate the graph
        self.temporal_file_generation_process() # generate graph and store it in triple store
        # generate TDs using sparql query retrieving all elements of the graph
        return self.response
        
    def post_enrichment(self, enricher):
        """
        Enrich TDs with images or extra files
        """
        # call enricher class
        pass


    def put(self):
        """
        Insert graph given as argument in body of the request in triple store and generate TDs
        """
        if "rdf" not in request.files:
            return make_response(jsonify({"response": "No rdf file part"})) # Change to array with serialization that we need ttl, n3 and xml -> if not provide error
        self.uploaded_file = self.request.files['rdf'].read()
        self.generate_graph = False
        triple_store_service = TripleStore_Service()
        triple_store_service.store_rdf(self.uploaded_file, self.id)
        
        query = ""
        triple_store_service.query_graph(query)
        #self.response = self.insert_graph(temp.name, self.id, self.triple_store_credentials)
        #self.temporal_file_generation_process()
        # Query SPARQL -> Triple Store
        # Generate TDs
        return self.response

    def delete(self):
        """
        Delete statement
        """
        self.response = {'status': 'success'} # TODO: create delete method



    def insert_graph(self,file_name):
        """
        Insert graph in triple store
        """
        proc = subprocess.Popen(["curl",
                                "--digest",
                                "--verbose" ,
                                "--user",
                                self.triple_store_credentials['username'] + ":" + self.triple_store_credentials['password'],
                                "--url",
                                'http://virtuoso_db:8890/sparql-graph-crud-auth?graph-uri=http://virtuoso_db:8890/' + self.id,
                                "-T",
                                file_name +".ttl"],
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        ## https://stackoverflow.com/questions/50376348/http-request-authentication-for-sparql-insert-in-virtuoso-endpoint

        if os.path.exists(file_name +'.ttl'):
            os.remove(file_name +".ttl")
            

    def temporal_file_generation_process(self):
        """
        Create temporal file, generate graph and store it in triple store
        """
        temp = tempfile.NamedTemporaryFile()
        try:
            temp.write(self.uploaded_file)
            temp.seek(0)
            self.graph_generator.generate_graph(self.file_type, temp.name) # remove after graph file path to not make trash files
            self.response = self.insert_graph(self.graph_generator.graph_path, self.id, self.triple_store_credentials)
        finally:
            temp.close()