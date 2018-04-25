import requests
from django.core.management.base import BaseCommand

from core.models import (Spell, MagicSchool, Condition, DamageType, Equipment, Language, Proficiency, AbilityScore,
                         Skill, Feature, Race, Size, Abilities, KlassLevel, Klass)


def json_from_url(url):
    # possible to add retry functionality etc later
    return requests.get(url).json()


class Command(BaseCommand):
    help = 'update core models from http://dnd5eapi.co/'

    API_URLS = [
        {"method": 'add_magic_school', "url": "http://dnd5eapi.co/api/magic-schools/"},
        {"method": 'add_spell', "url": "http://dnd5eapi.co/api/spells/"},
        {"method": 'add_condition', "url": "http://dnd5eapi.co/api/conditions/"},
        {"method": 'add_damage_type', "url": "http://dnd5eapi.co/api/damage-types/"},
        {"method": 'add_equipment', "url": "http://dnd5eapi.co/api/equipment/"},
        {"method": 'add_language', "url": "http://dnd5eapi.co/api/languages/"},
        {"method": 'add_proficiency', "url": "http://dnd5eapi.co/api/proficiencies/"},
        {"method": 'add_ability_score', "url": "http://dnd5eapi.co/api/ability-scores/"},
        {"method": 'add_skill', "url": "http://dnd5eapi.co/api/skills/"},
        {"method": 'add_feature', "url": "http://dnd5eapi.co/api/features/"},
        {"method": 'add_race', "url": "http://dnd5eapi.co/api/races/"},
        {"method": 'add_sub_race', "url": "http://dnd5eapi.co/api/subraces/"},
        # {"method": 'add_klasse', "url": "http://dnd5eapi.co/api/classes/"},
    ]

    def convert_to_copper(self, value):
        if value['unit'] == "gp":
            return value['quantity'] * 100
        elif value['unit'] == "sp":
            return value['quantity'] * 10
        elif value['unit'] == "cp":
            return value['quantity']
        raise Exception("No conversion set for %s" % value['unit'])

    def add_klass(self, url):
        data = json_from_url(url)

        # klass, _created = Klass.objects.get_or_create(name=data['name'])
        # klass.hit_die = data['hit_die']

        # multiple possible
        # klass.proficiencies
        # klass.choices

    def add_sizes(self):
        SIZES = (
            ('Tiny', '1/4th square'),
            ('Small', '1x1 square'),
            ('Medium', '1x1 square'),
            ('Large', '2x2 squares'),
            ('Huge', '3x3 squares'),
            ('Gargantuan', '4x4 squares'),
        )
        for name, space in SIZES:
            Size.objects.get_or_create(name=name, space=space)

    def add_sub_race(self, url):
        data = json_from_url(url)
        try:
            parent = Race.objects.get(name=data['race']['name'])
        except Race.DoesNotExist:
            parent = self.add_race(data['race']['url'])
        return self.add_race(url, parent=parent)

    def add_race(self, url, parent=None):
        data = json_from_url(url)
        race, _created = Race.objects.get_or_create(name=data['name'])
        race.parent = parent
        race.speed = data.get("speed")
        race.desc = data.get("desc")
        race.alignment_desc = data.get("alignment")
        race.age_desc = data.get("age")
        race.size_desc = data.get("size_description")
        race.language_desc = data.get("language_desc")

        if data.get("ability_bonuses"):
            bonus = race.ability_bonus if race.ability_bonus else Abilities()
            bonus.bonus = True
            for i, field in enumerate(['strength', 'dexterity', 'constitution', 'wisdom', 'intelligence', 'charisma']):
                setattr(bonus, field, data['ability_bonuses'][i])
            bonus.save()
            race.ability_bonus = bonus

        if not parent:
            race.size = Size.objects.get(name=data['size'])

        # multiples possible
        # traits = models.ManyToManyField("core.Trait")

        race.save()
        # add languages
        for lang in data.get("languages", []):
            try:
                race.languages.add(Language.objects.get(name=lang['name']))
            except Language.DoesNotExist:
                race.languages.add(self.add_language(lang['url']))

        # add proficiencies
        for prof in data.get("starting_proficiencies", []):
            if "from" in prof:
                for temp in prof['from']:
                    del temp['url']
                choice = {"type": prof['type'], "amount": prof['choose'], "choices": prof['from']}
                if choice not in race.choices:
                    race.choices.append(choice)
            else:
                try:
                    race.proficiencies.add(Proficiency.objects.get(name=prof['name']))
                except Proficiency.DoesNotExist:
                    race.proficiencies.add(self.add_proficiency(prof['url']))

        return race

    def add_ability_score(self, url):
        data = json_from_url(url)
        score, _created = AbilityScore.objects.get_or_create(name=data['full_name'])
        score.short = data['name']
        score.desc = data['desc']
        score.save()
        return score

    def add_feature(self, url):
        data = json_from_url(url)
        score, _created = Feature.objects.get_or_create(name=data['name'])
        score.desc = "\n".join(data['desc'])
        score.save()
        return score

    def add_skill(self, url):
        data = json_from_url(url)
        skill, _created = Skill.objects.get_or_create(name=data['name'])
        skill.desc = data['desc']
        try:
            skill.ability_score = AbilityScore.objects.get(short=data['ability_score']['name'])
        except AbilityScore.DoesNotExist:
            skill.ability_score = self.add_ability_score(data['ability_score']['url'])
        skill.save()
        return skill

    def add_language(self, url):
        data = json_from_url(url)
        language, _created = Language.objects.get_or_create(name=data['name'])
        language.type = data['type']
        language.script = data['script']
        language.save()
        return language

    def add_proficiency(self, url):
        data = json_from_url(url)
        proficiency, _created = Proficiency.objects.get_or_create(name=data['name'])
        proficiency.type = data['type']
        proficiency.save()
        return proficiency

    def add_equipment(self, url):
        data = json_from_url(url)
        equipment, _created = Equipment.objects.get_or_create(name=data['name'])

        equipment.type = data.get("type")
        equipment.sub_type = data.get("subtype")

        # proficiencies count as OR
        # requirements = models.ManyToManyField("core.Requirement")

        # weapon specific
        if "damage" in data:
            equipment.range = data.get("weapon_range")
            equipment.dice_count = data.get("damage", {}).get("dice_count")
            equipment.dice_value = data.get("damage", {}).get("dice_value")
            equipment.properties = data.get("properties")
            if data.get("damage", {}):
                try:
                    equipment.damage_type = DamageType.objects.get(name=data["damage"]['damage_type'].get("name"))
                except DamageType.DoesNotExist:
                    equipment.damage_type = self.add_damage_type(data["damage"]['damage']['url'])

        # armor specific
        if "armor_class" in data:
            equipment.bonus = data["armor_class"]['base'] - 10
            equipment.dex_bonus = data["armor_class"]["max_bonus"]
            if data.get("stealth") == "Disadvantage":
                equipment.stealth = False
            else:
                equipment.stealth = None

        # price is always set in copper and will be calculated to readable price
        equipment.price = self.convert_to_copper(data["cost"])
        equipment.weight = data.get("weight")

        return equipment

    def add_condition(self, url):
        data = json_from_url(url)
        condition, _created = Condition.objects.get_or_create(name=data['name'])
        condition.desc = data["desc"]
        return condition

    def add_magic_school(self, url):
        data = json_from_url(url)
        school, _created = MagicSchool.objects.get_or_create(name=data['name'])
        school.desc = data["desc"]
        school.save()
        return school

    def add_damage_type(self, url):
        data = json_from_url(url)
        damage, _created = DamageType.objects.get_or_create(name=data['name'])
        damage.desc = "\n".join(data["desc"])
        damage.save()
        return damage

    def add_spell(self, url):
        data = json_from_url(url)

        spell, _created = Spell.objects.get_or_create(name=data['name'])
        spell.desc = "\n".join(data["desc"])
        spell.higher_level = "\n".join(data["higher_level"]) if data.get('higher_level') else None
        spell.page = data["page"]
        spell.range = data["range"]
        spell.components = data["components"]
        spell.material = data.get("material")
        spell.ritual = data["ritual"] == "yes"
        spell.duration = data["duration"]
        spell.concentration = data["concentration"]
        spell.casting_time = data["casting_time"]
        spell.level = data["level"]

        try:
            school = MagicSchool.objects.get(name=data['school']['name'])
        except MagicSchool.DoesNotExist:
            school = self.add_magic_school(data["school"]['url'])

        spell.school = school
        spell.save()
        return spell

    def handle(self, *args, **options):
        self.add_sizes()

        for part in self.API_URLS:
            print("updating %s" % part['method'])
            for link in json_from_url(part['url'])['results']:
                getattr(self, part['method'])(link['url'])