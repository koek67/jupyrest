from jupyrest.model import BaseRdfModel
from jupyrest.nbschema import ModelCollection
from rdflib.graph import Graph
from rdflib.namespace import NamespaceManager
import io
import pydotplus
from IPython.display import display, Image
from rdflib.tools.rdf2dot import rdf2dot

def create_graph(*objs: BaseRdfModel):
    g = Graph()
    for obj in objs:
        for triple in obj.to_triples():
            g.add(triple) # type: ignore
    return g

def visualize(g: Graph):
    stream = io.StringIO()
    rdf2dot(g, stream, opts = {display})
    dg = pydotplus.graph_from_dot_data(stream.getvalue())
    png = dg.create_png() # type: ignore
    display(Image(png))