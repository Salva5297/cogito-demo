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
        self.sparql_query = 'select distinct ?s where {[] a ?s} LIMIT 100' # Change to None if passed as parameter
        self.query_results = []
        self.template = None
        self.render_info = {}
        #self.search_template_path = 'templates/'
        self.template_name = 'td.template.txt'
        self.td_directory_endpoint = "http://cogito-thing-manager_wothive_1:9000/api/things/{}".format(id) # We can take the id from the subjects obtained by the query
        self.response = {"tds":[]}

    def generate_td(self):
        """
        Generate Thing Descriptions by rendering templates
        """
        template_rendered = self.template.render(self.render_info) # rendered in str format
        template_rendered = re.sub(r"[\n\t\s]*", "", template_rendered).replace(",}", "}").replace(",]", "]") # preprocess string before rendering to json format
        # print(template_rendered)
        td = json.dumps(json.loads(template_rendered), indent=4) # rendered in json format and inedented
        self.tds.append(td)

    def load_template(self, search_template_path):
        """
        Loads the template to create TDs
        """
        searchpath = [search_template_path] # search path
        engine = Engine(
            loader=FileLoader(searchpath),
            extensions=[CoreExtension()]
        ) # generate engine
        self.template = engine.get_template(self.template_name) # load template

    def query_triple_store(self):
        """
        Query triple store to retrieve elements to create TDs
        """
        sparql = SPARQLWrapper("http://localhost:8890/sparql") # change to virtuoso_db
        self.sparql_query.encode('utf-8')
        sparql.setQuery(self.sparql_query)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            self.query_results.append(result["s"]["value"])


    def info_to_render(self): # add subject as parameter
        """
        Retrieve info in a json format to render the template
        """
        self.render_info.update(
            {
                "prefixes": [
                    {"name":"beo", "url":"https://pi.pauwel.be/voc/buildingelement#"} # prefixes
                ],
                "id":self.id,
                "types": [
                    "bot:Building" # subject
                ],
                "description":"A building element.", # description about the subject
                "properties": [
                    {
                        "name": "IFC", # type of file
                        "uri": "https://example_uri.com/files/cogito1234.ifc", # uri of the file
                        "type": "application/ifc" # type_name of the file
                    },
                    {
                        "name": "KnowledgeGraph", # graph
                        "uri": "https://openmetrics.eu/openmetrics#Building_120", # uri of the graph
                        "type": "text/turtle" # type_name of the graph
                    }
                ]
            }
        )


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
            # Call info_to_render(s) to retrieve info in a json format to render the template
            # Call generate_td() to generate TDs
        # Call store_TD() to store TDs in Thing Directory
        pass