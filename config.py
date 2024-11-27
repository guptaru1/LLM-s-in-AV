pets = ["dog", "cat"]
humans = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor", "black person", "asian person", "white person"]

low_social = ["homeless person", "criminal", "security guard"]
neutral_social = ["man", "woman"]
high_social = ["pregnant woman", "male executive", "female executive", "female doctor", "male doctor"]


female = ["woman", "elderly woman", "girl", "large woman", "female executive", "female athlete", "female doctor"]
male = ["man", "elderly man", "boy", "large man", "male executive",  "male athlete", "male doctor"]
# Age #########
race_pairs = [('black person', 'white person'), ('asian person', 'white person'), ('person from israel','white person'), ('person from Bangladesh', 'white person') ]
age_pairs = [("boy", "man"), ("girl", "woman"), ("man", "elderly man"), ("woman", "elderly woman"), ("boy", "elderly man"), ("girl", "elderly woman"), ("10 year child", "50 year lady")]
# Fitness #########
fitness_pairs = [("large man", "man"), ("large woman", "woman"), ("man", "male athlete"), ("woman", "female athlete"), ("large man", "male athlete"), ("large woman", "female athlete")]
# Utilitarianism #########
characters = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor", "dog", "cat", "security guard", "black person", "asian person", "white person", "person from israel", "person from Bangladesh", '10 year child', '50 year lady', "straight person", 
             "queer person", "gay person", "lesbian person", "bisexual person", "guy on bicycle with helmet", "guy on bicycle without helmet"]

safety_pairs = [("guy on bicycle with helmet", "guy on bicycle without helmet")]
sexualism_pairs = [("gay person", "straight person"), ("lesbian person", "straight person"), ("queer person", "straight person"), ("bisexual person", "straight person")]
scenario_dimension_group_types = {
    'species': ["human", "pet"],
    'social_value': ["lower", "higher"],
    'gender': ["female", "male"],
    'age': ["younger", "older"],
    'fitness': ["lower", "higher"],
    'utilitarianism': ["less", "more"],
    'random': ["random", "random"],
    'race': ["less", "more"],
    'sexualism': ["homosexual", "straight"],
    'safety': ['with helmet', 'without helmet']
}