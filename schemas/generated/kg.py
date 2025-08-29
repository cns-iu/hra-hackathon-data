# Auto generated from kg.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-08-28T14:46:49
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

from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Namespaces
KG = CurieNamespace('kg', 'https://purl.humanatlas.io/vocab/kg/')
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
    label: Optional[str] = None
    type: Optional[Union[str, Uri]] = None
    source: Optional[Union[str, Uri]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.iri):
            self.MissingRequiredField("iri")
        if not isinstance(self.iri, NodeIri):
            self.iri = NodeIri(self.iri)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.type is not None and not isinstance(self.type, Uri):
            self.type = Uri(self.type)

        if self.source is not None and not isinstance(self.source, Uri):
            self.source = Uri(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Edge(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF["Statement"]
    class_class_curie: ClassVar[str] = "rdf:Statement"
    class_name: ClassVar[str] = "Edge"
    class_model_uri: ClassVar[URIRef] = KG.Edge

    subject: Optional[Union[str, NodeIri]] = None
    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, NodeIri]] = None
    source: Optional[Union[str, Uri]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.subject is not None and not isinstance(self.subject, NodeIri):
            self.subject = NodeIri(self.subject)

        self.predicate = str(self.class_class_curie)

        if self.object is not None and not isinstance(self.object, NodeIri):
            self.object = NodeIri(self.object)

        if self.source is not None and not isinstance(self.source, Uri):
            self.source = Uri(self.source)

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
                   model_uri=KG.label, domain=None, range=Optional[str])

slots.type = Slot(uri=RDF.type, name="type", curie=RDF.curie('type'),
                   model_uri=KG.type, domain=None, range=Optional[Union[str, Uri]])

slots.source = Slot(uri=RDFS.isDefinedBy, name="source", curie=RDFS.curie('isDefinedBy'),
                   model_uri=KG.source, domain=None, range=Optional[Union[str, Uri]])

slots.subject = Slot(uri=RDF.subject, name="subject", curie=RDF.curie('subject'),
                   model_uri=KG.subject, domain=None, range=Optional[Union[str, NodeIri]])

slots.predicate = Slot(uri=RDF.predicate, name="predicate", curie=RDF.curie('predicate'),
                   model_uri=KG.predicate, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.object = Slot(uri=RDF.object, name="object", curie=RDF.curie('object'),
                   model_uri=KG.object, domain=None, range=Optional[Union[str, NodeIri]])

slots.graph__nodes = Slot(uri=KG.nodes, name="graph__nodes", curie=KG.curie('nodes'),
                   model_uri=KG.graph__nodes, domain=None, range=Optional[Union[dict[Union[str, NodeIri], Union[dict, Node]], list[Union[dict, Node]]]])

slots.graph__edges = Slot(uri=KG.edges, name="graph__edges", curie=KG.curie('edges'),
                   model_uri=KG.graph__edges, domain=None, range=Optional[Union[Union[dict, Edge], list[Union[dict, Edge]]]])
