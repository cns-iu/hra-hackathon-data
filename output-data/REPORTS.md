# Summary of Reports

  ## Table of Contents

* ad-hoc
  * [Named graphs in the db (named-graphs)](#named-graphs)
  * [node-and-edge-counts](#node-and-edge-counts)
  * [nodes-per-type](#nodes-per-type)



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
| https://purl.humanatlas.io/graph/hra-kidney-disease-atlas | 446463 |
| https://purl.humanatlas.io/vocab/cl | 99013 |
| https://purl.humanatlas.io/vocab/hp | 903078 |
| https://purl.humanatlas.io/vocab/uberon | 1181703 |

## ad-hoc

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
| # Edges | 49642 |
| # Nodes | 12763 |
| # Node Types | 4 |
| # Edge Types | 4 |


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
| http://purl.bioontology.org/ontology/HGNC/gene | 12436 |
| http://purl.obolibrary.org/obo/HP_0000118 | 183 |
| http://purl.obolibrary.org/obo/CL_0000000 | 80 |
| http://purl.obolibrary.org/obo/UBERON_0000061 | 64 |


  