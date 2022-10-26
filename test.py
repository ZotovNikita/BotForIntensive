from rasa import train

train("domain.yml", "config.yml", "data/nlu.yml", fixed_model_name="my_model")