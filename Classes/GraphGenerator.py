
import requests

class GraphGenerator:
    def __init__(self):
        self.graph = None # Generated graph
        self.graph_path = None
        self.ifc_url = 'https://kgg.openmetrics.eu/'
        self.url_upload_ifc = self.ifc_url + '/upload'
        self.url_download_ifc_graph = self.ifc_url + '/download'



    def generate_graph(self, file_type, file_name):

        if file_type == 'idf':
            self.graph = self.generate_idf_graph(file_name)
        
        else:
            # execute helio using jar and save the output in a file with same name as the file adding .ttl


            self.graph_path = file_name + ".ttl"
        pass

    def generate_idf_graph(self, file_name):
        """
        Generate graph using idf file
        """
        files = [
            ('file',(file_name+'.ifc',open(file_name, 'rb'),'application/octet-stream'))
        ]
        payload = {}
        s = requests.Session()
        s.get(self.ifc_url)

        headers_post = {
            'Cookie': 'JSESSIONID=' + s.cookies.get_dict()['JSESSIONID']
        }
        
        headers_get = {
            'Cookie': 'JSESSIONID=' + s.cookies.get_dict()['JSESSIONID']
        }

        response_post = requests.request("POST", self.url_upload_ifc, headers=headers_post, data=payload, files=files)
        response_get = requests.request("GET", self.url_download_ifc_graph, headers=headers_get, data=payload)

        return response_get.text  # GRAPH DB DOCKER?????