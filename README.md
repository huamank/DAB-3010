# Webinar: Declarative Automation Bundles

Demo de ingesta CSV -> Bronze -> Silver -> Gold con Lakeflow Jobs y GitHub Actions.

## Preparacion
1. Instala Databricks CLI y Git. Inicia sesion: `databricks auth login --host https://TU-WORKSPACE.azuredatabricks.net` o `databricks configure --profile mi-perfil`
.
`curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh`
2. Configura el perfil o la variable `DATABRICKS_HOST` para que el CLI encuentre el workspace.
3. En Unity Catalog crea los catalogos `demo_dev` y `demo_prod`, o cambia sus nombres en `databricks.yml`. La identidad ejecutora necesita USE CATALOG, CREATE SCHEMA y permisos para crear tablas en los esquemas.
4. Verifica que el workspace admita notebooks en serverless Jobs.
5. `databricks bundle validate -t dev`
6. `databricks bundle deploy -t dev`
7. `databricks bundle run -t dev retail_etl`
8. Consulta `demo_dev.retail_gold.ventas_categoria` desde Catalog Explorer.

## GitHub Actions
- Crea GitHub Environments llamados `dev` y `prod`.
- En cada environment configura variables `DATABRICKS_HOST` y `DATABRICKS_TOKEN_DEV`.
- Opcional: activa required reviewers en GitHub Environment `prod`.

**Nota:** `bundle deploy` no ejecuta el Job. Ejecutalo desde CLI, Databricks Jobs UI, o agrega `databricks bundle run -t dev retail_etl` en CD si deseas ejecucion automatica.

## Documentacion
- https://docs.databricks.com/aws/en/dev-tools/bundles/
- https://docs.databricks.com/aws/en/dev-tools/bundles/examples
- https://docs.databricks.com/aws/en/dev-tools/auth/provider-github
