from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, regexp_extract, to_date, when
from const import (
    SCHEMA,
    JDBC_URL,
    JDBC_PROPERTIES,
    KAFKA_TOPIC,
    KAFKA_BOOTSTRAP_SERVER,
)

# Initialize SparkSession
spark= SparkSession.builder \
    .appName("Kafka-Spark-Streaming-Dictionnaire") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,"
            "org.postgresql:postgresql:42.2.18") \
    .master("spark://spark-master:7077")\
    .getOrCreate()
df_references = spark.read \
    .jdbc(JDBC_URL, "rappel_conso", properties=JDBC_PROPERTIES) \
    .select("reference_fiche")


def write_to_postgres(batch_df, batch_id):
    
    global df_references
    # Écrire dans la table PostgreSQL
    batch_df.write \
        .mode("append") \
        .jdbc(JDBC_URL, "rappel_conso", properties=JDBC_PROPERTIES)
    
    df_references = spark.read \
        .jdbc(JDBC_URL, "rappel_conso", properties=JDBC_PROPERTIES) \
        .select("reference_fiche")
    


if __name__=='__main__':

    df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

    # Parse the JSON data with the schema
    df_parsed = df.selectExpr("CAST(value AS STRING) as json_data") \
        .select(from_json("json_data", SCHEMA).alias("data")) \
        .select("data.*")

    date_pattern = r"(\d{2}/\d{2}/\d{4})"

    df_with_dates = df_parsed \
        .withColumn(
            "date_debut_de_commercialisation",
            when(
                col("date_debut_fin_de_commercialisation").isNotNull(),
                regexp_extract(col("date_debut_fin_de_commercialisation"), date_pattern, 0)
            ).otherwise(None)
        ) \
        .withColumn(
            "date_fin_de_commercialisation",
            when(
                col("date_debut_fin_de_commercialisation").isNotNull(),
                regexp_extract(col("date_debut_fin_de_commercialisation"), date_pattern, 1)
            ).otherwise(None)
        ) \
        .withColumn(
            "date_debut_de_commercialisation",
            when(
                col("date_debut_de_commercialisation").isNotNull(),
                to_date(col("date_debut_de_commercialisation"), "dd/MM/yyyy")
            ).otherwise(None)
        ) \
        .withColumn(
            "date_fin_de_commercialisation",
            when(
                col("date_fin_de_commercialisation").isNotNull(),
                to_date(col("date_fin_de_commercialisation"), "dd/MM/yyyy")
            ).otherwise(None)
        ).withColumn(
            "date_de_fin_de_la_procedure_de_rappel",
            when(
                col("date_de_fin_de_la_procedure_de_rappel").isNotNull(),
                to_date(col("date_de_fin_de_la_procedure_de_rappel"), "dd/MM/yyyy")
            ).otherwise(None)
        )


    df_filtered = df_with_dates.select(
        "reference_fiche",
        "nature_juridique_du_rappel",
        "categorie_de_produit",
        "sous_categorie_de_produit",
        "nom_de_la_marque_du_produit",
        "date_debut_de_commercialisation",
        "date_fin_de_commercialisation",
        "zone_geographique_de_vente",
        "risques_encourus_par_le_consommateur",
        "preconisations_sanitaires",
        "conduites_a_tenir_par_le_consommateur",
        "modalites_de_compensation",
        "date_de_fin_de_la_procedure_de_rappel",
        "date_de_publication",
        "libelle"
    )

    df_filtered = df_filtered.dropDuplicates(["reference_fiche"])

    df_filtered = df_filtered.join(df_references, on="reference_fiche", how="left_anti")

    query = df_filtered.writeStream \
        .outputMode("append") \
        .foreachBatch(write_to_postgres) \
        .start()

    query.awaitTermination()