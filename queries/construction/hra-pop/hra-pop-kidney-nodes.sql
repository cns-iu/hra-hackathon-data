.mode csv
WITH rows AS MATERIALIZED (SELECT * FROM read_csv('/dev/stdin'))
SELECT DISTINCT
  "as" as id,
  "as_label" as name,
  '' as symbol,
  'biolink:GrossAnatomicalStructure' as category,
  'https://purl.humanatlas.io/graph/hra-pop' as provided_by
FROM rows
UNION ALL
SELECT DISTINCT
  "ct" as id,
  "ct_label" as name,
  '' as symbol,
  'biolink:Cell' as category,
  'https://purl.humanatlas.io/graph/hra-pop' as provided_by
FROM rows
UNION ALL
SELECT DISTINCT
  "biomarker" as id,
  "biomarker_label" as name,
  "biomarker_label" as symbol,
  'biolink:Gene' as category,
  'https://purl.humanatlas.io/graph/hra-pop' as provided_by
FROM rows
ORDER BY category, id
