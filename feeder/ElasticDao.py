from  elasticsearch import Elasticsearch

class ElasticDao:
    host="uninitialized"
    port="uninitialized"
    es="uninitialized "

    def __init__(self,host,port):
        self.host=host;
        self.port=port;
        self.es = Elasticsearch(self.host+":"+self.port)

    def put(self, index, doc_type, data):
        self.es.index(index,doc_type,data)


        
