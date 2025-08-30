# Auto generated from kg.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-08-30T18:46:55
# Schema: KG
#
# id: https://purl.humanatlas.io/vocab/kg
# description: Simple Knowledge Graph representation
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Float, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Namespaces
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
KG = CurieNamespace('kg', 'https://purl.humanatlas.io/vocab/kg#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = KG


# Types
class Uri(Uriorcurie):
    """ Use this only in the `range` field of a slot to make a URI point at a node in an RDF graph. """
    type_class_uri = RDFS["Resource"]
    type_class_curie = "rdfs:Resource"
    type_name = "Uri"
    type_model_uri = KG.Uri


# Class references
class NodeIri(Uri):
    pass


@dataclass(repr=False)
class Node(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL["Class"]
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Node"
    class_model_uri: ClassVar[URIRef] = KG.Node

    iri: Union[str, NodeIri] = None
    label: str = None
    type: Union[str, Uri] = None
    source: Union[str, Uri] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.iri):
            self.MissingRequiredField("iri")
        if not isinstance(self.iri, NodeIri):
            self.iri = NodeIri(self.iri)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, Uri):
            self.type = Uri(self.type)

        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, Uri):
            self.source = Uri(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Edge(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF["Statement"]
    class_class_curie: ClassVar[str] = "rdf:Statement"
    class_name: ClassVar[str] = "Edge"
    class_model_uri: ClassVar[URIRef] = KG.Edge

    subject: Union[str, NodeIri] = None
    predicate: Union[str, Uri] = None
    object: Union[str, NodeIri] = None
    source: Union[str, Uri] = None
    gene_expr: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NodeIri):
            self.subject = NodeIri(self.subject)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, Uri):
            self.predicate = Uri(self.predicate)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, NodeIri):
            self.object = NodeIri(self.object)

        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, Uri):
            self.source = Uri(self.source)

        if self.gene_expr is not None and not isinstance(self.gene_expr, float):
            self.gene_expr = float(self.gene_expr)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Graph(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KG["Graph"]
    class_class_curie: ClassVar[str] = "kg:Graph"
    class_name: ClassVar[str] = "Graph"
    class_model_uri: ClassVar[URIRef] = KG.Graph

    nodes: Optional[Union[dict[Union[str, NodeIri], Union[dict, Node]], list[Union[dict, Node]]]] = empty_dict()
    edges: Optional[Union[Union[dict, Edge], list[Union[dict, Edge]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="nodes", slot_type=Node, key_name="iri", keyed=True)

        if not isinstance(self.edges, list):
            self.edges = [self.edges] if self.edges is not None else []
        self.edges = [v if isinstance(v, Edge) else Edge(**as_dict(v)) for v in self.edges]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.iri = Slot(uri=KG.iri, name="iri", curie=KG.curie('iri'),
                   model_uri=KG.iri, domain=None, range=URIRef)

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=KG.label, domain=None, range=str)

slots.type = Slot(uri=RDF.type, name="type", curie=RDF.curie('type'),
                   model_uri=KG.type, domain=None, range=Union[str, Uri])

slots.source = Slot(uri=RDFS.isDefinedBy, name="source", curie=RDFS.curie('isDefinedBy'),
                   model_uri=KG.source, domain=None, range=Union[str, Uri])

slots.subject = Slot(uri=RDF.subject, name="subject", curie=RDF.curie('subject'),
                   model_uri=KG.subject, domain=None, range=Union[str, NodeIri])

slots.predicate = Slot(uri=RDF.predicate, name="predicate", curie=RDF.curie('predicate'),
                   model_uri=KG.predicate, domain=None, range=Union[str, Uri])

slots.object = Slot(uri=RDF.object, name="object", curie=RDF.curie('object'),
                   model_uri=KG.object, domain=None, range=Union[str, NodeIri])

slots.gene_expr = Slot(uri=OBI['0001938'], name="gene_expr", curie=OBI.curie('0001938'),
                   model_uri=KG.gene_expr, domain=None, range=Optional[float])

slots.graph__nodes = Slot(uri=KG.nodes, name="graph__nodes", curie=KG.curie('nodes'),
                   model_uri=KG.graph__nodes, domain=None, range=Optional[Union[dict[Union[str, NodeIri], Union[dict, Node]], list[Union[dict, Node]]]])

slots.graph__edges = Slot(uri=KG.edges, name="graph__edges", curie=KG.curie('edges'),
                   model_uri=KG.graph__edges, domain=None, range=Optional[Union[Union[dict, Edge], list[Union[dict, Edge]]]])
