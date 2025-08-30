.mode csv
WITH rows AS MATERIALIZED (SELECT * FROM read_csv('/dev/stdin'))
SELECT DISTINCT
  "as" as iri,
  "as_label" as label,
  'http://purl.obolibrary.org/obo/UBERON_0000061' as type,
  'https://purl.humanatlas.io/graph/hra-pop' as source
FROM rows
UNION ALL
SELECT DISTINCT
  "ct" as iri,
  "ct_label" as label,
  'http://purl.obolibrary.org/obo/CL_0000000' as type,
  'https://purl.humanatlas.io/graph/hra-pop' as source
FROM rows
UNION ALL
SELECT DISTINCT
  "biomarker" as iri,
  "biomarker_label" as label,
  'http://purl.bioontology.org/ontology/HGNC/gene' as type,
  'https://purl.humanatlas.io/graph/hra-pop' as source
FROM rows
ORDER BY type, iri
