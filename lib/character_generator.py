import json
import random
from collections import Counter
from PIL import Image

# Load dataset 

def load_dataset():
    with open('./data/dataset.json','r') as json_file:
        dataset = json.load(json_file)
        return dataset

# Create a new class for the player character

class PlayerCharacter:

  #class default constructor
    def __init__(self, dataset):
        
        # Core character
        self.gender = random.choice(['Female', 'Male'])
        self.alignment = random.choice(dataset['alignments'])
        self.race = random.choice(list(dataset['races'].keys()))
        self.classname = random.choice(list(dataset['classes'].keys()))
                
        # Core features
        self.base_hit_die = dataset['classes'][self.classname]['hit_die']
        self.speed = dataset['races'][self.race]['speed']
        self.saving_throws = dataset['classes'][self.classname]['saving_throws']

        # Racial attributes
        self.traits = dataset['races'][self.race]['racial_traits']
        self.languages = dataset['races'][self.race]['languages']
        
        # Inventory
        self.equipment = dataset['classes'][self.classname]['starting_equipment']
 

        
    def __str__(self):

        return "{} {} ({}) - {} - {}".format(
                                        self.subrace,
                                        self.classname,
                                        self.subclass,
                                        self.alignment,
                                        self.gender,
                                    )


    # Method to roll character subrace 
    def roll_subrace(self, dataset):
    
        for race in dataset['races'].keys():
            if race == self.race:
                try:
                    self.subrace = random.choice(dataset['races'][race]['subraces'])
                
                except IndexError:
                    self.subrace = self.race
                    
                    
    # Method to roll character subclass               
    def roll_subclass(self, dataset):
    
        for classname in dataset['classes'].keys():
            if classname == self.classname:
            
                try:
                    self.subclass = random.choice(dataset['classes'][classname]['subclasses'])
                
                except IndexError:
                    self.subclass = self.classname

    # Method to roll character skills               
    def roll_skills(self, dataset):
    
        for classname in dataset['classes'].keys():
            if classname == self.classname:
            
                self.skills = random.sample(dataset['classes'][classname]['chose_skills']['skills'], dataset['classes'][classname]['chose_skills']['chose'])
                
                # Two races have skills as starting proficiencies
                if self.race in ['Half-Orc' ,'Elf']: 

                    # Append these skills to the list generated above and keep only unique values  
                    self.skills = list(set(self.skills + [skill.replace('Skill: ', '') for skill in dataset['races'][self.race]['starting_proficiencies']])) 
                    
                    
    # Method to determine character proficiencies               
    def roll_proficiencies(self, dataset):
    
        for classname in dataset['classes'].keys():
            if classname == self.classname:
                
                # Fetch class-related proficiencies without accounting for saving throws (which were added to proficiencies for some reason)
                self.proficiencies = [proficiency for proficiency in dataset['classes'][classname]['proficiencies'] if 'Saving Throw' not in proficiency]
                
                # Two races have skills as starting proficiencies
                if self.race not in ['Half-Orc' ,'Elf'] and self.race != self.subrace:  

                    # Append race and subrace starting proficiencies and keep only unique values 
                    self.proficiencies = list(set(self.proficiencies + dataset['races'][self.race]['starting_proficiencies'] + dataset['subraces'][self.subrace]['starting_proficiencies']))


    # Method to roll ability scores and determine modifiers
    def roll_ability_scores(self, dataset, method):   
    
        # If the standard method is used
        if method == 'standard':
    
            standard_array = [15, 14, 13, 12, 10, 8]
            raw_roll = dict(zip(dataset['ability_scores'], random.sample(standard_array,6)))
      
        # If the roll method is used
        elif method == 'roll':
        
            rolled_array = []
            for ability in dataset['ability_scores']:
                rolled_array.append(sum(sorted(random.randint(1, 6) for i in range(4))[1:]))
        
            raw_roll = dict(zip(dataset['ability_scores'], rolled_array))
        
        # Add racial ability bonuses
        if self.subrace != self.race:

            self.ability_scores = dict(Counter(raw_roll) + Counter(dataset['races'][self.race]['ability_bonus']) + Counter(dataset['subraces'][self.subrace]['ability_bonus']))
            
        else:
            self.ability_scores = dict(Counter(raw_roll) + Counter(dataset['races'][self.race]['ability_bonus']))

        # Calculate modifiers
        self.ability_modifiers = {score:((value-10) // 2) for score,value in self.ability_scores.items()}

    # Method to pick an avatar
    def set_avatar(self):

        # Define a group for each class (this trick allows us to use the same avatar for several classes)
        class_group = {
            'Fighter': 'Warrior',
            'Ranger': 'Warrior',
            'Paladin': 'Warrior',
            'Barbarian': 'Warrior',
            'Cleric': 'Priest',
            'Druid': 'Priest',
            'Monk': 'Priest',
            'Wizard': 'Wizard',
            'Warlock': 'Wizard',
            'Sorcerer': 'Wizard',
            'Rogue': 'Rogue',
            'Bard': 'Rogue'
            }

        # Select an avatar based on group, race and gender
        self.avatar = Image.open(
            "assets/{}/{}_{}_single.png".format(class_group[self.classname], self.race, self.gender[:1])
            ).resize((400, 400))

    # Method to set hit points 
    def set_hit_points(self): 
        self.hit_point = self.base_hit_die + self.ability_modifiers['CON']

    ## Method to set base AC
    def set_armor_class(self):
        self.armor_class = 10 + self.ability_modifiers['DEX']

    # Method to roll a deity
    def roll_deity(self, dataset):   
    
        race_panth = {
            'Dragonborn' : 'Human deities',
            'Dwarf' : 'Morndinsamman',
            'Gnome' : 'Lords of the Golden Hills',
            'Halfling' : "Yondalla's Children",
            'Half-Elf' : 'Seldarine', 
            'Half-Orc' : 'Orcish pantheon',
            'Human' : 'Human deities', 
            'Elf' : 'Seldarine', 
            'Drow' : 'Dark Seldarine',
            'Tiefling' : 'Human deities'
        }
    
        # Match each character race or subrace (eg. Drow) to a pantheon
        for race, pantheon in race_panth.items():
            if race == self.race or race == self.subrace:  

                # Handles the specific case of clerics, for which domain (subclass) must match their deity's.
                if self.classname == 'Cleric':

                    match_domain = []

                    for deity, deity_att in dataset['deities'][pantheon].items():
                        if self.subclass in deity_att['deity_domains']:
                            match_domain.append(deity)

                    try:
                        self.deity = random.choice(match_domain)
                
                    except IndexError: # In case no deity from the pantheon matches the domain, select any deity from the pantheon
                        self.deity = random.choice(list(dataset['deities'][pantheon]))

                # Add human deities as options for mixed races
                elif self.race == 'Half-Elf' or self.race == 'Half-Orc':
                    self.deity = random.choice(list(dataset['deities'][pantheon]) + list(dataset['deities']['Human deities']))

                else:
                    self.deity = random.choice(list(dataset['deities'][pantheon]))

    # Method to generate a dictionary of attributes after converting them to human readable strings
    def clean_attributes(self):

        # Ability scores and modifiers
        ## Add modifiers
        ability_dict = {score: str(self.ability_scores[score]) + ' (' + str(self.ability_modifiers.get(score, '')) + ')' for score in self.ability_scores.keys()}

        ## Convert the dictionary to a readable comma-separated list of scores
        ability_list = [ability + '\t' + score for ability, score in ability_dict.items()]

        ### Convert the list to a string
        ability_scores = ', '.join(ability_list).replace(', ', '\n')

        # Lists of skills, proficiencies, etc.
        skills = ', '.join(self.skills)
        proficiencies = ', '.join(self.proficiencies)
        saving_throws = ', '.join(self.saving_throws)
        traits = ', '.join(self.traits)
        languages = ', '.join(self.languages)
    
    
        # Items in the inventory 
        ## Set item names to plural when the character carries more than 1
        item_dict = {k + 's' if v > 1 else k:v for k,v in self.equipment.items()}
    
        ## Convert the dictionary to a readable comma-separated list of items
        item_list = [str(number) + ' ' + item for item, number in item_dict.items()]

        ## Convert the list to a string
        inventory = ', '.join(item_list)

        # Write output

        self.attribute_dict = {
            "Ability scores" : ability_scores,
            "Hit die" : str(self.hit_point),
            "Armor Class": str(self.armor_class),
            "Speed" : str(self.speed),
            "Skills" : skills,
            "Proficiencies" : proficiencies,
            "Saving throws": saving_throws,
            "Traits" : traits,
            "Languages": languages,
            "Deity":str(self.deity),
            "Base inventory": inventory
        }



# Generate the character

def generate_character(method):
    """
    This function generates a random D&D 5E player character according to the Player's Handbook.

    Args: a method the use to roll ability scores for the character. 
    Two methods can be used: 
     * the "standard" method, distributing randomly across scores an array of fixed values, 
     * or the "roll" method where 4d6 are rolled for each score, and the highest 3 are summed.

    Returns: A random playable character to either print in the Terminal or output in a text file.
    """
    # Load dataset
    dataset = load_dataset()

    # Generate the main attributes of the character
    new_character = PlayerCharacter(dataset)
    
    # Roll a subrace
    new_character.roll_subrace(dataset)
    
    # Roll a subclass
    new_character.roll_subclass(dataset)
    
    # Roll ability scores
    new_character.roll_ability_scores(dataset, method)

    # Select avatar
    new_character.set_avatar()

    # Set hit points and AC
    new_character.set_hit_points()
    new_character.set_armor_class()

    # Roll skills and proficiencies
    new_character.roll_skills(dataset)
    new_character.roll_proficiencies(dataset)

    # Roll a deity
    new_character.roll_deity(dataset)

    # Generate a dictionary of attributes
    new_character.clean_attributes()
   
    return new_character


# Display and export the character

def print_character(character):
    """
    Print character string and attributes to the terminal
    """

    print(character)
    print(15*'*')
    for k,v in character.attribute_dict.items():
        if k == "Ability scores":
            print(k)
            print(v)
            print(15*'*')
        else:
            print(k, ':', v)


def write_character(character):

    """
    Write character string and attributes to a text file
    """
    with open("character.txt", "w") as out_file:
        print(character, file=out_file)
        print(15*'*', file=out_file)
        for k,v in character.attribute_dict.items():
            if k == "Ability scores":
                print(k, file=out_file)
                print(v, file=out_file)
                print(15*'*', file=out_file)
            else:
                print(k, ':', v, file=out_file)


