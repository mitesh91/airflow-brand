import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from collections import defaultdict
import csv
import datetime
from datetime import timedelta, datetime
import re
import requests
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['miteshmangaonkar@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_recipes():

    now = datetime.now()
    dt  = datetime.strftime(now,'%Y_%m_%d')

    base_url = 'https://api.edamam.com/search'
    headers = {'app_key' : '4e3f2c74d5ba8fb262a25095b6bc6d3f',
               'app_id' : 'b02abb27',
               'q' :'pasta',
               'from': 0,
               'to': 200}

    r = requests.get(base_url, params=headers)

    # r = requests.get(base_url, params=headers, stream=True)
    print(r.url)
    response = r.json()

    items = response['hits']

    index = ['uri', 'label', 'source', 'image', 'url', 'diet_labels', 'health_labels', 'no_of_ingridients', 'calories',
            'total_weight', 'total_time']

    data = []
    for i in items:
        recipe              = i['recipe']
        label               = recipe['label'].encode("utf-8")
        uri                 = re.findall(r"recipe_([A-Za-z0-9]+)", recipe['uri'].encode("utf-8"))[0]
        image               = recipe['image'].encode("utf-8")
        url                 = recipe['url'].encode("utf-8")
        source              = recipe['source'].encode("utf-8")
        diet_labels         = recipe['dietLabels']
        health_labels       = recipe['healthLabels']
        no_of_ingridients   = len(recipe['ingredientLines'])
        calories            = recipe['calories']
        total_weight        = recipe['totalWeight']
        total_time          = recipe['totalTime']

        data.append([uri, label, source, image, url, diet_labels, health_labels, no_of_ingridients, calories, total_weight, total_time])

    dfs = pd.DataFrame(data, index=None, columns=index)

    dfs.to_csv('/Users/Assasin/Desktop/files_{dt}.csv'.format(dt=dt), index= False, sep=',',
               quotechar='"', encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
    
    return("Recipes loaded successfully")

with DAG('airflow_recipes',
         default_args=default_args,
         schedule_interval='0 12 * * *',
         ) as dag:

    load_recipes = PythonOperator(task_id='load_recipes',
                                 python_callable=load_recipes)
