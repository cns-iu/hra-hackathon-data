# %%
import pandas as pd
import biorosetta as br
import hpotk
import typing
from hpotk import TermId
import os
import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# This notebook collects the sources to integrate HPO and HRA as a knowledge graph (KG). The KG will be agregated in the form of nodes and edges. In thecase of HPO we have the following nodes:
# 
# - Genes
# - Phenotypes
# - Anatomical structures (AS)
# 
# The nodes tables will have the following format: iri | label | type | source
# 
# The edge table explains the relationships between theser nodes. In HPO, The only direct relationship between the above mentioned nodes is between genes and phenotypes, we will just focus on this and will work on the other relatiosnhips later. 
# 
# The edges table will have the following format: subject | predicate | object | source

# %% [markdown]
# # Genes Table

# %% [markdown]
# ##### Load  genes_to_phenotype.txt file form HPO: https://hpo.jax.org/data/ontology
# 
# version:v2025-08-11

# %%
hpo_genes_to_phenotype = pd.read_csv("./HRA_HPO_integration/data/genes_to_phenotype_v2025-08-11.txt", sep="\t")
hpo_genes_to_phenotype.head()
hpo_genes_to_phenotype['ncbi_gene_id'] = hpo_genes_to_phenotype['ncbi_gene_id'].astype(str)
hpo_genes_to_phenotype.head()

# %% [markdown]
# ### Subset HPO to those related to kidney:

# %%
store = hpotk.configure_ontology_store()
hpo = store.load_hpo(release='v2025-05-06')

def get_all_decendant_hpo_term_dict(
    hpo: hpotk.MinimalOntology, parent_TermID: str = "HP:0003674"
) -> typing.Set[TermId]:
    """
    Retrieve all descendant onset TermIds from a specified parent term ID in an ontology.

    :param parent_TermID: The parent term ID to find descendants for, defaults to 'HP:0003674'.
    :param hpo: The ontology instance containing term relationships.
    :return: A set of onset TermIds derived from the given parent term ID.
    """
    descendant_term_id_dict = dict()
    for term in hpo.graph.get_descendants(parent_TermID):
        descendant_term_id_dict[term.value] = hpo.get_term_name(term)
    return descendant_term_id_dict

# %% [markdown]
# #### 'HP:0000077' corresponds to 'Abnormality of the kidney'
# ##### We assume that all the terms that are the decendants of 'Abnormality of the kidney' are kidney related HPO terms
# #### We subset the HPO term - phenotype relationships table to those terms related to kidney

# %%

kidney_related_hpo_dict = get_all_decendant_hpo_term_dict(hpo=hpo, parent_TermID='HP:0000077')


# %%
hpo_genes_to_phenotype_kidney = hpo_genes_to_phenotype[hpo_genes_to_phenotype['hpo_id'].isin(kidney_related_hpo_dict.keys())]

# %%
hpo_genes_to_phenotype_kidney

# %% [markdown]
# ### Map the NCBI IDs and the gene symbols to HGNC IDs

# %%
# get the idmapper from biorosetta
idmap = br.IDMapper([br.EnsemblBiomartMapper(),br.HGNCBiomartMapper(),br.MyGeneMapper()])

# %%
NCBI_geneSymbol_HGNC_mapping = hpo_genes_to_phenotype[['ncbi_gene_id', 'gene_symbol']]
NCBI_geneSymbol_HGNC_mapping.drop_duplicates(inplace=True)
NCBI_geneSymbol_HGNC_mapping.loc[:, 'NCBI_to_HGNC'] = list(idmap.convert(NCBI_geneSymbol_HGNC_mapping['ncbi_gene_id'],'entr','hgnc'))
NCBI_geneSymbol_HGNC_mapping.loc[:, 'geneSymbol_to_HGNC'] = list(idmap.convert(NCBI_geneSymbol_HGNC_mapping['gene_symbol'],'symb','hgnc'))
NCBI_geneSymbol_HGNC_mapping

# %%
NCBI_geneSymbol_HGNC_mapping.loc[NCBI_geneSymbol_HGNC_mapping['gene_symbol']=='-',:].shape[0]

