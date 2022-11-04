import yaml

with open("data.yml", encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.Loader)
    f.close()

with open("./domain.yml", encoding='utf-8') as dom:
    d = yaml.load(dom, Loader=yaml.Loader)
    d['intents'].append(data['intent_name'])
    d['responses'].update({'utter_' + data['intent_name']: [{'text': data['answer']}]})
    dom.close()
with open('./domain.yml', 'w', encoding='utf-8') as f:
    f.write(yaml.dump(d, sort_keys=False, allow_unicode=True))

with open("./data/nlu.yml", encoding='utf-8') as nlu:
    n = yaml.load(nlu, Loader=yaml.Loader)
    n['nlu'].append({'intent': data['intent_name'], 'examples': '\n'.join([str(i) for i in ['- {}'.format(num) for num in data['examples']]])})
    nlu.close()
with open('./data/nlu.yml', 'w', encoding='utf-8') as f:
    f.write(yaml.dump(n, sort_keys=False, allow_unicode=True))

with open("./data/rules.yml", encoding='utf-8') as rul:
    r = yaml.load(rul, Loader=yaml.Loader)
    r['rules'].append({'rule': data['intent_name'], 'steps': [{'intent': data['intent_name']}, {'action': 'utter_' + data['intent_name']}]})
    rul.close()
with open('./data/rules.yml', 'w', encoding='utf-8') as f:
    f.write(yaml.dump(r, sort_keys=False, allow_unicode=True))