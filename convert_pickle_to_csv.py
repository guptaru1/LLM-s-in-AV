import pandas as pd
import re

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--model', default='gpt-3.5-turbo-0613', type=str)
parser.add_argument('--nb_scenarios', default='10', type=int)
parser.add_argument('--scenario', default='race', type=str)
args = parser.parse_args()

df = pd.read_pickle("results_for_{}_scenarios_{}_{}.pickle".format(args.nb_scenarios, args.model, args.scenario))

keywords = ["case 1", "case 2"]

def response_classification(query):
  text = query.lower()
  print(text)
  pattern_case1 = re.compile(r"case\s?1")
  pattern_case2 = re.compile(r"case\s?2")

  match_case1 = pattern_case1.search(text) is not None
  match_case2 = pattern_case2.search(text) is not None

  if match_case1 and not match_case2:
      label = 0 #CASE 1
  elif not match_case1 and match_case2:
      label = 1 # CASE 2
  else:
      label = -1 #NO CASE CHOSEN

  return label

# assign the response labels
if 'chat_response' in df.columns:
  df['label'] = df['chat_response'].apply(response_classification)
else:
  if "gpt" in args.model:
    df['label'] = df['chatgpt_response'].apply(response_classification)
  elif "palm" in args.model:
    df['label'] = df['palm2_response'].apply(response_classification)
  elif "llama" in args.model:
    df['label'] = df['llama2_response'].apply(response_classification)
  elif "vicuna" in args.model:
    df['label'] = df['vicuna_response'].apply(response_classification)
  elif "gemini" in args.model:
    df['label'] = df['gemini_response'].apply(response_classification)
  elif "claude" in args.model:
    df['label'] = df['claude_response'].apply(response_classification)

df = df[df["label"] >=0].reset_index(drop=True)
print(df)


# conver the data into data format for conjoint analysis
CrossingSignal_dict = {
  "NA": 0,
  "green": 1,
  "red": 2, 
}

ScenarioType_dict = {
  "species": "Species",
  "social_value": "Social Value",
  "gender": "Gender",
  "age": "Age",
  "fitness": "Fitness",
  "utilitarianism": "Utilitarian",
  "random": "Random",
  "race": "Race",
  "sexualism": "Sexualism"
}

AttributeLevel_dict = {
  "species": {
    "human": "Humans",
    "pet": "Pets",
  },
  "social_value": {
    "lower": "Low",
    "higher": "High",
  },
  "gender": {
    "female": "Female",
    "male": "Male",
  },
  "age": {
    "younger": "Young",
    "older": "Old",
  },
  "fitness": {
    "lower": "Fat",
    "higher": "Fit",
  },
  "utilitarianism": {
    "less": "Less",
    "more": "More",
  },
  "random": {
    "random": "Random",
  },
  "race":{
    "less": "Black/Indian Race",
    "more" : "America/European Race"
  },
  "sexualism" : {
    "homosexual": "Gay/Lesbian",
    "straight": "straight",
  }
}

characters = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor", "dog", "cat", "security guard", "black person", "asian person", "white person", "person from israel", "person from Bangladesh", '10 year child', '50 year lady', "straight person", 
             "queer person", "gay person", "lesbian person", "bisexual person"]

characters_dict = {
  "man": "Man",
  "woman": "Woman",
  "pregnant woman": "Pregnant",
  "baby": "Stroller",
  "elderly man": "OldMan",
  "elderly woman": "OldWoman",
  "boy": "Boy",
  "girl": "Girl",
  "homeless person": "Homeless",
  "large woman": "LargeWoman",
  "large man": "LargeMan",
  "criminal": "Criminal",
  "male executive": "MaleExecutive",
  "female executive": "FemaleExecutive",
  "female athlete": "FemaleAthlete",
  "male athlete": "MaleAthlete",
  "female doctor": "FemaleDoctor",
  "male doctor": "MaleDoctor",
  "dog": "Dog",
  "cat": "Cat",
  "security guard": "Guard",
  "black person": "Black person", 
  "asian person" : "Asian person",
   "white person" : "White person",
    "person from israel" : "Israel Person", 
    "person from Bangladesh" : "Bangladesh person", 
    '10 year child': "10 year old child",
    '50 year lady' : "50 year old lady", 
    "straight person" : "straight person", 
    "queer person" : "queer person",
    "gay person" : "gay person",
   "lesbian person" : "lesbian person", 
   "bisexual person" : "bisexual person"
}

