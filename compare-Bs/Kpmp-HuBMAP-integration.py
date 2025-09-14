import argparse
import scanpy as sc
import anndata
import pandas as pd
import re

# Schema
OBS_FIELDS = [
    "consortium", "collection", "dataset_id", "as_id",
    "cl_id", "cl_label", "age", "sex", "race", "disease"
]
VAR_FIELDS = ["gene_name"]

# Filtering helpers
def filter_to_dataset_cell_types(adata, dataset_names, source_col="cell_type"):
    before = adata.n_obs
    mask = adata.obs[source_col].isin(dataset_names)
    adata_filtered = adata[mask, :].copy()
    after = adata_filtered.n_obs
    print(f"Filtered {after}/{before} cells ({before - after} removed) using {source_col}.")
    return adata_filtered

def remove_slide_seq_cells(adata, slide_seq_ids):
    before = adata.n_obs
    mask = adata.obs["hubmap_id"].isin(slide_seq_ids)
    adata_filtered = adata[~mask, :].copy()
    after = adata_filtered.n_obs
    print(f"Removed {before - after} slide-seq cells (kept {after}/{before}).")
    return adata_filtered

# Column cleanups
def add_common_value(adata, is_RK, shared_obs, shared_var):
    adata.obs["as_id"] = "UBERON:0002113"
    adata.obs["disease"] = "normal"
    adata.obs["consortium"] = "HuBMAP"
    adata.obs["collection"] = "HuBMAP Right Kidney" if is_RK else "HuBMAP Left Kidney"
    adata.obs.rename(columns=shared_obs, inplace=True)
    adata.var.rename(columns=shared_var, inplace=True)
    adata.var.index = adata.var.index.to_series().apply(lambda x: re.sub(r"\.\d+$", "", x))
    return adata

def remove_extra_var(adata):
    adata.var = adata.var[VAR_FIELDS]
    return adata

def drop_unique_obs_columns(adata):
    missing = [c for c in OBS_FIELDS if c not in adata.obs.columns]
    if missing:
        print("Warning: Missing columns:", missing)
    adata.obs = adata.obs[[c for c in OBS_FIELDS if c in adata.obs.columns]]
    return adata

def map_the_gene_name(adata, kpmp_var):
    common_genes = kpmp_var.index.intersection(adata.var.index)
    gene_names = kpmp_var.loc[common_genes, "gene_name"].astype(str)
    adata.var["gene_name"] = adata.var.get("gene_name", pd.Series(dtype=str)).astype(str)
    adata.var.loc[common_genes, "gene_name"] = gene_names
    print(f"Updated {len(common_genes)} shared gene names.")
    return adata

def filter_to_dataset_cell_types(adata,dataset_names,source_col='cell_type'):
    mask = adata.obs[source_col].isin(dataset_names)
    adata_filtered = adata[mask, :]
    return adata_filtered

