Brandless Data Engineering Take Home Exercise

Setup:
1. Scheduler :Apache Airflow
2. Database : Postgres 10.0(dev)/ Amazon Redshift(prod)
3. Intermediate file/object storage : Local file system and S3
4. Languages used : Python, SQL


In this exercise we have setup an Airflow scheduler which queries Edemam Recipe Search API and pulls data for the Pasta recipes and also the health and diet labels associated with each recipes in our recipes table. We have scheduled daily incremental batch jobs which loads data into 3 tables
1. recipe_health_lables
2. recipe_diet_lables &
3. recipes

We have separate Python tasks to load into each of the three tables in the form of a DAG.
