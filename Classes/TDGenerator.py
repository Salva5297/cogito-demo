import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import time
import json
import re
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

class TDGenerator:

    def __init__(self, id):
        self.id = id
        self.tds = []
        self.sparql_query = None
        self.query_results = None
        self.template = None
        self.render_info = None
        self.search_template_path = 'templates/'
        self.template_name = 'td.template.txt'
        self.td_directory_endpoint = "http://cogito-thing-manager_wothive_1:9000/api/things/{}".format(id) # We can take the id from the subjects obtained by the query
        self.response = {"tds":[]}

    def generate_td(self, rendering_info):
        """
        Generate Thing Descriptions by rendering templates
        """
        template_rendered = self.template.render(rendering_info) # rendered in str format
        template_rendered = re.sub(r"[\n\t\s]*", "", template_rendered).replace(",}", "}").replace(",]", "]") # preprocess string before rendering to json format
        # print(template_rendered)
        td = json.dumps(json.loads(template_rendered), indent=4) # rendered in json format and inedented
        self.tds.append(td)

    def load_template(self):
        """
        Loads the template to create TDs
        """
        searchpath = [self.search_template_path] # search path
        engine = Engine(
            loader=FileLoader(searchpath),
            extensions=[CoreExtension()]
        ) # generate engine
        self.template = engine.get_template(self.template_name) # load template

    def query_triple_store(self):
        """
        Query triple store to retrieve elements to create TDs
        """
        sparql = SPARQLWrapper("http://virtuoso_db:8890/sparql")
        sparql.setQuery(self.sparql_query)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            self.query_results += result["s"]["value"]


    def info_to_render(self):
        """
        Retrieve info in a json format to render the template
        """
        pass


    def store_TD(self):
        """
        Store TDs in Thing Directory
        """
        for td in self.tds:
            requests.put(self.td_directory_endpoint, json=td, headers={'Content-Type': 'application/td+json'}) # store TD in TD directory
            response_get_td = requests.get(self.td_directory_endpoint) # retrieve TD
            self.response["tds"].append(response_get_td.text) # add TD to response
        return self.response

    def main(self):
        """
        Main function
        """
        # Call self.query_triple_store() to query triple store
        # Call self.template_to_render() to load the template
        # Inside for loop
            # Call info_to_render() to retrieve info in a json format to render the template
            # Call generate_td() to generate TDs
        # Call store_TD() to store TDs in Thing Directory
        pass