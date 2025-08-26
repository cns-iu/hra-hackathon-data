# Summary of Reports

  ## Table of Contents

* ad-hoc
  * [Named graphs in the db (named-graphs)](#named-graphs)



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
| https://purl.humanatlas.io/graph/hra-kidney-disease-atlas | 451575 |
| https://purl.humanatlas.io/vocab/cl | 99013 |
| https://purl.humanatlas.io/vocab/hp | 903078 |
| https://purl.humanatlas.io/vocab/uberon | 1181703 |

## ad-hoc

  