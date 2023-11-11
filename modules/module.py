#imports
import requests #tenemos el json
import pandas as pd
import re #analiza el script para ver si esta bien
import json
import math#operacion matematica
import os
from dotenv import load_dotenv 
import argparse

#TOKEN:
load_dotenv('./.env')
TOKEN = os.environ.get("API_TOKEN")

#Endpoints: mayus parametros
API_TOKEN = TOKEN
USERNAME = 'SilviaAlconGarrido'
BASE_URL = 'https://api.github.com/'
KEY = 'repos/'#no tocar
OWNER = 'ih-datapt-mad/'#no tocar
REPO = 'dataptmad0923_labs/'#LAB_REPOSITORY -->el repo de los labs
SEARCH = 'search/issues?q=repo:'+OWNER+REPO+'+type:pr+state:{}'
PULLS = 'pulls?page={}&per_page=100&state={}'
COMMITS = 'pulls/{}/commits'
STATE = 'open'
#Aqui vemos si funciona bien y si nos trae el https bien
BASE_URL + KEY + OWNER + REPO + PULLS


#Function 1: saca 100 paginas 
def pages(base_url, search, state, username, api_token):
    pages = requests.get(base_url + search.format(state), auth=(username,api_token)).json()['total_count']
    if STATE == 'open':
        pages = math.ceil(pages/100)
        return pages
    elif STATE == 'closed':
        pages = math.ceil(pages/100)
        return pages
    
#Function 2:
def get_commits(base_url, key, owner, repo, commits, pull, username, api_token):
    r_commits = requests.get(base_url + key + owner + repo + commits.format(pull),
                             auth=(username, api_token)).json()
    df_commits = pd.json_normalize(r_commits)
    list_commits = list(df_commits['commit.message'])
    commit = list(set([commit if commit == 'lab-finished' else 'lab-started' for commit in list_commits]))
    if 'lab-finished' in commit:
        return 'lab-finished'
    else:
        return 'lab-started'
    
#Function 3:
def student_name(x):
    if ']' in x:
        x = x.split(']')
        x = x[1].replace('_', ' ').strip()
        len_x = len(x.split(' '))
        if len_x > 1:
            x = re.findall('\w[a-zA-Z áéíóúÁÉÍÓÚñÑ-]+', x)
            x = x[0].strip()
            return x
        else:
            x = 'No student name provided'
            return x
    else:
        x = 'Pull request is not properly named'
        return x
    
#Function 4:
def lab_name(x):
    if ']' in x:
        x = x.split(']')
        x = x[0] + ']'
        x = x.strip()
        lower_case = re.findall('[A-ZÁÉÍÓÚñÑ]+', x)
        if x[0] == '[' and x[-1] == ']' and ' ' not in x and len(lower_case) == 0:
            return x
        else:
            x = 'Lab format name is incorrect'
            return x
    else:
        x = 'Pull request is not properly named'
        return x
    
#Function 5:
def time_parser(x):
    try:
        x = x.strip()
        x = re.findall('[0-9]+', x)
        x = ''.join(x)
        x = pd.to_datetime(x, format='%Y%m%d%H%M%S', errors='coerce')
        return x
    except:
        return 'Nothing pushed yet'
    
#PIPELINE FUNCTIONS:
#Function 1:
def get_pulls(base_url, key, owner, repo, pulls, search, state, username, api_token, field_list):
    pulls_list = []
    max_pages = pages(base_url, search, state, username, api_token)
    for i in range(max_pages):
        r_pulls = requests.get(base_url + key + owner + repo + pulls.format(i+1, state),
                               auth=(username, api_token)).json()
        df_pulls = pd.json_normalize(r_pulls)
        pulls_list.append(df_pulls)
    df_pulls = pd.concat(pulls_list)
    df_pulls = df_pulls[field_list]
    return df_pulls

#Function 2:
def df_status(df_pulls, base_url, key, owner, repo, commits, username, api_token, field_list):
    df_pulls['student_name'] = df_pulls['title'].apply(student_name)
    df_pulls['lab_name'] = df_pulls['title'].apply(lab_name)
    print(df_pulls)
    df_pulls['created_at'] = df_pulls['created_at'].apply(time_parser)
    df_pulls['updated_at'] = df_pulls['updated_at'].apply(time_parser)
    df_pulls['head.repo.pushed_at'] = df_pulls['head.repo.pushed_at'].apply(time_parser)
    df_pulls['lab_status'] = df_pulls.apply(lambda col: get_commits(base_url,
                                                                    key,
                                                                    owner,
                                                                    repo,
                                                                    commits,
                                                                    col['number'],
                                                                    username,
                                                                    api_token), axis=1)
    df_status = df_pulls[field_list]
    return df_status

#Function 3:
def create_csv(df_status, field_sort, field_name):
    df_csv = df_status.sort_values(by=field_sort, ascending=False)
    df_csv.columns = field_name
    df_csv.to_csv('./data/labs_status.csv', index=False)
    return df_csv


#Funcion para: bonus argparse advanced-mysql'