# Utilities
import logging

# Pull data from API
import requests # !pip install requests

# In case of warnings regarding the urllib3 and chardet versions, try !pip3 install --upgrade requests

## MAIN FUNCTIONS ##

def get_url(category:str):
    
    """  
    Collects urls from the D&D5E API.

    Args: a category of interest (str). 
    Accepted values are 'classes', 'races', 'subclasses', 'subraces', 'alignments' and 'ability-scores'
     
    Returns:   
    A list of dictionaries is generated, including : 
     - the items from this category,
     - their url   
     
    """
    api_url = 'https://www.dnd5eapi.co'
    
    out_dict = {}
    
    try:
        response = requests.get(api_url+'/api/'+category).json()

        for item in response['results']:
            item_name = item['name']
            item_url = item['url']
            
            out_dict.update({
                item_name : item_url
            })
            
    except KeyError:
        logging.exception('KeyError: invalid category provided ({})'.format(category))
            
    return out_dict


def get_elements(category:str):
    
    """  
    Collects lists of items from the D&D5E API.

    Args: a category of interest. Accepted values are 'classes', 'races', 'alignments' and 'ability-scores'
     
    Returns:  
    A single list is generated, including the item names from this category,    
    """
    api_url = 'https://www.dnd5eapi.co'
    
    out_list = []
    
    try:
        response = requests.get(api_url+'/api/'+category).json()

        for item in response['results']:
            item_name = item['name']

            
            out_list.append(item_name)
            
    except KeyError:
        logging.exception('KeyError: invalid category provided ({})'.format(category))
                    
    return out_list


def get_race_data(in_dict:dict):
    
    """
    Collects race data from the D&D5E API.

    Args: a category of interest (str). Default value is 'races'
     
    Returns: a nested dictionary summarizing, for each race, languages, proficiencies, traits...
    """
    api_url = 'https://www.dnd5eapi.co'
    
    out_dict = {}
        
    
    for race, race_url in in_dict.items():
        
        response = requests.get(api_url+race_url).json()
        
        # Get languages
        languages = []
    
        for lang in response['languages']:
            languages.append(lang['name'])
        
        # Get starting proficiencies
        starting_proficiencies = []
    
        for prof in response['starting_proficiencies']:
            starting_proficiencies.append(prof['name'])
            
        # Get racial traits
        racial_traits = []
        
        for trait in response['traits']:
            racial_traits.append(trait['name'])
            
        # Get speed
        speed = response['speed']
        
        # Get ability score bonuses
        ability_scores = {}
    
        for score in response['ability_bonuses']:
            ability_scores.update({score['ability_score']['name'] : score['bonus']})

        # Get subraces
        subraces = []

        for subrace in response['subraces']:
            subraces.append(subrace['name'])

        out_dict.update({
            race : {
                'languages' : languages,
                'racial_traits': racial_traits,
                'starting_proficiencies' : starting_proficiencies,
                'speed' : speed,
                'ability_bonus' : ability_scores,
                'subraces' : subraces
            }
        })
            
    return out_dict


def get_class_data(in_dict:dict):
    
    """
    Collects class data from the D&D5E API.

    Args: a category of interest (str). Default value is 'classes'     
     
     Returns: a nested dictionary summarizing, for each class, hit die, proficiencies...
    """

    api_url = 'https://www.dnd5eapi.co'
    
    out_dict = {}
    
    for classname, class_url in in_dict.items():
        
        response = requests.get(api_url+class_url).json()
            
        # Get hit die
        hit_die = response['hit_die']
        
        # Get saving throws
        saving_throws = []
        
        for saving_throw in response['saving_throws']:
            saving_throws.append(saving_throw['name'])
    
          
        # Get class proficiencies
        proficiencies = []
        
        for proficiency in response['proficiencies']:
            proficiencies.append(proficiency['name'])

        
        # Additional proficiency choices : skills
        skill_choice = []

        nb_skills = response['proficiency_choices'][0]['choose']
    
        for proficiency in response['proficiency_choices'][0]['from']['options']:
            skill_choice.append(proficiency['item']['name'].replace('Skill: ', ''))        
                
        # Get starting equipment
        starting_equipment = {}
    
        for equipment in response['starting_equipment']:
            starting_equipment.update({equipment['equipment']['name'] : equipment['quantity']})

        # Get subclasses
        subclasses = []

        for subclass in response['subclasses']:
            subclasses.append(subclass['name'])
                
        # Output dictionary
        out_dict.update({
            classname : {
                'hit_die': hit_die,
                'saving_throws' : saving_throws,
                'proficiencies' : proficiencies,
                'chose_skills': {
                    'chose': nb_skills,
                    'skills': skill_choice
                },
                'starting_equipment' : starting_equipment,
                'subclasses' : subclasses,
            }
        })             
        
    return out_dict


def get_subrace_data(in_dict:dict):
    
    """
    Collects subrace data from the D&D5E API.

    Args: a category of interest (str). 
     
    Returns: a nested dictionary summarizing, for each subrace, languages, proficiencies, traits...
    """
    api_url = 'https://www.dnd5eapi.co'
    
    out_dict = {}
        
    
    for subrace, subrace_url in in_dict.items():
        
        response = requests.get(api_url+subrace_url).json()

        # Get starting proficiencies
        starting_proficiencies = []
    
        for prof in response['starting_proficiencies']:
            starting_proficiencies.append(prof['name'])
            
        # Get racial traits
        racial_traits = []
        
        for trait in response['racial_traits']:
            racial_traits.append(trait['name'])
            
        
        # Get ability score bonuses
        ability_scores = {}
    
        for score in response['ability_bonuses']:
            ability_scores.update({score['ability_score']['name'] : score['bonus']})
        
        
        # Get race
        race = response['race']['name']


        out_dict.update({
            subrace : {
                'racial_traits': racial_traits,
                'starting_proficiencies' : starting_proficiencies,
                'ability_bonus' : ability_scores,
                'race' : race,
            }
        })
            
    return out_dict