sharedresponse_list = []
for index, row in df.iterrows():
  # group 1
  sharedresponse = {}
  sharedresponse['ResponseID'] = "res_{:08}_CASE1".format(index)
  sharedresponse["Response"] = "Case 1" if not row['label'] else "Case 2"
  sharedresponse['Intervention'] = int(row['is_interventionism'])
  sharedresponse['PedPed'] = int(not row['is_in_car'])
  if sharedresponse['PedPed'] == 1:
    sharedresponse['Barrier'] = 0
    sharedresponse['CrossingSignal'] = CrossingSignal_dict[row["traffic_light_pattern"][0]]
  else:
    sharedresponse['Barrier'] = 1
    sharedresponse['CrossingSignal'] = 0
  sharedresponse['Saved'] = int(row['label'] != 0)
  sharedresponse['NumberOfCharacters'] = sum(row["count_dict_1"].values())
  sharedresponse['DiffNumberOFCharacters'] = abs(sum(row["count_dict_1"].values()) - sum(row["count_dict_2"].values()))
  sharedresponse['ScenarioType'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['AttributeLevel'] = AttributeLevel_dict[row["scenario_dimension"]][row["scenario_dimension_group_type"][0]]
  count = {characters_dict[key]: row["count_dict_1"].get(key, 0) for key in characters}
  sharedresponse.update(count)

  sharedresponse_list.append(sharedresponse)

  # group 2
  sharedresponse = {}
  sharedresponse['ResponseID'] = "res_{:08}_CASE2".format(index)
  #sharedresponse['ExtendedSessionID'] = "chatbot_extended"
  #sharedresponse['UserID'] = "chatbot"
  #sharedresponse['ScenarioOrder'] = 0
  sharedresponse["Response"] = "Case 2" if row['label'] else "Case 1"
  sharedresponse['Intervention'] = int(not row['is_interventionism'])
  sharedresponse['PedPed'] = int(not row['is_in_car'])
  sharedresponse['Barrier'] = 0
  sharedresponse['CrossingSignal'] = CrossingSignal_dict[row["traffic_light_pattern"][1]]
  sharedresponse['Saved'] = int(row['label'] != 1)
  sharedresponse['NumberOfCharacters'] = sum(row["count_dict_2"].values())
  sharedresponse['DiffNumberOFCharacters'] = abs(sum(row["count_dict_1"].values()) - sum(row["count_dict_2"].values()))
  sharedresponse['ScenarioType'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['AttributeLevel'] = AttributeLevel_dict[row["scenario_dimension"]][row["scenario_dimension_group_type"][1]]
  count = {characters_dict[key]: row["count_dict_2"].get(key, 0) for key in characters}
  sharedresponse.update(count)

  sharedresponse_list.append(sharedresponse)


new_index_order = ["ResponseID",  "Intervention", "PedPed", "Barrier", "CrossingSignal", "AttributeLevel", "ScenarioType", "Response", "NumberOfCharacters", "DiffNumberOFCharacters", "Saved", "Man", "Woman", "Pregnant", "Stroller", "OldMan", "OldWoman", "Boy", "Girl", "Homeless", "LargeWoman", "LargeMan", "Criminal", "MaleExecutive", "FemaleExecutive", "FemaleAthlete", "MaleAthlete", "FemaleDoctor", "MaleDoctor", "Dog", "Cat","Guard", "Black person", "Asian person", "White person", "Israel Person", "Bangladesh person", "10 year old child", "50 year old lady", "straight person", "queer person", "gay person", "lesbian person", "bisexual person" ]

df = pd.DataFrame(sharedresponse_list)
df = df[new_index_order]

df.to_csv("shared_responses_{}_{}.csv".format(args.model, args.nb_scenarios), index=False)

