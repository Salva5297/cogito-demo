import requests
from SPARQLWrapper import SPARQLWrapper, JSON

class TDGenerator:

    def __init__(self, id):
        self.id = id
        self.tds = []
        self.sparql_query = None
        self.query_results = None
        self.td_directory_endpoint = "http://cogito-thing-manager_wothive_1:9000/api/things/{}".format(id)
        self.response = {
            "tds":[]
        }

    def generate_td(self):
        """
        Generate Thing Descriptions
        """
        td = {}
        self.tds.append(td)
        pass

    def retrieve_template(self):
        """
        Retrieve template to generate TDs
        """
        pass

    def query_triple_store(self):
        """
        Quuery triple store to retrieve elements to create TDs
        """
        sparql = SPARQLWrapper("http://virtuoso_db:8890/sparql")
        sparql.setQuery(self.sparql_query)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            self.query_results += result["s"]["value"]


    def store_TD(self):
        """
        Store TDs in Thing Directory
        """
        for td in self.tds:
            requests.put(self.td_directory_endpoint, json=td, headers={'Content-Type': 'application/td+json'}) # store TD in TD directory
            response_get_td = requests.get(self.td_directory_endpoint) # retrieve TD
            self.response["tds"].append(response_get_td.text) # add TD to response


        return self.response