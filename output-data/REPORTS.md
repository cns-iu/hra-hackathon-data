# Summary of Reports

  ## Table of Contents

* ad-hoc
  * [edges-per-type](#edges-per-type)
  * [Named graphs in the db (named-graphs)](#named-graphs)
  * [node-and-edge-counts](#node-and-edge-counts)
  * [nodes-per-type](#nodes-per-type)
* atlas-ad-hoc
  * [gene-expr-paths](#gene-expr-paths)



### <a id="edges-per-type"></a>edges-per-type



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?type (COUNT(*) AS ?count)
FROM <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>
WHERE {
  [] a rdf:Statement ;
    rdf:predicate ?type .
}
GROUP BY ?type
ORDER BY DESC(?count)

```

([View Source](../queries/reports/ad-hoc/edges-per-type.rq))
</details>

#### Results ([View CSV File](reports/ad-hoc/edges-per-type.csv))

| type | count |
| :--- | :--- |
| http://purl.org/ccf/ccf_characterizes | 43819 |
| https://purl.humanatlas.io/vocab/hp#has_modifier | 5074 |
| https://purl.humanatlas.io/graph/hra-lit#COOCCURS_WITH_DISEASE | 981 |
| http://purl.org/ccf/ccf_located_in | 352 |
| http://purl.org/ccf/ccf_part_of | 313 |
| ... | ... |

## ad-hoc

### <a id="named-graphs"></a>Named graphs in the db (named-graphs)

All named graphs in the queried SPARQL database

<details>
  <summary>View Sparql Query</summary>

```sparql
#+ summary: Named graphs in the db
#+ description: All named graphs in the queried SPARQL database

SELECT ?graph (COUNT(*) as ?triples) WHERE {
  GRAPH ?graph {
    ?s ?p ?o .
  }
}
GROUP BY ?graph
ORDER BY ?graph

```

([View Source](../queries/reports/ad-hoc/named-graphs.rq))
</details>

#### Results ([View CSV File](reports/ad-hoc/named-graphs.csv))

| graph | triples |
| :--- | :--- |
| https://purl.humanatlas.io/collection/hra | 2120944 |
| https://purl.humanatlas.io/collection/hra-api | 2006982 |
| https://purl.humanatlas.io/graph/ccf | 557123 |
| https://purl.humanatlas.io/graph/hra-kidney-disease-atlas | 458067 |
| https://purl.humanatlas.io/vocab/cl | 99013 |
| https://purl.humanatlas.io/vocab/hp | 903078 |
| https://purl.humanatlas.io/vocab/uberon | 1181703 |


### <a id="node-and-edge-counts"></a>node-and-edge-counts



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?count
FROM <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>
WHERE {
  {
    SELECT ("# Nodes" as ?label) (COUNT(*) as ?count)
    WHERE {
      SELECT DISTINCT ?s 
      WHERE {
        ?s a owl:Class .
      }
    }
  }
  UNION
  {
    SELECT ("# Edges" as ?label) (COUNT(*) as ?count)
    WHERE {
      SELECT DISTINCT ?s 
      WHERE {
        ?s a rdf:Statement .
      }
    }
  }
  UNION
  {
    SELECT ("# Node Types" as ?label) (COUNT(*) as ?count)
    WHERE {
      SELECT DISTINCT ?class
      WHERE {
        ?s a owl:Class ;
          a ?class .
        FILTER(?class != owl:Class)
      }
    }
  }
  UNION
  {
    SELECT ("# Edge Types" as ?label) (COUNT(*) as ?count)
    WHERE {
      SELECT DISTINCT ?p
      WHERE {
        [] a rdf:Statement ;
          rdf:predicate ?p .
      }
    }
  }
}
ORDER BY DESC(?count)

```

([View Source](../queries/reports/ad-hoc/node-and-edge-counts.rq))
</details>

#### Results ([View CSV File](reports/ad-hoc/node-and-edge-counts.csv))

| label | count |
| :--- | :--- |
| # Edges | 50780 |
| # Nodes | 13028 |
| # Edge Types | 10 |
| # Node Types | 8 |


### <a id="nodes-per-type"></a>nodes-per-type



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class (COUNT(DISTINCT(?s)) AS ?count)
FROM <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>
WHERE {
  ?s a owl:Class ;
    a ?class .
  FILTER(?class != owl:Class)
}
GROUP BY ?class
ORDER BY DESC(?count)

```

([View Source](../queries/reports/ad-hoc/nodes-per-type.rq))
</details>

#### Results ([View CSV File](reports/ad-hoc/nodes-per-type.csv))

| class | count |
| :--- | :--- |
| http://purl.bioontology.org/ontology/HGNC/gene | 12439 |
| http://purl.obolibrary.org/obo/HP_0000118 | 193 |
| http://id.nlm.nih.gov/mesh/D004194 | 87 |
| http://purl.obolibrary.org/obo/CL_0000000 | 85 |
| http://id.nlm.nih.gov/mesh/D007674 | 85 |
| http://purl.obolibrary.org/obo/MONDO_0000001 | 77 |
| http://purl.obolibrary.org/obo/DOID_4 | 76 |
| http://purl.obolibrary.org/obo/UBERON_0000061 | 71 |


### <a id="gene-expr-paths"></a>gene-expr-paths



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ccf: <http://purl.org/ccf/>

PREFIX PART_OF: <http://purl.org/ccf/ccf_part_Of>
PREFIX LOCATED_IN: <http://purl.org/ccf/ccf_located_in>
PREFIX CHARACTERIZES: <http://purl.org/ccf/ccf_characterizes>
PREFIX HAS_MODIFIER: <https://purl.humanatlas.io/vocab/hp#has_modifier>
PREFIX expression_level: <http://purl.obolibrary.org/obo/OBI_0001938>

PREFIX HRAkda: <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>
PREFIX HRA: <https://purl.humanatlas.io/collection/hra>
PREFIX HPO: <https://purl.humanatlas.io/vocab/hp>

SELECT ?mean_gene_expr ?gene ?ct ?as ?phenotype ?gene_label ?ct_label ?as_label ?phenotype_label ?num_sources
FROM HRAkda:
WHERE {
  {
    SELECT DISTINCT ?ct ?gene (AVG(?exp) as ?mean_gene_expr) (COUNT(DISTINCT(?source)) as ?num_sources)
    WHERE {
      [] a rdf:Statement ;
        rdf:subject ?gene ;
        rdf:predicate CHARACTERIZES: ;
        rdf:object ?ct ;
        rdfs:isDefinedBy ?source ;
        expression_level: ?exp .
    }
    GROUP BY ?ct ?gene
    HAVING (?mean_gene_expr > 1.0)
  }

  ?ct LOCATED_IN: ?as .
  ?gene HAS_MODIFIER: ?phenotype .

  GRAPH HRA: {
    ?as rdfs:label ?as_label .
    ?ct rdfs:label ?ct_label .
    ?gene rdfs:label ?gene_label .
  }
  GRAPH HPO: {
    ?phenotype rdfs:label ?phenotype_label .
  }
}
ORDER BY ?as ?ct DESC(?mean_gene_expr)

```

([View Source](../queries/reports/atlas-ad-hoc/gene-expr-paths.rq))
</details>

#### Results ([View CSV File](reports/atlas-ad-hoc/gene-expr-paths.csv))

| mean_gene_expr | gene | ct | as | phenotype | gene_label | ct_label | as_label | phenotype_label | num_sources |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 3.843714 | http://identifiers.org/hgnc/10327 | http://purl.obolibrary.org/obo/CL_0000084 | http://purl.obolibrary.org/obo/UBERON_0001228 | http://purl.obolibrary.org/obo/HP_0000085 | RPL26 | T cell | renal papilla | Horseshoe kidney | 1 |
| 3.843714 | http://identifiers.org/hgnc/10327 | http://purl.obolibrary.org/obo/CL_0000084 | http://purl.obolibrary.org/obo/UBERON_0001228 | http://purl.obolibrary.org/obo/HP_0000104 | RPL26 | T cell | renal papilla | Renal agenesis | 1 |
| 3.843714 | http://identifiers.org/hgnc/10327 | http://purl.obolibrary.org/obo/CL_0000084 | http://purl.obolibrary.org/obo/UBERON_0001228 | http://purl.obolibrary.org/obo/HP_0000122 | RPL26 | T cell | renal papilla | Unilateral renal agenesis | 1 |
| 2.8935435 | http://identifiers.org/hgnc/132 | http://purl.obolibrary.org/obo/CL_0000084 | http://purl.obolibrary.org/obo/UBERON_0001228 | http://purl.obolibrary.org/obo/HP_0000126 | ACTB | T cell | renal papilla | Hydronephrosis | 1 |
| 2.853652 | http://identifiers.org/hgnc/10369 | http://purl.obolibrary.org/obo/CL_0000084 | http://purl.obolibrary.org/obo/UBERON_0001228 | http://purl.obolibrary.org/obo/HP_0000085 | RPL9 | T cell | renal papilla | Horseshoe kidney | 1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## atlas-ad-hoc

  