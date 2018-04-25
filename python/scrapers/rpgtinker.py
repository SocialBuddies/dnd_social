import random
import uuid
import requests
from bs4 import BeautifulSoup
import time
import pathlib
from selenium import webdriver


class RpgTinker(object):
    TEMPLATES = {
        # strength
        "Berserker": {"hit_dice": "d12", "focus": "strength"}, 
        "Holy Champion": {"hit_dice": "d10", "focus": "strength"}, 
        "Hermit": {"hit_dice": "d10", "focus": "strength"},
        "Militia": {"hit_dice": "d8", "focus": "strength"}, 
        "Knight": {"hit_dice": "d10", "focus": "strength"}, 
        "Pikeman": {"hit_dice": "d8", "focus": "strength"}, 
        "Soldier": {"hit_dice": "d8", "focus": "strength"},
        # dexterity
        "Pirate": {"hit_dice": "d8", "focus": "dexterity"}, 
        "Scout": {"hit_dice": "d8", "focus": "dexterity"}, 
        "Spy": {"hit_dice": "d6", "focus": "dexterity"}, 
        "Swordsman": {"hit_dice": "d10", "focus": "dexterity"},
        # caster
        "Acolyte": {"hit_dice": "d6", "focus": "caster"}, 
        "Arcanist": {"hit_dice": "d6", "focus": "caster"}, 
        "Evoker": {"hit_dice": "d8", "focus": "caster"},
        # profession
        "Artisan": {"hit_dice": "d6", "focus": "profession"}, 
        "Beggar": {"hit_dice": "d6", "focus": "profession"}, 
        "Farmer": {"hit_dice": "d8", "focus": "profession"}, 
        "Healer": {"hit_dice": "d6", "focus": "profession"}, 
        "Innkeeper-Barmaid": {"hit_dice": "d8", "focus": "profession"}, 
        "Scholar": {"hit_dice": "d6", "focus": "profession"},
    }
    
    RACES = {
        # common
        "Human": {"hit_dice": "d8", "occurrance": "common"}, 
        "Half Elf": {"hit_dice": "d8", "occurrance": "common"}, 
        "Half Orc": {"hit_dice": "d8", "occurrance": "common"}, 
        "Drow": {"hit_dice": "d8", "occurrance": "common"}, 
        "High Elf": {"hit_dice": "d8", "occurrance": "common"}, 
        "Wood Elf": {"hit_dice": "d8", "occurrance": "common"}, 
        "Hill Dwarf": {"hit_dice": "d8", "occurrance": "common"}, 
        "Mountain Dwarf": {"hit_dice": "d8", "occurrance": "common"},
        "Lightfoot Halfling": {"hit_dice": "d6", "occurrance": "common"},
        "Stout Halfling": {"hit_dice": "d6", "occurrance": "common"},
        "Forest Gnome": {"hit_dice": "d6", "occurrance": "common"},
        "Rock Gnome": {"hit_dice": "d6", "occurrance": "common"},
        "Dragonborn": {"hit_dice": "d8", "occurrance": "common"}, 
        "Tiefling": {"hit_dice": "d8", "occurrance": "common"},
        "Goliath": {"hit_dice": "d8", "occurrance": "common"},
        # monster - common
        "Gnoll": {"hit_dice": "d8", "occurrance": "monster"}, 
        "Hobgoblin": {"hit_dice": "d8", "occurrance": "monster"}, 
        "Merfolk": {"hit_dice": "d8", "occurrance": "monster"}, 
        "Orc": {"hit_dice": "d8", "occurrance": "monster"}, 
        "Kobold": {"hit_dice": "d6", "occurrance": "monster"},
        "Goblin": {"hit_dice": "d6", "occurrance": "monster"},
        # monster rare
        "Tabaxi": {"hit_dice": "d8", "occurrance": "monster_rare"}, 
        "Aarakocra": {"hit_dice": "d8", "occurrance": "monster_rare"}, 
        "Bullywug": {"hit_dice": "d8", "occurrance": "monster_rare"},
    }
    
    ATTRIBUTES = {
        "Terrible Array": "Terrible Array (8,8,8,8,7,7)",
        "Bad Array": "Bad Array (10,10,10,10,10,8)",
        "Poor Array": "Poor Array (12,12,11,10,10,8)",
        "Medium Array": "Medium Array (14,12,12,10,10,8)",
        "Standard Array": "Standard Array (15,14,13,12,10,8)",
        "Good Array": "Good Array (16,14,12,11,10,10)",
        "Hero Array": "Hero Array (18,16,14,12,10,10)",
        "Epic Array": "Epic Array (20,16,14,14,12,10)",
        "Terrible Focused Array": "Terrible Focused Array (12,8,8,8,8,7)",
        "Bad Focused Array": "Bad Focused Array (13,10,8,8,8,8)",
        "Lower Focused Array": "Lower Focused Array (13,10,10,10,8,8)",
        "Medium Focused Array": "Medium Focused Array (14,12,10,10,8,8)",
        "Higher Focused Array": "Higher Focused Array (16,14,12,10,8,8)",
        "Random Array": "Random Array (4d6 method)"
    }

    LEVELS = [i for i in range(1, 21)]

    HIT_DICE = ["d%s" % i for i in [4, 6, 8, 10, 12, 20]]
    
    def __init__(self, driver=None, to_file=False, template=None, race=None, attribute=None, level=None,
                 hit_dice=None, **kwargs):
        self.template = template if template else self.random_template(**kwargs)
        self.race = race if race else self.random_race(**kwargs)
        self.attribute = attribute if attribute else self.random_attribute(**kwargs)
        self.level = level if level else self.random_level(**kwargs)
        self.hit_dice = hit_dice if hit_dice else self.random_hit_dice(template=self.template, **kwargs)
        self.driver = driver
        self.to_file = to_file

    def random_template(self, **kwargs):
        # TODO: build and give option to choose category of template
        if kwargs:
            pass
        else:
            return random.choice(list(self.TEMPLATES.keys()))

    def random_race(self, **kwargs):
        # TODO: build and give option to choose category of race
        if kwargs:
            pass
        else:
            return random.choice(list(self.RACES.keys()))

    def random_attribute(self, **kwargs):
        # TODO: build and give option to choose category of attributes
        if kwargs:
            pass
        else:
            return random.choice(list(self.ATTRIBUTES.keys()))

    def random_level(self, **kwargs):
        # TODO: build and give option to choose range of levels
        if kwargs:
            pass
        else:
            return random.choice(self.LEVELS)

    def random_hit_dice(self, **kwargs):
        # TODO: build and give option to choose range of hit dice
        # by default thsi is based on tempalte first, else race with a random fallback
        if kwargs:
            if "template" in kwargs:
                return self.TEMPLATES[kwargs['template']]['hit_dice']
            elif "race" in kwargs:
                return random.choice(['d6', 'd8'])
        else:
            return random.choice(['d6', 'd8'])

    def generate_url(self):
        url = "http://rpgtinker.com/index.php?"
        url += "template=%s" % self.template.replace(" ", "+")
        url += "&race=%s" % self.race.replace(" ", "+")
        url += "&radioattribute=%s" % self.ATTRIBUTES[self.attribute].replace(" ", "+").replace(",", "%2C")
        url += "&radioattribute=%s" % self.attribute.replace(" ", "+").replace(",", "%2C")
        url += "&numberofhitdice=%s" % self.level
        url += "&hitdice=%s" % self.hit_dice
        return url

    def find_path(self):
        path = "scrapers/npc_stats/"
        path += self.template.lower().replace(" ", "_") + "/"
        path += self.race.lower().replace(" ", "_") + "/"
        path += "level_%s" % str(self.level) + "/"
        path += self.attribute.lower().replace(" ", "_") + "/"

        # make sure path exists
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def scrape_npc(self):
        if self.driver:
            self.driver.get(self.generate_url())
            data = self.driver.find_element_by_css_selector(".character-sheet > div:nth-child(1)")
            html = data.get_attribute("innerHTML")

        else:
            response = requests.get(self.generate_url())
            soup = BeautifulSoup(response.content, "html.parser")
            data = soup.find("div", {"class": "col-xs-12 col-sm-12 col-md-4 col-md-offset-2"})
            html = str(data)

        if self.to_file:
            # save to file
            path = self.find_path()
            with open(path + "stats_%s.html" % uuid.uuid4().hex[:10], "w") as f:
                f.write(html)
        else:
            return html


def scrape_npc_stats():
    for template in sorted(list(RpgTinker.TEMPLATES.keys())):
        print("doing template %s" % template)
        for race in sorted(["Human", "Half Elf", "Half Orc", "Drow", "High Elf", "Wood Elf", "Hill Dwarf", "Mountain Dwarf", "Lightfoot Halfling", "Stout Halfling", "Forest Gnome", "Rock Gnome", "Dragonborn", "Tiefling", "Goliath"]): #noqa
            print("doing race %s" % race)
            for level in sorted(RpgTinker.LEVELS):
                print("doing level %s" % level)
                for i in range(7):
                    tinker = RpgTinker(level=level, template=template, race=race, attribute="Lower Focused Array")
                    tinker.scrape_npc()
                for i in range(7):
                    tinker = RpgTinker(level=level, template=template, race=race, attribute="Poor Array")
                    tinker.scrape_npc()
                for i in range(7):
                    tinker = RpgTinker(level=level, template=template, race=race, attribute="Standard Array")
                    tinker.scrape_npc()
