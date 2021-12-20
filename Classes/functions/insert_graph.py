import os
import subprocess

def insert_graph(fileName, id, triple_store_credentials):
    proc = subprocess.Popen(["curl",
                            "--digest",
                            "--verbose" ,
                            "--user",
                            "dba:mysecret",
                            "--url",
                            'http://virtuoso_db:8890/sparql-graph-crud-auth?graph-uri=http://virtuoso_db:8890/' + id,
                             "-T",
                             "RDF/"+ fileName.replace('/tmp/','') +".ttl"],
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    (out, err) = proc.communicate()
    lastCode = str(err).split('HTTP/1.1 ')[-1].split(" ")[0]
    
    if os.path.exists('RDF/'+ fileName.replace('/tmp/','') +'.ttl'):
        os.remove('RDF/'+ fileName.replace('/tmp/','') +".ttl")
    
    if lastCode == "200":
        return {'status': 'Success'}
    elif lastCode == "201":
        return {'status': 'Created'}
    elif lastCode == "401":
        return {'status': 'Error in authorization'}
    else:
        return {'status': 'Error'}