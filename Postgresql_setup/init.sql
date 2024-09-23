CREATE TABLE IF NOT EXISTS rappel_conso (
    reference_fiche VARCHAR(255) PRIMARY KEY,
    nature_juridique_du_rappel TEXT,
    categorie_de_produit TEXT,
    sous_categorie_de_produit TEXT,
    nom_de_la_marque_du_produit TEXT,
    date_debut_de_commercialisation DATE,
    date_fin_de_commercialisation DATE,
    zone_geographique_de_vente TEXT,
    risques_encourus_par_le_consommateur TEXT,
    preconisations_sanitaires TEXT,
    conduites_a_tenir_par_le_consommateur TEXT,
    modalites_de_compensation TEXT,
    date_de_fin_de_la_procedure_de_rappel DATE,
    date_de_publication DATE,
    libelle TEXT
);