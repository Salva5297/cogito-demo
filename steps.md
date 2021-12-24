# ProcessRDF Data (parametros : RDF, id, type) (PUT llama a este servicio)  --> First
1. Almacenar el rdf en un named graph. Output: id del graph
2. Consultar Thing Descriptions por si existe el identificador pasado como parametro dentro del dominio
3. Extraer sujeto y tipo del id named graph... rdfs:label (modular como conjunto de queries)
4. Llamar a ProcessTD


# Process TD --> Second
1. Por cada sujeto crear un TD --> 
    * ID fichero general (twin:platform:id_del_graph) --> si el id no es uuid
    * sujeto que nos permite acceder al fragmento del rdf
    * named_graph --> query de sparql (describe/construct)
2. Si existe un TD con el id del fichero -->
    * Actualizar el TD con todos los sujetos del named graph y el named graph
    * Por cada TD del 5.1 actualizo con el endpoint del fichero
3. Almacenar (Crear/Actualizar) los TDs en el TDD


# Process Raw Data (POST llama a este servicio) --> Third
1. Recibir el fichero, el id y el tipo

    1.1. Comprobar que el fichero no es rdf ni ninguna serialización de RDF
2. Almacenar el fichero
3. Llamar al generador de grafos

    3.1. Si es ifc --> UCL

    3.2. Si no --> Llamar a Helio (elegir el tipo de mappings)
4. Crear TD con el ID del file y almacenarlo
5. Llamar al ProcessRDF Data
    