# first mapping
mapping = {
    # exact matches
    'B cell': 'B cell',
    'T cell': 'T cell',
    'conventional dendritic cell': 'conventional dendritic cell',
    'mast cell': 'mast cell',
    'mature NK T cell': 'mature NK T cell',
    'mononuclear phagocyte': 'mononuclear phagocyte',
    'neutrophil': 'neutrophil',
    'non-classical monocyte': 'non-classical monocyte',
    'papillary tips cell': 'papillary tips cell',
    'parietal epithelial cell': 'parietal epithelial cell',
    'plasma cell': 'plasma cell',
    'plasmacytoid dendritic cell, human': 'plasmacytoid dendritic cell, human',
    'podocyte': 'podocyte',
    'kidney interstitial fibroblast': 'kidney interstitial fibroblast',
    'renal interstitial pericyte': 'renal interstitial pericyte',
    # proximal tubule
    'epithelial cell of proximal tubule segment 1': 'epithelial cell of proximal tubule',
    'epithelial cell of proximal tubule segment 2': 'epithelial cell of proximal tubule',
    'epithelial cell of proximal tubule segment 3': 'epithelial cell of proximal tubule',
    # distal convoluted tubule
    'epithelial cell of early distal convoluted tubule': 'kidney distal convoluted tubule epithelial cell',
    'epithelial cell of late distal convoluted tubule': 'kidney distal convoluted tubule epithelial cell',
    # connecting tubule & collecting duct
    'kidney connecting tubule alpha-intercalated cell': 'kidney collecting duct intercalated cell',
    'kidney connecting tubule principal cell': 'kidney collecting duct principal cell',
    'kidney cortex collecting duct intercalated cell': 'kidney collecting duct intercalated cell',
    'kidney outer medulla collecting duct intercalated cell': 'kidney collecting duct intercalated cell',
    'kidney cortex collecting duct principal cell': 'kidney collecting duct principal cell',
    'kidney inner medulla collecting duct principal cell': 'kidney collecting duct principal cell',
    'kidney outer medulla collecting duct principal cell': 'kidney collecting duct principal cell',
    'kidney collecting duct intercalated cell': 'kidney collecting duct intercalated cell',
    'kidney collecting duct principal cell': 'kidney collecting duct principal cell',
    'kidney connecting tubule epithelial cell': 'kidney connecting tubule epithelial cell',
    # loop of Henle
    'kidney loop of Henle cortical thick ascending limb epithelial cell': 
        'kidney loop of Henle thick ascending limb epithelial cell',
    'kidney loop of Henle medullary thick ascending limb epithelial cell': 
        'kidney loop of Henle thick ascending limb epithelial cell',
    'kidney loop of Henle thick ascending limb epithelial cell': 
        'kidney loop of Henle thick ascending limb epithelial cell',
    'kidney loop of Henle thin ascending limb epithelial cell': 
        'kidney loop of Henle thin ascending limb epithelial cell',
    'kidney loop of Henle short descending thin limb epithelial cell': 
        'kidney loop of Henle thin descending limb epithelial cell',
    'kidney loop of Henle long descending thin limb inner medulla epithelial cell': 
        'kidney loop of Henle thin descending limb epithelial cell',
    'kidney loop of Henle long descending thin limb outer medulla epithelial cell': 
        'kidney loop of Henle thin descending limb epithelial cell',
    # endothelial
    'endothelial cell': 'endothelial cell',
}

# Label mapping
label_mapping = {
    # Proximal tubule
    "epithelial cell of proximal tubule": "Proximal tubule epithelial cell",
    "epithelial cell of proximal tubule segment 1": "Proximal tubule epithelial cell",
    "epithelial cell of proximal tubule segment 2": "Proximal tubule epithelial cell",
    "epithelial cell of proximal tubule segment 3": "Proximal tubule epithelial cell",

    # Distal convoluted tubule
    "kidney distal convoluted tubule epithelial cell": "Distal convoluted tubule epithelial cell",
    "epithelial cell of early distal convoluted tubule": "Distal convoluted tubule epithelial cell",
    "epithelial cell of late distal convoluted tubule": "Distal convoluted tubule epithelial cell",

    # Loop of Henle
    "kidney loop of Henle thin descending limb epithelial cell": "Loop of Henle epithelial cell",
    "kidney loop of Henle thin ascending limb epithelial cell": "Loop of Henle epithelial cell",
    "kidney loop of Henle cortical thick ascending limb epithelial cell": "Loop of Henle epithelial cell",
    "kidney loop of Henle medullary thick ascending limb epithelial cell": "Loop of Henle epithelial cell",
    "kidney loop of Henle long descending thin limb outer medulla epithelial cell": "Loop of Henle epithelial cell",
    "kidney loop of Henle long descending thin limb inner medulla epithelial cell": "Loop of Henle epithelial cell",
    "kidney loop of Henle short descending thin limb epithelial cell": "Loop of Henle epithelial cell",

    # Collecting duct principal cells
    "kidney collecting duct principal cell": "Collecting duct principal cell",
    "kidney cortex collecting duct principal cell": "Collecting duct principal cell",
    "kidney outer medulla collecting duct principal cell": "Collecting duct principal cell",
    "kidney inner medulla collecting duct principal cell": "Collecting duct principal cell",

    # Collecting duct intercalated cells
    "kidney collecting duct intercalated cell": "Collecting duct intercalated cell",
    "kidney cortex collecting duct intercalated cell": "Collecting duct intercalated cell",
    "kidney outer medulla collecting duct intercalated cell": "Collecting duct intercalated cell",

    # Connecting tubule
    "kidney connecting tubule epithelial cell": "Connecting tubule epithelial cell",
    "kidney connecting tubule principal cell": "Connecting tubule epithelial cell",
    "kidney connecting tubule alpha-intercalated cell": "Connecting tubule epithelial cell",

    # Other epithelial
    "podocyte": "Podocyte",
    "parietal epithelial cell": "Parietal epithelial cell",
    "papillary tips cell": "Papillary tips cell",

    # Stromal & endothelial
    "endothelial cell": "Endothelial cell",
    "kidney interstitial cell": "Kidney interstitial cell",
    "kidney interstitial fibroblast": "Kidney interstitial fibroblast",
    "kidney interstitial alternatively activated macrophage": "Kidney interstitial alternatively activated macrophage",
    "renal interstitial pericyte": "Renal interstitial pericyte",

    # Immune cells
    "T cell": "T cell",
    "cytotoxic T cell": "T cell",
    "mature NK T cell": "T cell",
    "B cell": "B cell",
    "plasma cell": "Plasma cell",
    "natural killer cell": "Natural killer cell",
    "monocyte": "Monocyte",
    "non-classical monocyte": "Monocyte",
    "conventional dendritic cell": "Dendritic cell",
    "plasmacytoid dendritic cell, human": "Dendritic cell",
    "mononuclear phagocyte": "Mononuclear phagocyte",
    "mast cell": "Mast cell",
    "neutrophil": "Neutrophil",
}

