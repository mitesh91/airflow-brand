import psycopg2
import logging
from datetime import datetime

now = datetime.now()
dt  = datetime.strftime(now,'%Y_%m_%d')

recipe_file        = 'files_{dt}.csv'.format(dt=dt)
recipe_diet_file   = 'dl_{dt}.csv'.format(dt=dt)
recipe_health_file = 'hl_{dt}.csv'.format(dt=dt)

conn = psycopg2.connect("host=brandless-redshift.ctnojem4tg5m.us-east-2.redshift.amazonaws.com dbname=dev user=airflow port=5439 password=Airflow123")
cur = conn.cursor()

create_and_copy_statement = """
CREATE TABLE IF NOT EXISTS airflow.recipes(
    uri VARCHAR(48) PRIMARY KEY,
    label VARCHAR(200),
    source VARCHAR(250),
    image VARCHAR(250),
    url VARCHAR(250),
    diet_labels VARCHAR(250),
    health_labels VARCHAR(250),
    no_of_ingridients INTEGER,
    calories DECIMAL(10,5),
    total_weight DECIMAL(10,5),
    total_time DECIMAL(10,5)
);

CREATE TABLE IF NOT EXISTS airflow.recipe_health_lables(
    uri VARCHAR(48),
    health_label VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS airflow.recipe_diet_lables(
    uri VARCHAR(48),
    diet_label VARCHAR(200)
);

COPY airflow.recipes
from 's3://airflow-brand/{}'
iam_role 'arn:aws:iam::866164669542:role/airflow_role'
DELIMITER ','
IGNOREHEADER 1
REMOVEQUOTES
region 'us-east-2';

copy  airflow.recipe_health_lables
from 's3://airflow-brand/{}'
DELIMITER ','
IGNOREHEADER 1
REMOVEQUOTES
region 'us-east-2'
iam_role 'arn:aws:iam::866164669542:role/airflow_role';

copy  airflow.recipe_diet_lables
from 's3://airflow-brand/{}'
DELIMITER ','
IGNOREHEADER 1
REMOVEQUOTES
region 'us-east-2'
iam_role 'arn:aws:iam::866164669542:role/airflow_role';

COMMIT;

""".format(recipe_file, recipe_health_file, recipe_diet_file, )

print("Redshift load successful!")
cur.execute(create_and_copy_statement)

conn.commit()
cur.close()
conn.close()
