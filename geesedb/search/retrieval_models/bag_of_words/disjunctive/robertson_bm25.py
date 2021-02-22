from .disjunctive_retieval_model import DisjunctiveRetrievalModel


class RobertsonBM25(DisjunctiveRetrievalModel):
    def __init__(self, k1=0.9, b=0.4):
        DisjunctiveRetrievalModel.__init__(self)
        self.k1 = k1
        self.b = b

    def construct_query(self, topic):
        return DisjunctiveRetrievalModel.construct_query(self, topic) + \
               self.get_retrieval_model() + \
               DisjunctiveRetrievalModel.get_aggregator(self) + \
               DisjunctiveRetrievalModel.get_create_ranked_list(self)

    def get_retrieval_model(self):
        return ", subscores AS (" \
               "SELECT docs.collection_id, " \
               f"(LOG(((SELECT count(*) from docs)-df+0.5)/(df+0.5))*tf" \
               "/" \
               f"(tf+{self.k1}*(1-{self.b}+{self.b}*len/(SELECT AVG(len) from docs)))" \
               ") AS subscore " \
               "FROM qterms " \
               "JOIN condocs " \
               "ON qterms.doc_id = condocs.doc_id " \
               "JOIN docs " \
               "ON qterms.doc_id = docs.doc_id)"