slide_seq=['HBM222.VQSW.335',
 'HBM248.HPXX.584',
 'HBM269.GDLH.894',
 'HBM294.XZLM.256',
 'HBM356.MDPN.792',
 'HBM363.FVKP.935',
 'HBM398.BLRW.228',
 'HBM456.CGDP.395',
 'HBM462.XQCR.933',
 'HBM522.QXVG.468',
 'HBM528.KNCB.488',
 'HBM547.SJSK.268',
 'HBM547.TFRR.794',
 'HBM595.LBXP.486',
 'HBM679.RLJH.432',
 'HBM735.FSBZ.626',
 'HBM757.KLKW.524',
 'HBM775.CMGG.464',
 'HBM785.XFTT.663',
 'HBM834.SLQN.292',
 'HBM883.PHQS.523',
 'HBM976.*','HBM232.MBNR.586', 'HBM266.FTJN.632', 'HBM297.FDTX.382', 'HBM445.HBRO.488',
 'HBM459.KCST.593', 'HBM532.KKRC.477', 'HBM634.JHVB.286', 'HBM634.ZSHF.736',
 'HBM647.QDBG.936', 'HBM736.MNMD.453', 'HBM827.MJMM.447', 'HBM846.KVCF.674',
 'HBM892.CCDZ.345', 'HBM965.PSNC.855', 'HBM986.KFWG.239', 'HBM232.MBNR.586']