# %%
NCBI_geneSymbol_HGNC_mapping.loc[NCBI_geneSymbol_HGNC_mapping['geneSymbol_to_HGNC']=='N/A',:].shape[0]

# %%
NCBI_geneSymbol_HGNC_mapping.loc[
    (NCBI_geneSymbol_HGNC_mapping['geneSymbol_to_HGNC'] != 'N/A') & 
    (NCBI_geneSymbol_HGNC_mapping['NCBI_to_HGNC'] == 'N/A')
]

# %%
NCBI_geneSymbol_HGNC_mapping.loc[
    (NCBI_geneSymbol_HGNC_mapping['gene_symbol']=='-') & 
    (NCBI_geneSymbol_HGNC_mapping['NCBI_to_HGNC'] != 'N/A')
]

# %% [markdown]
# #### the best way of mapping NCBI - gene symbol - HGNC is thorugh gene symbols.
# 
# - 6 NCBI genes do not have any corresponding symbol or genes
# - 41 NCBI genes do not have corresponding HGNC ID
# - 19 gene symbols do not have any corresponding HGNC ID
# 
# Therefore, we can use gene symbols as the bridge and in this way we map 5167/5186 genes 

# %%
NCBI_geneSymbol_HGNC_mapping_complete = NCBI_geneSymbol_HGNC_mapping.loc[NCBI_geneSymbol_HGNC_mapping['geneSymbol_to_HGNC']!='N/A',:]
NCBI_geneSymbol_HGNC_mapping_complete.tail()

# %% [markdown]
# ### map hpo_genes_to_phenotype_kidney ncbi ids to HGNC though gene symbols using NCBI_geneSymbol_HGNC_mapping lookup table

# %%
# remove the rows without any gene symbol
hpo_genes_to_phenotype_kidney_annotated = hpo_genes_to_phenotype_kidney.copy()
hpo_genes_to_phenotype_kidney_annotated = hpo_genes_to_phenotype_kidney_annotated.loc[hpo_genes_to_phenotype_kidney_annotated['gene_symbol']!='-',:]
hpo_genes_to_phenotype_kidney_annotated

# %%

# add HGNC annotations
hpo_genes_to_phenotype_kidney_annotated['HGNC'] = [NCBI_geneSymbol_HGNC_mapping_complete[NCBI_geneSymbol_HGNC_mapping_complete['gene_symbol']==x].loc[:, 'geneSymbol_to_HGNC'].values[0] for x in hpo_genes_to_phenotype_kidney_annotated['gene_symbol']]
hpo_genes_to_phenotype_kidney_annotated

# %%
gene_nodes_table = pd.DataFrame({
    'iri':['http://identifiers.org/hgnc/'+ a.split(':')[-1] for a in hpo_genes_to_phenotype_kidney_annotated['HGNC']],
    'label': hpo_genes_to_phenotype_kidney_annotated['gene_symbol'],
    'type':'http://purl.bioontology.org/ontology/HGNC/gene',
    'source':'https://purl.humanatlas.io/vocab/hp'
})
gene_nodes_table.drop_duplicates(inplace=True)

# %%
gene_nodes_table.to_csv('./input-csvs/hpo-kidney-genes-nodes.csv', index=False)

# %% [markdown]
# # Phenotypes Table

# %%
phenotype_nodes_table = pd.DataFrame({
    'iri':['http://purl.obolibrary.org/obo/HP_'+ a.split(':')[-1] for a in hpo_genes_to_phenotype_kidney_annotated['hpo_id']],
    'label': hpo_genes_to_phenotype_kidney_annotated['hpo_name'],
    'type':'http://purl.obolibrary.org/obo/HP_0000118', # phenotypic abnormality
    'source':'https://purl.humanatlas.io/vocab/hp'
})

phenotype_nodes_table_complete = phenotype_nodes_table.drop_duplicates()
phenotype_nodes_table_complete = phenotype_nodes_table_complete.reset_index(drop=True)
phenotype_nodes_table_complete.head()

# %%
phenotype_nodes_table_complete.to_csv('./input-csvs/hpo-kidney-phenotypes-nodes.csv', index=False)

