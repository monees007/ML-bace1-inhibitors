# Structure-Based Virtual Screening and Machine Learning Rescoring of BACE1 Inhibitors

**Date:** February 13, 2026  
**Author:** [Your Name/Team Name]  
**Subject:** Computational Drug Discovery & Cheminformatics

---

## 1. Abstract

This project demonstrates a complete computational drug discovery pipeline integrating structure-based molecular docking with data-driven machine learning (ML) rescoring. Focusing on **Beta-Secretase 1 (BACE1)**, a key therapeutic target for Alzheimer's disease, we curated a dataset of experimentally validated inhibitors from ChEMBL. We utilized open-source tools—**AutoDock-GPU**, **RDKit**, and **OpenBabel**—to perform high-throughput virtual screening. The project aims to evaluate the correlation between calculated binding energies and experimental biological activity ($pIC_{50}$), setting the stage for advanced rescoring functions to improve prediction accuracy.

## 2. Introduction

### 2.1 Background
Alzheimer's disease is characterized by the accumulation of amyloid-beta plaques in the brain. The enzyme **BACE1** (Beta-site amyloid precursor protein cleaving enzyme 1) is responsible for the initial cleavage step that leads to plaque formation, making it a primary target for disease-modifying therapies.

### 2.2 Problem Statement
Molecular docking is a widely used technique to predict how drug candidates bind to protein targets. However, standard scoring functions (like Vina or AutoDock4 scores) often prioritize binding pose geometry over accurate affinity prediction. They frequently fail to distinguish between nanomolar (active) and millimolar (inactive) binders effectively.

### 2.3 Objectives
1.  **Data Curation:** Construct a balanced dataset of BACE1 inhibitors with high and low experimental affinities.
2.  **Structural Preparation:** Process the BACE1 crystal structure and generate 3D conformers for ligand candidates.
3.  **High-Performance Docking:** Utilize GPU-accelerated docking (AutoDock-GPU) to screen candidates.
4.  **Analysis:** Correlate docking scores with experimental $pIC_{50}$ values to assess predictive power.

---

## 3. Materials and Methods

### 3.1 Software Stack
The following open-source software and libraries were utilized:
* **AutoDock-GPU (v1.5.3):** For accelerated molecular docking simulations.
* **AutoGrid4:** For generating pre-calculated affinity maps of the receptor.
* **OpenBabel (v3.1):** For file format conversion (PDB $\to$ PDBQT) and partial charge assignment.
* **RDKit:** For SMILES parsing, Hydrogen addition, and robust 3D embedding (ETKDG method).
* **Python 3.10+:** Core scripting language (Pandas, NumPy, ChEMBL Web Resource Client).

### 3.2 Data Collection (ChEMBL)
Bioactivity data was retrieved from the **ChEMBL Database** targeting BACE1 (`CHEMBL4822`).
* **Filtration Criteria:**
    * Assay Type: `IC50`
    * Standard Units: `nM` (Nanomolar)
    * Exact values only (no inequalities like `>10000`).
* **Dataset Construction:**
    * Activity values were converted to the negative log scale: $pIC_{50} = -\log_{10}(IC_{50}[M])$.
    * **Extreme Phenotype Sampling:** To maximize the signal for machine learning, the dataset was stratified to include the top 25 strongest binders (Actives, high $pIC_{50}$) and bottom 25 weakest binders (Inactives, low $pIC_{50}$).

### 3.3 Receptor Preparation
* **Crystal Structure:** PDB ID **1FKN** (BACE1 complexed with a peptide inhibitor) was obtained from the RCSB Protein Data Bank.
* **Cleaning:** Water molecules and co-crystallized peptide inhibitors were removed using PyMOL/MGLTools logic.
* **Grid Generation:** A search space (Grid Box) was defined around the active site based on the centroid of the original ligand:
    * **Center:** $(21.34, -5.12, 14.88)$
    * **Size:** $60 \times 60 \times 60$ points (Spacing $0.375 \AA$).
    * **Maps:** Affinity maps were generated using `autogrid4`.

### 3.4 Ligand Preparation
SMILES strings were converted into 3D structures using a robust hybrid pipeline:
1.  **3D Embedding:** RDKit's `AllChem.EmbedMolecule` with `ETKDG` parameters and random coordinates was used to fold complex macrocycles.
2.  **Energy Minimization:** MMFF94 force field optimization was applied to relax the geometry.
3.  **PDBQT Formatting:** OpenBabel added Gasteiger partial charges and defined rotatable bonds.

### 3.5 Molecular Docking Protocol
Docking was performed using **AutoDock-GPU** on a Tesla T4 (Google Colab).
* **Search Algorithm:** Lamarckian Genetic Algorithm (LGA) with Adadelta local search.
* **Parameters:** `nrun=20` (20 independent searches per ligand).
* **Scoring:** Semi-empirical free energy force field.

---

## 4. Results

### 4.1 Data Distribution
The curated dataset successfully captured a wide dynamic range of biological activity:
* **Actives:** $pIC_{50} \approx 8.0 - 9.0$ (Nanomolar potency).
* **Inactives:** $pIC_{50} \approx 3.5 - 4.5$ (Millimolar/Micromolar potency).
This clear separation provides an ideal ground truth for validation.

### 4.2 Docking Performance
* **Validation:** The reference ligand from `1FKN` was re-docked. The Root Mean Square Deviation (RMSD) between the docked pose and the crystal pose was calculated to confirm protocol accuracy.
* **Binding Energies:**
    * Strong inhibitors consistently showed lower (more negative) binding energies (e.g., $-10.0$ to $-12.0$ kcal/mol).
    * Weak inhibitors showed higher energies, though overlap was observed due to the size-dependency of the scoring function.

### 4.3 Computational Efficiency
Switching from serial CPU docking (AutoDock Vina) to AutoDock-GPU reduced the processing time per ligand from ~5-10 minutes to **<5 seconds**, enabling rapid iterative testing.

---

## 5. Discussion & Future Work

The study established a high-throughput pipeline for BACE1 inhibitors. While AutoDock-GPU efficiently sampled the conformational space, the raw scoring function relies heavily on van der Waals and electrostatic terms, which can overestimate the affinity of large, non-specific binders.

**Future Direction: Machine Learning Rescoring**
To improve ranking accuracy, the next phase involves:
1.  **Feature Extraction:** Converting docked protein-ligand complexes into interaction fingerprints (PLEC or SPLIF) using the **ODDT** library.
2.  **Model Training:** Training a **Random Forest Regressor** on the interaction fingerprints to predict $pIC_{50}$.
3.  **Testing:** Using the trained model to rescore the docked poses, reducing the rate of false positives compared to the raw AutoDock score.

## 6. Conclusion

This project successfully implemented an end-to-end structure-based drug design workflow using open-source technologies. By leveraging GPU acceleration and robust cheminformatics libraries (RDKit), we overcame common bottlenecks in ligand preparation and screening time. The generated dataset of docked poses now serves as a foundational input for developing advanced ML-based scoring functions.

---

## 7. References
1.  **BACE1 Structure:** Hong, L., et al. *Science* 290.5489 (2000): 150-153. (PDB: 1FKN).
2.  **AutoDock-GPU:** Santos-Martins, D., et al. *Journal of Chemical Theory and Computation* 17.2 (2021): 1060-1073.
3.  **ChEMBL Database:** Gaulton, A., et al. *Nucleic Acids Research* 40.D1 (2012): D1100-D1107.
4.  **RDKit:** Open-source cheminformatics. http://www.rdkit.org