# Main workflow
def main():
    parser = argparse.ArgumentParser(description="Normalize, merge, and preprocess KPMP + HuBMAP datasets.")
    parser.add_argument("--kpmp", required=True, help="Path to KPMP")
    parser.add_argument("--hubmap_lk", required=True, help="Path to HuBMAP Left Kidney")
    parser.add_argument("--hubmap_rk", required=True, help="Path to HuBMAP Right Kidney")
    parser.add_argument("--output", required=True, help="Path to save merged file")
    args = parser.parse_args()

    # Load raw datasets
    KPMP_SN_raw = sc.read(args.kpmp)
    HuBMAP_LK_raw = sc.read(args.hubmap_lk)
    HuBMAP_RK_raw = sc.read(args.hubmap_rk)

    # Shared column mappings
    KPMP_shared = {
        "library_id": "dataset_id",
        "tissue_ontology_term_id": "as_id",
        "cell_type_ontology_term_id": "cl_id",
        "cell_type": "cl_label",
        "nCount_RNA": "gene_count",
        "Age_binned": "age",
        "sex": "sex",
        "self_reported_ethnicity": "race",
        "disease": "disease",
    }
    KPMP_var_shared = {"feature_name": "gene_name"}

    HuBMAP_shared = {
        "cell_id": "cell_id",
        "predicted_CLID": "cl_id",
        "predicted_label": "cl_label",
        "n_genes": "gene_count",
        "age": "age",
        "sex": "sex",
        "race": "race",
        "hubmap_id": "dataset_id",
    }
    HuBMap_var_shared = {"hugo_symbol": "gene_name"}

    # Annotate KPMP
    KPMP_SN_raw.obs["consortium"] = "KPMP"
    KPMP_SN_raw.obs["collection"] = "KPMP SC RNAseq"
    KPMP_SN_raw.obs.rename(columns=KPMP_shared, inplace=True)
    KPMP_SN_raw.var.rename(columns=KPMP_var_shared, inplace=True)
    KPMP_SN_raw = remove_extra_var(KPMP_SN_raw)
    KPMP_SN_raw = drop_unique_obs_columns(KPMP_SN_raw)

    # HuBMAP cleaning
    
    HuBMAP_LK_raw = filter_to_dataset_cell_types(HuBMAP_LK_raw, mapping, source_col='predicted_label')
    HuBMAP_RK_raw = filter_to_dataset_cell_types(HuBMAP_RK_raw, mapping, source_col='predicted_label')


    HuBMAP_LK_raw=remove_slide_seq_cells(HuBMAP_LK_raw,slide_seq)
    HuBMAP_RK_raw=remove_slide_seq_cells(HuBMAP_RK_raw,slide_seq)

    HuBMAP_LK_raw = add_common_value(HuBMAP_LK_raw, is_RK=False, shared_obs=HuBMAP_shared, shared_var=HuBMap_var_shared)
    HuBMAP_RK_raw = add_common_value(HuBMAP_RK_raw, is_RK=True, shared_obs=HuBMAP_shared, shared_var=HuBMap_var_shared)

    HuBMAP_LK_raw = remove_extra_var(HuBMAP_LK_raw)
    HuBMAP_RK_raw = remove_extra_var(HuBMAP_RK_raw)

    HuBMAP_LK_raw = drop_unique_obs_columns(HuBMAP_LK_raw)
    HuBMAP_RK_raw = drop_unique_obs_columns(HuBMAP_RK_raw)

    HuBMAP_LK_raw = map_the_gene_name(HuBMAP_LK_raw, KPMP_SN_raw.var)
    HuBMAP_RK_raw = map_the_gene_name(HuBMAP_RK_raw, KPMP_SN_raw.var)

    # Keep shared genes
    shared = (
        KPMP_SN_raw.var.index
        .intersection(HuBMAP_LK_raw.var.index)
        .intersection(HuBMAP_RK_raw.var.index)
    )
    print(f"Found {len(shared)} genes shared across all datasets.")

    KPMP_SN_raw   = KPMP_SN_raw[:, shared].copy()
    HuBMAP_LK_raw = HuBMAP_LK_raw[:, shared].copy()
    HuBMAP_RK_raw = HuBMAP_RK_raw[:, shared].copy()

    # Concatenate datasets
    adata_concat_scvi = anndata.concat(
        [KPMP_SN_raw, HuBMAP_LK_raw, HuBMAP_RK_raw],
        label="batch",
        keys=["KPMP", "HuBMAP_LK", "HuBMAP_RK"],
        axis=0,
        join="inner",
        merge="first",
    )

    # Enforce schema
    adata_concat_scvi.obs = adata_concat_scvi.obs[OBS_FIELDS]
    adata_concat_scvi.var = adata_concat_scvi.var[VAR_FIELDS]

    # QC + normalization
    sc.pp.filter_cells(adata_concat_scvi, min_genes=200)
    sc.pp.filter_genes(adata_concat_scvi, min_cells=3)
    sc.pp.normalize_total(adata_concat_scvi, target_sum=1e4)
    sc.pp.log1p(adata_concat_scvi)

    # Label harmonization
    adata_concat_scvi.obs["general_cl_label"] = adata_concat_scvi.obs["cl_label"].map(label_mapping)
    adata_concat_scvi.obs["general_cl_label"] = adata_concat_scvi.obs["general_cl_label"].fillna(adata_concat_scvi.obs["cl_label"])
    adata_concat_scvi.obs["age"] = adata_concat_scvi.obs["age"].astype(str)

    print(adata_concat_scvi.obs[["cl_label", "general_cl_label"]].head(20))

    print(f"Cells: {adata_concat_scvi.n_obs}")
    print(f"Genes: {adata_concat_scvi.n_vars}")

    # Save
    adata_concat_scvi.write(args.output)


if __name__ == "__main__":
    main()



# !python E:\Research_umich\Professor_He\IU_hackthon\edge_generator\IU_clean.py \
#   --kpmp /scratch/uniqname/path/kpmp-sn-raw-rnaseq.h5ad \
#   --hubmap_lk /scratch/uniqname/path/LK_raw_updated_2025_june.h5ad \
#   --hubmap_rk /scratch/uniqname/path/RK_raw_updated_2025_june.h5ad \
#   --output /scratch/uniqname/path/merged_test.h5ad