import pandas as pd
import random
from tqdm import tqdm

from scenarios import generate_scenarios
from chatapi import ChatBot
from chatmodel import ChatModel

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model", default='gpt-3.5-turbo-0613', type=str)
parser.add_argument("--nb_scenarios", default =5, type=int)
parser.add_argument('--random_seed', default='123', type=int)
args = parser.parse_args()

if any(s in args.model for s in ["claude", "palm"]):
  chat_model = ChatBot(model=args.model)
elif any(s in args.model for s in ["llama", "vicuna", "gemma"]):
  chat_model = ChatModel(model=args.model)
  
else:
  raise ValueError("Unsupported model")

model_file_name = "results_for_{}_scenarios_{}_race.pickle".format(args.nb_scenarios, args.model)
random.seed(args.random_seed)
scenario_info_list = []
for i in tqdm(range(args.nb_scenarios)):
    #dimension = random.choice(["species", "social_value", "gender", "age", "fitness", "race"])
    dimension = "sexualism"
    is_interventionism = random.choice([True, False])
    is_in_car = random.choice([False, True])
    is_law = random.choice([True, False])

    system_content, user_content, scenario_info = generate_scenarios(dimension, is_in_car, is_interventionism, is_law)
    
    response = chat_model.chat(system_content, user_content)
    scenario_info['chat_response'] = response

    scenario_info_list.append(scenario_info)

    if (i + 1) % 100 == 0:
       df = pd.DataFrame(scenario_info_list)
       df.to_pickle(model_file_name)
    print("NEXT ROUND")


df = pd.DataFrame(scenario_info_list)
df.to_pickle(model_file_name)
