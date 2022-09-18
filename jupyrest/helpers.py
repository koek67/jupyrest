from jupyrest.model import BaseRdfModel
from jupyrest.graph import create_graph, visualize
from rdflib import Namespace, Graph
from typing import Set, Optional
from datetime import datetime
from pathlib import Path
import pickle


class Node(BaseRdfModel):
    node_id: str
    
    def uid(self):
        return self.node_id
    
    class Config:
        ns = Namespace("nodes/")
        
class Replica(BaseRdfModel):
    replica_id: str
    node: Optional[Node] = None
    
    def uid(self):
        return self.replica_id
    
    class Config:
        ns = Namespace("replicas/")

class Service(BaseRdfModel):
    service_name: str
    replicas: Set[Replica] = set()
    
    def uid(self):
        return self.service_name
    
    class Config:
        ns = Namespace("services/")

class Customer(BaseRdfModel):
    customer_id: str
    services: Set["Service"] = set()

    def uid(self):
        return self.customer_id

    class Config:
        ns = Namespace("customers/")
        
class Incident(BaseRdfModel):
    incident_id: str
    incident_time: datetime

    def uid(self):
        return self.incident_id

    class Config:
        ns = Namespace("incidents/")
    
class ReplicaResends(Incident):
    src_replica: Replica
    dest_replica: Replica
    
class SlowDisk(Incident):
    node: Node
    
class SLADip(Incident):
    customer: Customer

def get_customer(customer_id: str):
    services = set([
        Service(service_name="a349f9", replicas=set([
            Replica(replica_id="706cd", node=Node(node_id="212")), #r1 n1
            Replica(replica_id="6e795", node=Node(node_id="601")), #r2 n2
            Replica(replica_id="3c06c", node=Node(node_id="803")), #r3 n3
            Replica(replica_id="9f58f", node=Node(node_id="498")), #r4 n4
        ])),
        Service(service_name="b59d2", replicas=set([
            Replica(replica_id="1e55e", node=Node(node_id="212")), #r5 n1
            Replica(replica_id="c385f", node=Node(node_id="601")), #r6 n2
            Replica(replica_id="8b3f9", node=Node(node_id="803")), #r7 n3
            Replica(replica_id="f976f", node=Node(node_id="900")), #r8 n5
        ])),
    ])
    return Customer(customer_id="Paddys_Pub", services=services)

graphs_dir = Path.home() / ".jupyrest_graphs"
graphs_dir.mkdir(exist_ok=True)

def save_graph(incident: Incident, graph: Graph):
    destination = graphs_dir / f"{incident.incident_id}.ttl"
    data = graph.serialize(format="turtle")
    destination.write_text(data)
    # destination.write_bytes(pickle.dumps(graph))
    print(f"Saved graph at {destination}")

def get_graph(*incident_ids):
    g = Graph()
    for incident_id in incident_ids:
        data = (graphs_dir / f"{incident_id}.ttl").read_text()
        g.parse(format="turtle", data=data, location=None)
    return g

def get_past_incident_ids():
    """
    Incident ids:
        - 001
        - 002
        - 003
        - 004
    """
    return ["001", "002", "003", "004"]