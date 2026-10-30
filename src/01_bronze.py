# Databricks notebook source
# MAGIC %md
# MAGIC ## Bronze: leer CSV incluido con el Bundle

# COMMAND ----------
from pyspark.sql import functions as F

dbutils.widgets.text("catalog", "demo_dev")
dbutils.widgets.text("schema_prefix", "retail")
catalog = dbutils.widgets.get("catalog")
prefix = dbutils.widgets.get("schema_prefix")
# Parametros de catalogo/esquema solo alfanumericos y guiones bajos.
assert catalog.replace("_", "").isalnum() and prefix.replace("_", "").isalnum()
schema = f"{prefix}_bronze"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema}`")

# El Bundle sincroniza data/*.csv en la raiz de su carpeta del workspace.
import csv
dbutils.widgets.text("source_path", "")
source = dbutils.widgets.get("source_path")
assert source.startswith("/Workspace/") and source.endswith(".csv")
with open(source, newline="", encoding="utf-8") as handle:
    records = list(csv.DictReader(handle))
columns = ["venta_id", "fecha", "producto", "categoria", "cantidad", "precio_unitario"]
raw = spark.createDataFrame([tuple(r[c] for c in columns) for r in records], columns)
(raw.withColumn("fecha_ingesta", F.current_timestamp())
    .write.format("delta").mode("overwrite")
    .saveAsTable(f"`{catalog}`.`{schema}`.`ventas_raw`"))
print(f"Bronze: {raw.count()} filas cargadas")
