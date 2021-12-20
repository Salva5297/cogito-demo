import requests
from SPARQLWrapper import SPARQLWrapper, JSON

class TDGenerator:

    def __init__(self, id):
        self.id = id
        self.td = None
        self.sparql_query = None
        self.query_results = None
        self.td_directory_endpoint = "http://cogito-thing-manager_wothive_1:9000/api/things/{}".format(id)

    def generate_td(self):
        self.td = {}
        pass

    def retrieve_template(self):
        pass

    def query_triple_store(self):
        sparql = SPARQLWrapper("http://virtuoso_db:8890/sparql")
        sparql.setQuery(self.sparql_query)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            self.query_results += result["s"]["value"]


    def store_TD(self):
        response_put_td = requests.put(self.td_directory_endpoint, json=self.td, headers={'Content-Type': 'application/td+json'})
        response_get_td = requests.get(self.td_directory_endpoint)

        return response_get_td.text