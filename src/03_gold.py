# Databricks notebook source
# MAGIC %md
# MAGIC ## Gold: indicador de ventas por categoria

# COMMAND ----------
from pyspark.sql import functions as F

dbutils.widgets.text("catalog", "demo_dev")
dbutils.widgets.text("schema_prefix", "retail")
catalog = dbutils.widgets.get("catalog")
prefix = dbutils.widgets.get("schema_prefix")
assert catalog.replace("_", "").isalnum() and prefix.replace("_", "").isalnum()
spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{prefix}_gold`")
source = spark.table(f"`{catalog}`.`{prefix}_silver`.`ventas`")
kpi = (source.groupBy("categoria").agg(
    F.count("venta_id").alias("transacciones"),
    F.sum("cantidad").alias("unidades"),
    F.round(F.sum("importe"), 2).alias("ventas_totales")))
kpi.write.format("delta").mode("overwrite").saveAsTable(f"`{catalog}`.`{prefix}_gold`.`ventas_categoria`")
display(kpi.orderBy(F.desc("ventas_totales")))
