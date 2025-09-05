# Summary of Reports

  ## Table of Contents

* ad-hoc
  * [edges-per-type](#edges-per-type)
  * [Named graphs in the db (named-graphs)](#named-graphs)
  * [node-and-edge-counts](#node-and-edge-counts)
  * [nodes-per-type](#nodes-per-type)
  * [nodes-without-labels](#nodes-without-labels)
* atlas-ad-hoc
  * [asct-disease-evidence](#asct-disease-evidence)
  * [asct-kpmp-phenotype-evidence](#asct-kpmp-phenotype-evidence)
  * [asct-phenotype-evidence](#asct-phenotype-evidence)
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
| https://purl.humanatlas.io/graph/hra-kidney-disease-atlas | 392487 |
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
| # Node Types | 7 |


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
| http://purl.obolibrary.org/obo/MONDO_0000001 | 77 |
| http://purl.obolibrary.org/obo/DOID_4 | 76 |
| http://purl.obolibrary.org/obo/UBERON_0000061 | 71 |


### <a id="nodes-without-labels"></a>nodes-without-labels



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX HRAkda: <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>

SELECT DISTINCT ?iri
FROM HRAkda:
WHERE {
  { ?iri ?pred1 [] }
  UNION
  { 
    [] ?pred2 ?iri
    FILTER(isUri(?iri))
  }
  FILTER NOT EXISTS {
    ?iri rdfs:label [] .
  }
  FILTER(STRSTARTS(STR(?iri), 'http://purl.obolibrary.org/obo/'))
}

```

([View Source](../queries/reports/ad-hoc/nodes-without-labels.rq))
</details>

#### Results ([View CSV File](reports/ad-hoc/nodes-without-labels.csv))

| iri |
| :--- |



### <a id="asct-disease-evidence"></a>asct-disease-evidence



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ccf: <http://purl.org/ccf/>

PREFIX PART_OF: <http://purl.org/ccf/ccf_part_Of>
PREFIX LOCATED_IN: <http://purl.org/ccf/ccf_located_in>
PREFIX CHARACTERIZES: <http://purl.org/ccf/ccf_characterizes>
PREFIX COOCCURS_WITH_DISEASE: <https://purl.humanatlas.io/graph/hra-lit#COOCCURS_WITH_DISEASE>
PREFIX HAS_MODIFIER: <https://purl.humanatlas.io/vocab/hp#has_modifier>
PREFIX ASSOCIATED_WITH: <https://purl.humanatlas.io/vocab/hp#associated_with>
PREFIX value: <http://purl.obolibrary.org/obo/OBI_0001938>

PREFIX HRAkda: <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>
PREFIX HRA: <https://purl.humanatlas.io/collection/hra>
PREFIX HPO: <https://purl.humanatlas.io/vocab/hp>

SELECT DISTINCT ?asct_label ?disease_label ?gene_label ?gene_expr ?publication_count ?asct ?disease ?gene 
WHERE {
  ?asct COOCCURS_WITH_DISEASE: ?disease .
  ?disease skos:exactMatch|skos:narrowMatch|skos:broadMatch ?phenotype .
  ?gene HAS_MODIFIER:|ASSOCIATED_WITH: ?phenotype .
  # ?gene ASSOCIATED_WITH: ?phenotype .
  ?gene CHARACTERIZES: ?ct .
  ?ct LOCATED_IN: ?asct .

  [ a rdf:Statement ;
      rdf:subject ?gene ;
      rdf:predicate CHARACTERIZES: ;
      rdf:object ?ct ;
      value: ?gene_expr ;
  ] .

  [ a rdf:Statement ;
      rdf:subject ?asct ;
      rdf:predicate COOCCURS_WITH_DISEASE: ;
      rdf:object ?disease ;
      value: ?publication_count ;
  ] .

  ?asct rdfs:label ?asct_label .
  ?disease rdfs:label ?disease_label .
  ?gene rdfs:label ?gene_label .
}
ORDER BY DESC(?gene_expr) DESC(?publication_count)

```

([View Source](../queries/reports/atlas-ad-hoc/asct-disease-evidence.rq))
</details>

#### Results ([View CSV File](reports/atlas-ad-hoc/asct-disease-evidence.csv))

| asct_label | disease_label | gene_label | gene_expr | publication_count | asct | disease | gene |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| kidney | Renal Insufficiency, Chronic | ALDOB | 237.78284 | 6355 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://id.nlm.nih.gov/mesh/D051436 | http://identifiers.org/hgnc/417 |
| kidney | Renal Insufficiency | ALDOB | 237.78284 | 2890 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://id.nlm.nih.gov/mesh/D051437 | http://identifiers.org/hgnc/417 |
| kidney | Acidosis, Renal Tubular | ALDOB | 237.78284 | 397 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://id.nlm.nih.gov/mesh/D000141 | http://identifiers.org/hgnc/417 |
| nephron tubule | Renal Insufficiency, Chronic | ALDOB | 237.78284 | 335 | http://purl.obolibrary.org/obo/UBERON_0001231 | http://id.nlm.nih.gov/mesh/D051436 | http://identifiers.org/hgnc/417 |
| nephron tubule | Acidosis, Renal Tubular | ALDOB | 237.78284 | 265 | http://purl.obolibrary.org/obo/UBERON_0001231 | http://id.nlm.nih.gov/mesh/D000141 | http://identifiers.org/hgnc/417 |
| ... | ... | ... | ... | ... | ... | ... | ... |

## atlas-ad-hoc

### <a id="asct-kpmp-phenotype-evidence"></a>asct-kpmp-phenotype-evidence



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ccf: <http://purl.org/ccf/>

PREFIX PART_OF: <http://purl.org/ccf/ccf_part_Of>
PREFIX LOCATED_IN: <http://purl.org/ccf/ccf_located_in>
PREFIX CHARACTERIZES: <http://purl.org/ccf/ccf_characterizes>
PREFIX COOCCURS_WITH_DISEASE: <https://purl.humanatlas.io/graph/hra-lit#COOCCURS_WITH_DISEASE>
PREFIX HAS_MODIFIER: <https://purl.humanatlas.io/vocab/hp#has_modifier>
PREFIX ASSOCIATED_WITH: <https://purl.humanatlas.io/vocab/hp#associated_with>
PREFIX value: <http://purl.obolibrary.org/obo/OBI_0001938>

PREFIX HRAkda: <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>
PREFIX HRA: <https://purl.humanatlas.io/collection/hra>
PREFIX HPO: <https://purl.humanatlas.io/vocab/hp>

SELECT DISTINCT ?asct_label ?phenotype_label ?gene_label ?gene_expr ?publication_count ?asct ?phenotype ?gene 
WHERE {
  ?asct COOCCURS_WITH_DISEASE: ?disease .
  ?disease skos:exactMatch|skos:narrowMatch|skos:broadMatch ?phenotype .
  # ?gene HAS_MODIFIER:|ASSOCIATED_WITH: ?phenotype .
  ?gene ASSOCIATED_WITH: ?phenotype . # Basically limits to just AKI/CKD
  ?gene CHARACTERIZES: ?ct .
  ?ct LOCATED_IN: ?asct .

  [ a rdf:Statement ;
      rdf:subject ?gene ;
      rdf:predicate CHARACTERIZES: ;
      rdf:object ?ct ;
      value: ?gene_expr ;
  ] .

  [ a rdf:Statement ;
      rdf:subject ?asct ;
      rdf:predicate COOCCURS_WITH_DISEASE: ;
      rdf:object ?disease ;
      value: ?publication_count ;
  ] .

  ?asct rdfs:label ?asct_label .
  ?phenotype rdfs:label ?phenotype_label .
  ?gene rdfs:label ?gene_label .
}
ORDER BY DESC(?gene_expr) DESC(?publication_count)

```

([View Source](../queries/reports/atlas-ad-hoc/asct-kpmp-phenotype-evidence.rq))
</details>

#### Results ([View CSV File](reports/atlas-ad-hoc/asct-kpmp-phenotype-evidence.csv))

| asct_label | phenotype_label | gene_label | gene_expr | publication_count | asct | phenotype | gene |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| kidney | Acute kidney injury | IGFBP7 | 48.598885 | 10827 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://purl.obolibrary.org/obo/HP_0001919 | http://identifiers.org/hgnc/5476 |
| nephron tubule | Acute kidney injury | IGFBP7 | 48.598885 | 1762 | http://purl.obolibrary.org/obo/UBERON_0001231 | http://purl.obolibrary.org/obo/HP_0001919 | http://identifiers.org/hgnc/5476 |
| nephron | Acute kidney injury | IGFBP7 | 48.598885 | 164 | http://purl.obolibrary.org/obo/UBERON_0001285 | http://purl.obolibrary.org/obo/HP_0001919 | http://identifiers.org/hgnc/5476 |
| kidney | Acute kidney injury | IGFBP7 | 24.4 | 10827 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://purl.obolibrary.org/obo/HP_0001919 | http://identifiers.org/hgnc/5476 |
| kidney | Acute kidney injury | B2M | 23.835205 | 10827 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://purl.obolibrary.org/obo/HP_0001919 | http://identifiers.org/hgnc/914 |
| ... | ... | ... | ... | ... | ... | ... | ... |


### <a id="asct-phenotype-evidence"></a>asct-phenotype-evidence



<details>
  <summary>View Sparql Query</summary>

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ccf: <http://purl.org/ccf/>

PREFIX PART_OF: <http://purl.org/ccf/ccf_part_Of>
PREFIX LOCATED_IN: <http://purl.org/ccf/ccf_located_in>
PREFIX CHARACTERIZES: <http://purl.org/ccf/ccf_characterizes>
PREFIX COOCCURS_WITH_DISEASE: <https://purl.humanatlas.io/graph/hra-lit#COOCCURS_WITH_DISEASE>
PREFIX HAS_MODIFIER: <https://purl.humanatlas.io/vocab/hp#has_modifier>
PREFIX ASSOCIATED_WITH: <https://purl.humanatlas.io/vocab/hp#associated_with>
PREFIX value: <http://purl.obolibrary.org/obo/OBI_0001938>

PREFIX HRAkda: <https://purl.humanatlas.io/graph/hra-kidney-disease-atlas>
PREFIX HRA: <https://purl.humanatlas.io/collection/hra>
PREFIX HPO: <https://purl.humanatlas.io/vocab/hp>

SELECT DISTINCT ?asct_label ?phenotype_label ?gene_label ?gene_expr ?publication_count ?asct ?phenotype ?gene 
WHERE {
  ?asct COOCCURS_WITH_DISEASE: ?disease .
  ?disease skos:exactMatch|skos:narrowMatch|skos:broadMatch ?phenotype .
  ?gene HAS_MODIFIER:|ASSOCIATED_WITH: ?phenotype .
  ?gene CHARACTERIZES: ?ct .
  ?ct LOCATED_IN: ?asct .

  [ a rdf:Statement ;
      rdf:subject ?gene ;
      rdf:predicate CHARACTERIZES: ;
      rdf:object ?ct ;
      value: ?gene_expr ;
  ] .

  [ a rdf:Statement ;
      rdf:subject ?asct ;
      rdf:predicate COOCCURS_WITH_DISEASE: ;
      rdf:object ?disease ;
      value: ?publication_count ;
  ] .

  ?asct rdfs:label ?asct_label .
  ?phenotype rdfs:label ?phenotype_label .
  ?gene rdfs:label ?gene_label .
}
ORDER BY DESC(?gene_expr) DESC(?publication_count)

```

([View Source](../queries/reports/atlas-ad-hoc/asct-phenotype-evidence.rq))
</details>

#### Results ([View CSV File](reports/atlas-ad-hoc/asct-phenotype-evidence.csv))

| asct_label | phenotype_label | gene_label | gene_expr | publication_count | asct | phenotype | gene |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| kidney | Chronic kidney disease | ALDOB | 237.78284 | 6355 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://purl.obolibrary.org/obo/HP_0012622 | http://identifiers.org/hgnc/417 |
| kidney | Renal insufficiency | ALDOB | 237.78284 | 2890 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://purl.obolibrary.org/obo/HP_0000083 | http://identifiers.org/hgnc/417 |
| kidney | Proximal renal tubular acidosis | ALDOB | 237.78284 | 397 | http://purl.obolibrary.org/obo/UBERON_0002113 | http://purl.obolibrary.org/obo/HP_0002049 | http://identifiers.org/hgnc/417 |
| nephron tubule | Chronic kidney disease | ALDOB | 237.78284 | 335 | http://purl.obolibrary.org/obo/UBERON_0001231 | http://purl.obolibrary.org/obo/HP_0012622 | http://identifiers.org/hgnc/417 |
| nephron tubule | Proximal renal tubular acidosis | ALDOB | 237.78284 | 265 | http://purl.obolibrary.org/obo/UBERON_0001231 | http://purl.obolibrary.org/obo/HP_0002049 | http://identifiers.org/hgnc/417 |
| ... | ... | ... | ... | ... | ... | ... | ... |


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


  