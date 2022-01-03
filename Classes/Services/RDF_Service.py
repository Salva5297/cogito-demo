

class RDF_Service:

    def __init__(self):
        pass


    def generate_graph(self, file_type, file_name):
        """
        Generate graph from a specific file uploaded
        """
        if file_type == 'ifc':
            self.graph = self.generate_ifc_graph(file_name)
        else:
            # execute helio using jar and save the output in a file with same name as the file adding .ttl
            self.graph_path = file_name + ".ttl"
        pass


