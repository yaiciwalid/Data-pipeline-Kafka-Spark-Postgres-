from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Define the schema for the JSON data
SCHEMA = StructType([
    StructField("reference_fiche", StringType(), True),
    StructField("ndeg_de_version", IntegerType(), True),
    StructField("nature_juridique_du_rappel", StringType(), True),
    StructField("categorie_de_produit", StringType(), True),
    StructField("sous_categorie_de_produit", StringType(), True),
    StructField("nom_de_la_marque_du_produit", StringType(), True),
    StructField("noms_des_modeles_ou_references", StringType(), True),
    StructField("identification_des_produits", StringType(), True),
    StructField("conditionnements", StringType(), True),
    StructField("date_debut_fin_de_commercialisation", StringType(), True),
    StructField("temperature_de_conservation", StringType(), True),
    StructField("marque_de_salubrite", StringType(), True),
    StructField("informations_complementaires", StringType(), True),
    StructField("zone_geographique_de_vente", StringType(), True),
    StructField("distributeurs", StringType(), True),
    StructField("motif_du_rappel", StringType(), True),
    StructField("risques_encourus_par_le_consommateur", StringType(), True),
    StructField("preconisations_sanitaires", StringType(), True),
    StructField("description_complementaire_du_risque", StringType(), True),
    StructField("conduites_a_tenir_par_le_consommateur", StringType(), True),
    StructField("numero_de_contact", StringType(), True),
    StructField("modalites_de_compensation", StringType(), True),
    StructField("date_de_fin_de_la_procedure_de_rappel", StringType(), True),
    StructField("informations_complementaires_publiques", StringType(), True),
    StructField("liens_vers_les_images", StringType(), True),
    StructField("lien_vers_la_liste_des_produits", StringType(), True),
    StructField("lien_vers_la_liste_des_distributeurs", StringType(), True),
    StructField("lien_vers_affichette_pdf", StringType(), True),
    StructField("lien_vers_la_fiche_rappel", StringType(), True),
    StructField("rappelguid", StringType(), True),
    StructField("date_de_publication", TimestampType(), True),
    StructField("libelle", StringType(), True),
    StructField("id", IntegerType(), True)
])

JDBC_URL = "jdbc:postgresql://postgres:5432/mydatabase"
JDBC_PROPERTIES = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}
KAFKA_BOOTSTRAP_SERVER = "kafka:9092"
KAFKA_TOPIC = "rappel_conso"