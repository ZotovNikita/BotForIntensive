from http.client import HTTPException
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import yaml
import json

with open("data.json", encoding='utf-8') as f:
    data = json.load(f)
    f.close()
name = "greet" 

# with open("../domain.yml", encoding='utf-8') as dom:
#     d = yaml.load(dom, Loader=yaml.Loader)
#     dom.close()
# with open("../data/nlu.yml", encoding='utf-8') as nlu:
#     n = yaml.load(nlu, Loader=yaml.Loader)
#     nlu.close()
# with open("../data/rules.yml", encoding='utf-8') as rul:
#     r = yaml.load(rul, Loader=yaml.Loader) 
#     rul.close()

# # js = {'intents': [{'name': i['intent'] for i in n['nlu']}, {'name': '', 'examples': i['examples'].split('\n') for i in n['nlu']}]}
# res = {'intents': {'name': [], 'examples': [], 'answer': ''}}
# for i in n['nlu']:
#     res['intents']['name'].append(i['intent'])
#     res['intents']['examples'].append(i['examples'].split('\n'))
# with open('result.json', 'w', encoding='utf-8') as f:
#     json.dump(res, f, sort_keys=False,
#                     indent=4,
#                     ensure_ascii=False,
#                     separators=(',', ': '))
# name = 'sdasf'
# if name not in d['intents']:
#     print('rfr')