# %% [markdown]
# # Edge tables for phenotypes
# 
#  Subject | Predicate | Object
# 

# %%
hpo_genes_to_phenotype_kidney_annotated['hgnc_iri']= ['http://identifiers.org/hgnc/'+ a.split(':')[-1] for a in hpo_genes_to_phenotype_kidney_annotated['HGNC']]
hpo_genes_to_phenotype_kidney_annotated.head()

# %%


edge_table = pd.DataFrame({'subject': hpo_genes_to_phenotype_kidney_annotated['hgnc_iri'],
                            'predicate': 'https://purl.humanatlas.io/vocab/hp#has_modifier', 
                            'object': ['http://purl.obolibrary.org/obo/HP_' + a.split(':')[-1] for a in hpo_genes_to_phenotype_kidney_annotated['hpo_id']],
                            'source':'https://purl.humanatlas.io/vocab/hp'
                            })
edge_table

# %%
edge_table.to_csv('./input-csvs/hpo-kidney-genes-to-phenotype-edges.csv', index=False)

# %% [markdown]
# # AS table:
# 
#     
# 

# %% [markdown]
# #### The the input files to this notebook are retrieved from this repo: https://github.com/aybugealtay/OntoXRefExtractor
# 
# - Bruce provided renal-system-specific (http://purl.obolibrary.org/obo/UBERON_0001008) anatomical structures: https://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/hra/as-parts.csv?location=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FUBERON_0001008 --> this files is stored as renal_sytem_AS.csv
# 
# 
# - Organize the results as subject/predicate/object/source format and subset them to renal system related anatomical structures:

# %% [markdown]
# ### uberon links

# %%
all_uberon_xlinks = pd.read_csv('./HRA_HPO_integration/data/hpo_to_uberon_links.csv', index_col=None)
all_uberon_xlinks

# %%
all_uberon_xlinks_uberon = all_uberon_xlinks[all_uberon_xlinks['Filler_Label'].str.contains('kidney', case=False, na=False)]

# %%
len(all_uberon_xlinks['Filler_IRI'].unique())

# %%
renal_system_as = pd.read_csv('./HRA_HPO_integration/data/renal_system_AS.csv', index_col=None)
renal_system_as.head()

# %%
# Filter the DataFrame using the pattern
all_uberon_xlinks_kidney = all_uberon_xlinks[
    all_uberon_xlinks['Filler_IRI'].isin(renal_system_as['part_iri'].tolist())
]
all_uberon_xlinks_kidney.head()

# %%
hpo_asct_kidney_edges = all_uberon_xlinks_kidney[['HPO_IRI','Property','Filler_IRI']]
hpo_asct_kidney_edges['predicate'] = 'https://purl.humanatlas.io/vocab/hp#' + hpo_asct_kidney_edges['Property'].str.replace(' ', '_')
hpo_asct_kidney_edges['source'] = 'https://purl.humanatlas.io/vocab/hp'


# %%
hpo_asct_kidney_edges.drop(columns=['Property'], inplace=True)
hpo_asct_kidney_edges.columns = ['subject', 'object', 'predicate', 'source' ]

hpo_asct_kidney_edges.reindex(['subject', 'predicate', 'object', 'source' ], axis=1)


# %%
hpo_asct_kidney_edges.to_csv('./input-csvs/hpo-asct-kidney-edges.csv', index=False)

# %% [markdown]
# ### now, create a nodes table for the uberon terms:

# %%
all_uberon_xlinks_kidney.head()

# %%
hpo_kidney_as_nodes = all_uberon_xlinks_kidney[['Filler_IRI', 'Filler_Label']]
hpo_kidney_as_nodes['type'] = 'http://purl.obolibrary.org/obo/UBERON_0000061' # UBERON term for anatomical structure
hpo_kidney_as_nodes['source'] = 'https://purl.humanatlas.io/vocab/hp'
hpo_kidney_as_nodes.columns = ['iri', 'label', 'type', 'source']
hpo_kidney_as_nodes.head()
hpo_kidney_as_nodes.to_csv('./input-csvs/hpo-kidney-as-nodes.csv', index=False)




