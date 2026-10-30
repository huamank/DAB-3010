# Databricks notebook source
# MAGIC %md
# MAGIC ## Silver: calidad, tipificacion y deduplicacion

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window

dbutils.widgets.text("catalog", "demo_dev")
dbutils.widgets.text("schema_prefix", "retail")
catalog = dbutils.widgets.get("catalog")
prefix = dbutils.widgets.get("schema_prefix")
assert catalog.replace("_", "").isalnum() and prefix.replace("_", "").isalnum()
spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{prefix}_silver`")
raw = spark.table(f"`{catalog}`.`{prefix}_bronze`.`ventas_raw`")
clean = (raw.select(
    F.col("venta_id"), F.to_date("fecha").alias("fecha"),
    F.trim("producto").alias("producto"), F.trim("categoria").alias("categoria"),
    F.col("cantidad").cast("int").alias("cantidad"),
    F.col("precio_unitario").cast("decimal(12,2)").alias("precio_unitario"),
    "fecha_ingesta")
    .filter("venta_id IS NOT NULL AND fecha IS NOT NULL AND cantidad > 0 AND precio_unitario >= 0"))
w = Window.partitionBy("venta_id").orderBy(F.col("fecha_ingesta").desc())
clean = (clean.withColumn("rn", F.row_number().over(w)).filter("rn=1")
         .drop("rn").withColumn("importe", F.col("cantidad")*F.col("precio_unitario")))
clean.write.format("delta").mode("overwrite").saveAsTable(f"`{catalog}`.`{prefix}_silver`.`ventas`")
print(f"Silver: {clean.count()} ventas validas")
