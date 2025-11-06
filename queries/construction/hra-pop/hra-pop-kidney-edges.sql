.mode csv
WITH rows AS MATERIALIZED (SELECT * FROM read_csv('/dev/stdin'))
SELECT DISTINCT
  "ct" as subject,
  'biolink:located_in' as predicate,
  "as" as object,
  'biolink:CellToAnatomicalEntityAssociation' as category,
  'statistical_association' as knowledge_level,
  'automated_agent' as agent_type,
  'https://purl.humanatlas.io/graph/hra-pop' as primary_knowledge_source,
  '' as gene_expr
FROM rows
UNION ALL
SELECT DISTINCT
  "biomarker" as subject,
  'biolink:expressed_in' as predicate,
  "ct" as object,
  'biolink:GeneToEntityAssociation' as category,
  'statistical_association' as knowledge_level,
  'automated_agent' as agent_type,
  'https://purl.humanatlas.io/graph/hra-pop' as primary_knowledge_source,
  "gene_expr" as gene_expr
FROM rows
