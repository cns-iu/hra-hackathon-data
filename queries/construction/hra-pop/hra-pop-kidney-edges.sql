.mode csv
WITH rows AS MATERIALIZED (SELECT * FROM read_csv('/dev/stdin'))
SELECT DISTINCT
  "ct" as subject,
  'http://purl.org/ccf/ccf_located_in' as predicate,
  "as" as object,
  'https://purl.humanatlas.io/graph/hra-pop' as source
FROM rows
UNION ALL
SELECT DISTINCT
  "biomarker" as subject,
  'http://purl.org/ccf/ccf_characterizes' as predicate,
  "ct" as object,
  'https://purl.humanatlas.io/graph/hra-pop' as source
FROM rows
