from http.client import HTTPException
from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import yaml
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class QuestionModel(BaseModel):
    name: str
    examples: list
    answer: str

class AllQuestionModel(BaseModel):
    intents: List[QuestionModel]

with open("data.json", encoding='utf-8') as f:
    data = json.load(f)
    f.close()

@app.post("/add_intent")
def add_intent(intent: QuestionModel):
    if len(intent.name) == 0:
        raise HTTPException(status_code=404, detail="Поле названия блока вопросов не может быть пустым")
    if len(intent.examples) == 0:
        raise HTTPException(status_code=404, detail="Поле возможных вопросов от пользователя не может быть пустым")
    if len(intent.answer) == 0:
        raise HTTPException(status_code=404, detail="Поле ответа на вопросы не может быть пустым")
 
    with open("../domain.yml", encoding='utf-8') as dom:
        d = yaml.load(dom, Loader=yaml.Loader)
        d['intents'].append(intent.name)
        d['responses'].update({'utter_' + intent.name: [{'text': intent.answer}]})
        dom.close()
    with open('../domain.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(d, sort_keys=False, allow_unicode=True))

    with open("../data/nlu.yml", encoding='utf-8') as nlu:
        n = yaml.load(nlu, Loader=yaml.Loader)
        n['nlu'].append({'intent': intent.name, 'examples': '\n'.join([str(i) for i in ['- {}'.format(num) for num in intent.examples]])})
        nlu.close()
    with open('../data/nlu.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(n, sort_keys=False, allow_unicode=True))

    with open("../data/rules.yml", encoding='utf-8') as rul:
        r = yaml.load(rul, Loader=yaml.Loader)
        r['rules'].append({'rule': intent.name, 'steps': [{'intent': intent.name}, {'action': 'utter_' + intent.name}]})
        rul.close()
    with open('../data/rules.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(r, sort_keys=False, allow_unicode=True))


@app.delete("/delite_intent")
def delite_intent(name):
    with open("../domain.yml", encoding='utf-8') as dom:
        d = yaml.load(dom, Loader=yaml.Loader)
        if name not in d['intents']:
            raise HTTPException(status_code=404, detail="Не существует объекта с таким названием блока вопросов")
        d['intents'].remove(name)
        del d['responses']['utter_' + name]
        dom.close()
    with open('../domain.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(d, sort_keys=False, allow_unicode=True))

    with open("../data/nlu.yml", encoding='utf-8') as nlu:
        n = yaml.load(nlu, Loader=yaml.Loader)
        for i in n['nlu']:
            if i['intent'] == name: 
                ig = n['nlu'].index(i)
        del n['nlu'][ig]
        nlu.close()
    with open('../data/nlu.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(n, sort_keys=False, allow_unicode=True))

    with open("../data/rules.yml", encoding='utf-8') as rul:
        r = yaml.load(rul, Loader=yaml.Loader)
        for i in r['rules']:
            if i['rule'] == name: 
                ig = r['rules'].index(i)
        del r['rules'][ig]  
        rul.close()
    with open('../data/rules.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(r, sort_keys=False, allow_unicode=True))

@app.get("/get_intent/")  
async def get_intent():
    with open("../domain.yml", encoding='utf-8') as dom:
        d = yaml.load(dom, Loader=yaml.Loader)
        dom.close()
    with open("../data/nlu.yml", encoding='utf-8') as nlu:
        n = yaml.load(nlu, Loader=yaml.Loader)
        nlu.close()
    js = {'intent_objects':[]}
    for i in range(len(d['intents'])):
        js_part = {'name': n['nlu'][i]['intent'], 'examples': n['nlu'][i]['examples'].split('\n'), 'answer': d['responses']['utter_' + n['nlu'][i]['intent']][0]['text']}
        js['intent_objects'].append(js_part)
    return JSONResponse(content=jsonable_encoder(js))
    
@app.put("/update_intent/")
def update_intent(intent: QuestionModel):
    with open("../domain.yml", encoding='utf-8') as dom:
        d = yaml.load(dom, Loader=yaml.Loader)
        dom.close()
    if intent.name not in d['intents']:
        raise HTTPException(status_code=404, detail="Среди имеющихся блоков вопросов нет блока с таким названием. Возможно, вы хотите создать новый блок?")
    if len(intent.examples) == 0:
        raise HTTPException(status_code=404, detail="Поле возможных вопросов от пользователя не может быть пустым")
    if len(intent.answer) == 0:
        raise HTTPException(status_code=404, detail="Поле ответа на вопросы не может быть пустым")
    delite_intent(intent.name)
    add_intent(intent)
    

# @app.get("/train")
# async def get_intent():
    