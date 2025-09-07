# install pandas and requests before running the code!
import pandas as pd
import requests

# data needed
MARKER_GENES = [
    "CCL21", "NRXN1", "SLC9A3", "SPP1", "SERPINE2",
    "IL18", "NBAS", "TIMP2", "IGFBP7",
    "SUGP1", "APOA1", "MMP9", "ITGAM", "FEV",
    "TFF3", "B2M", "S100A6", "IL10", "IL6",
    "CXCL8", "LCN2", "HAVCR1", "CST3", "CCL2", "FABP1",
]

# IRI data and file saving path
PHENOTYPES = {
    "Acute kidney injury": "http://purl.obolibrary.org/obo/HP_0001919"
}

PREDICATE_IRI = "https://purl.humanatlas.io/vocab/hp#associated_with"
SOURCE_DOI = "https://doi.org/10.1101/2024.04.01.587658"

GENE_TYPE_IRI = "http://purl.bioontology.org/ontology/HGNC/gene"
SOURCE_VOCAB = "https://purl.humanatlas.io/vocab/hp"

EDGES_CSV = "kpmp-amia-gene-to-phenotype-edges.csv"
NODES_CSV = "kpmp-amia-gene-to-phenotype-nodes.csv"


# fetch the iri for genes
def fetch_hgnc_iri(gene: str) -> dict:
    url = "https://www.ebi.ac.uk/ols/api/search"
    params = {"q": gene, "ontology": "hgnc", "exact": "true"}

    r = requests.get(url, params=params)
    data = r.json()
    hit = data["response"]["docs"][0]
    iri_raw = hit.get("iri")
    label = hit.get("label")
    iri = None
    if iri_raw:
        suffix = iri_raw.rsplit("/", 1)[-1]
        iri = f"http://identifiers.org/hgnc/{suffix}"
    return {"gene": gene, "iri": iri, "label": label}


def main():

    # Build the df
    records = [fetch_hgnc_iri(g) for g in MARKER_GENES]
    df_hgnc = pd.DataFrame(records)

    # Build Gene nodes 
    df_nodes_genes = pd.DataFrame(
        {
            "iri": df_hgnc["iri"],
            "label": df_hgnc["gene"],  
            "type": GENE_TYPE_IRI,
            "source": SOURCE_VOCAB,
        }
    )

    # Build Phenotype nodes
    df_nodes_pheno = pd.DataFrame(
        [{"iri": iri, "label": lbl, "type": "http://purl.obolibrary.org/obo/hp", "source": SOURCE_VOCAB}
         for lbl, iri in PHENOTYPES.items()]
    )

    # Combined the Gene nodes and Phenotype nodes
    df_nodes = (
        pd.concat([df_nodes_genes, df_nodes_pheno], ignore_index=True)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    # Build edges files
    edge_rows = []
    for _, row in df_hgnc.iterrows():
        for phen_iri in PHENOTYPES.values():
            edge_rows.append(
                {
                    "subject": row["iri"],
                    "predicate": PREDICATE_IRI,
                    "object": phen_iri,
                    "source": SOURCE_DOI,
                }
            )

    df_edges = pd.DataFrame(edge_rows).drop_duplicates().reset_index(drop=True)

    df_nodes.to_csv(NODES_CSV, index=False)
    df_edges.to_csv(EDGES_CSV, index=False)


if __name__ == "__main__":
    main()