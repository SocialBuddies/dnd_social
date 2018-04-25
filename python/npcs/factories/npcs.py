import random

from core.models import Alignment, Name
from npcs.models import NpcRace, NpcKlass
from utils.helpers import FieldRandomizer
# from scrapers.rpgtinker import RpgTinker


class NpcFactory(FieldRandomizer):
    FIELDS = ["race", 'klass', 'alignment', 'level', 'gender']

    def level_choices(self):
        return range(1, random.randint(1, 20))

    def race_choices(self):
        return NpcRace.objects.all()

    def klass_choices(self):
        return NpcKlass.objects.all()

    def alignment_choices(self):
        return Alignment.objects.all()

    def gender_choices(self):
        return [gender for gender, _name in Name.GENDERS]

    def randomize(self, instance, commit=True):
        instance = super().randomize(instance, commit=False)

        # adding name
        name_qs = instance.race.group.names.filter(category=instance.gender)
        surname_qs = instance.race.group.names.filter(category=Name.SURNAME)
        instance.name = self.random_qs_choice(name_qs)
        instance.surname = self.random_qs_choice(surname_qs)

        if commit:
            instance.save()
        return instance


# class NpcFactory(object):
#     T_TYPES = {
#         "physical": ['Berserker', 'Holy Champion', 'Hermit', 'Militia', 'Knight', 'Pikeman', 'Soldier', 'Pirate',
#                      'Scout', 'Spy', 'Swordsman', ],
#         "strength": ['Berserker', 'Holy Champion', 'Hermit', 'Militia', 'Knight', 'Pikeman', 'Soldier',],
#         "dexterity": ['Pirate', 'Scout', 'Spy', 'Swordsman', ],
#         "caster": ['Acolyte', 'Arcanist', 'Evoker', 'Healer', ],
#         "profession": ['Artisan', 'Beggar', 'Farmer', 'Healer', 'Innkeeper-Barmaid', 'Scholar', ],
#     }
#
#     R_TYPES = {
#         "common": ['Human', 'Half Elf', 'Half Orc', 'Drow', 'High Elf', 'Wood Elf', 'Hill Dwarf', 'Mountain Dwarf',
#                    'Lightfoot Halfling', 'Stout Halfling', 'Forest Gnome', 'Rock Gnome', 'Dragonborn', 'Tiefling',
#                    'Goliath', ],
#         "elf": ['Half Elf', 'High Elf', 'Wood Elf', ],
#         "dwarf": ['Hill Dwarf', 'Mountain Dwarf', ],
#         "gnome": ['Forest Gnome', 'Rock Gnome', ],
#         "halfling": ['Lightfoot Halfling', 'Stout Halfling', ],
#         "monster": ['Gnoll', 'Hobgoblin', 'Merfolk', 'Orc', 'Kobold', 'Goblin', ],
#         "moster_rare": ['Tabaxi', 'Aarakocra', 'Bullywug', ],
#     }
#
    # A_TYPES = {
    #     "random": ['Random Array'],
    #     "strong": ['Higher Focused Array', 'Medium Focused Array', 'Epic Array', 'Hero Array', 'Random Array',
    #                'Good Array', 'Standard Array', ],
    #     "normal": ['Poor Array', 'Standard Array', 'Good Array', 'Medium Focused Array', 'Higher Focused Array',
    #                'Random Array', ],
    #     "weak": ['Bad Array', 'Poor Array', 'Bad Focused Array', 'Lower Focused Array', 'Random Array', ],
    # }
#
#     tmp = []
#     for values in A_TYPES.values():
#         tmp += list(values)
#     ALL_ATTRIBUTES = list(set(tmp))
#
#     L_TYPES = {
#         "novice": range(1, 4),
#         "beginner": range(2, 5),
#         "competent": range(3, 7),
#         "proficient": range(5, 10),
#         "expert": range(7, 14),
#         "master": range(10, 20),
#     }
#
#     ALIGNMENTS = [Alignment.GOOD] * 10 + [Alignment.NEUTRAL] * 6 + [Alignment.EVIL] * 4
#     OBEDIENCES = [Alignment.LAWFUL] * 3 + [Alignment.NEUTRAL] * 2 + [Alignment.CHAOTIC] * 2
#
#     HIT_DICE = {
#         "Berserker": {"hit_die": "d12", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Holy Champion": {"hit_die": "d10", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Hermit": {"hit_die": "d10", "description_kwargs": [{"field": "conflict_verbal", "amount": 1}]},
#         "Militia": {"hit_die": "d8", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Knight": {"hit_die": "d10", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Pikeman": {"hit_die": "d8", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Soldier": {"hit_die": "d8", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Pirate": {"hit_die": "d8", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Scout": {"hit_die": "d8", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Spy": {"hit_die": "d6", "description_kwargs": [{"field": "conflict_verbal", "amount": 1}]},
#         "Swordsman": {"hit_die": "d10", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Acolyte": {"hit_die": "d6", "description_kwargs": [{"field": "conflict_verbal", "amount": 1}]},
#         "Arcanist": {"hit_die": "d6", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Evoker": {"hit_die": "d8", "description_kwargs": [{"field": "conflict_physical", "amount": 1}]},
#         "Artisan": {"hit_die": "d6", "description_kwargs": [{}]},
#         "Beggar": {"hit_die": "d6", "description_kwargs": [{"field": "conflict_verbal", "amount": 1}]},
#         "Farmer": {"hit_die": "d8", "description_kwargs": [{}]},
#         "Healer": {"hit_die": "d6", "description_kwargs": [{"field": "conflict_verbal", "amount": 1}]},
#         "Innkeeper-Barmaid": {"hit_die": "d8", "description_kwargs": [{"field": "conflict_verbal", "amount": 1}]},
#         "Scholar": {"hit_die": "d6", "description_kwargs": [{}]},
#     }
#
#     def __init__(self, klass=None, race=None, quality=None, level=None, hit_die=None, alignment=None, **kwargs):
#         self.kwargs = kwargs
#         self.description_factory = NpcDescriptionFactory()
#         # base settings
#         self._klass = klass
#         self._race = race
#         self._quality = quality
#         self._level = level
#         self._hit_die = hit_die
#         self._alignment = alignment
#
#         # prepare for randomizing
#         self.name = None
#         self.gender = None
#         self.klass = None
#         self.race = None
#         self.quality = None
#         self.level = None
#         self.hit_die = None
#         self.alignment = None
#
#     def random_klass(self):
#         if isinstance(self._klass, Klass):
#             return self._klass
#         if "t_type" in self.kwargs:
#             name = random.choice(self.T_TYPES[self.kwargs['t_type']])
#             return Klass.objects.get(name=name)
#         return Klass.objects.order_by("?")[0]
#
#     def random_race(self,):
#         if isinstance(self._race, Race):
#             return self._race
#         if "r_type" in self.kwargs:
#             name = random.choice(self.R_TYPES[self.kwargs['r_type']])
#             return Race.objects.get(name=name)
#         return Race.objects.order_by("?")[0]
#
#     def random_quality(self):
#         if self._quality:
#             return random.choice(self.A_TYPES[self._quality])
#         return random.choice(self.ALL_ATTRIBUTES)
#
#     def random_alignment(self):
#         if isinstance(self._alignment, Alignment):
#             return self._alignment
#         # by default there is a higher chance of good alignments over evil
#         # good > neutral > evil
#         alignment = random.choice(self.ALIGNMENTS)
#         obedience = random.choice(self.OBEDIENCES)
#         if "a_choices" in self.kwargs:
#             alignment = random.choice(self.kwargs['a_choices'])
#         if "o_choices" in self.kwargs:
#             obedience = random.choice(self.kwargs['a_choices'])
#         return Alignment.objects.get_or_create(alignment=alignment, obedience=obedience)[0]
#
#     def random_level(self):
#         if isinstance(self._level, int):
#             return self._level
#         if "l_type" in self.kwargs:
#             return random.choice(self.L_TYPES[self.kwargs['l_type']])
#         return random.randint(1, random.randint(1, 20))
#
#     def random_gender(self):
#         gender = self.kwargs.get("gender", None)
#         if gender:
#             for value, name in Name.GENDERS:
#                 if name.lower() == gender.lower():
#                     return value
#         return random.choice([v for v, n in Name.GENDERS])
#
#     def random_name(self):
#         name = ""
#         # add first-name
#         try:
#             tmp = self.race.group.names.filter(category=self.gender).random()
#             if tmp:
#                 name += tmp.name
#         except Name.DoesNotExist:
#             pass
#
#         name = name + " " if name else ""
#         try:
#             tmp = self.race.group.names.filter(category=Name.SURNAME).random()
#             if tmp:
#                 name += tmp.name
#         except Name.DoesNotExist:
#             pass
#
#         return name
#
#     def get_combat_sheet(self):
#         tinker = RpgTinker(template=self.klass.name, race=self.race.name, level=self.level,
#                            hit_dice=self.hit_die, attribute=self.attribute)
#         return tinker.scrape_npc()
#
#     def create_npc(self):
#         self.klass = self.random_klass()
#         self.race = self.random_race()
#         self.quality = self.random_quality()
#         self.level = self.random_level()
#         self.hit_die = self.HIT_DICE[self.klass.name]['hit_die']
#         self.alignment = self.random_alignment()
#
#         self.gender = self.random_gender()
#         self.name = self.random_name()
#
#         npc = Npc.objects.create(
#             name=self.name,
#             gender=self.gender,
#             klass=self.klass,
#             race=self.race,
#             alignment=self.alignment,
#             quality=self.quality,
#             level=self.level,
#             sheet=self.get_combat_sheet() if self.kwargs.get('get_sheet') else None
#         )
#
#         descriptions = self.description_factory.random_descriptions(**self.kwargs.get("description", {}))
#         npc.descriptions.add(*descriptions)
#         return npc
#
#
# class NpcDescriptionFactory(object):
#     # this is pure random for now
#     BASE_IDS = NpcDescription.objects.filter(category=NpcDescription.BASE).values_list("pk", flat=True)
#     BODY_IDS = NpcDescription.objects.filter(category=NpcDescription.BODY).values_list("pk", flat=True)
#     CONFLICT_PHYSICAL_IDS = NpcDescription.objects.filter(category=NpcDescription.CONFLICT_PHYSICAL).values_list(
#         "pk", flat=True)
#     CONFLICT_VERBAL_IDS = NpcDescription.objects.filter(category=NpcDescription.CONFLICT_VERBAL).values_list(
#         "pk", flat=True)
#     DISABILITY_IDS = NpcDescription.objects.filter(category=NpcDescription.DISABILITY).values_list("pk", flat=True)
#     EXPRESSION_IDS = NpcDescription.objects.filter(category=NpcDescription.EXPRESSION).values_list("pk", flat=True)
#     FACE_IDS = NpcDescription.objects.filter(category=NpcDescription.FACE).values_list("pk", flat=True)
#     HAIR_IDS = NpcDescription.objects.filter(category=NpcDescription.HAIR).values_list("pk", flat=True)
#     MARK_IDS = NpcDescription.objects.filter(category=NpcDescription.MARK).values_list("pk", flat=True)
#     OTHER_IDS = NpcDescription.objects.filter(category=NpcDescription.OTHER).values_list("pk", flat=True)
#     PERSONALITY_QUIRKS_IDS = NpcDescription.objects.filter(
#         category=NpcDescription.PERSONALITY_QUIRKS).values_list("pk", flat=True)
#     PHYSICAL_SKILLS_IDS = NpcDescription.objects.filter(
#         category=NpcDescription.PHYSICAL_SKILLS).values_list("pk", flat=True)
#
#     ALWAYS_HAS = [
#         {"field": "base", "amount": [1, 1]},
#         {"field": "body", "amount": [1, 1]},
#         {"field": "expression", "amount": [1, 1]},
#         {"field": "face", "amount": [1, 1]},
#         {"field": "hair", "amount": [1, 1]},
#         {"field": "personality_quirks", "amount": [1, 3]},
#     ]
#     OPTIONAL = [
#         {"field": "conflict_physical", "amount": [1, 1]},
#         {"field": "conflict_verbal", "amount": [1, 1]},
#         {"field": "disability", "amount": [1, 1], "occurrence": "rare"},
#         {"field": "mark", "amount": [1, 1]},
#         {"field": "other", "amount": [1, 1]},
#         {"field": "physical_skills", "amount": [1, 1]},
#     ]
#
#     def get_random(self, field, amount):
#         picks = []
#         for i in range(amount):
#             try:
#                 picks.append(random.choice(getattr(self, ("%s_IDS" % field).upper())))
#             except IndexError:
#                 print(field)
#         return picks
#
#     def random_descriptions(self, **kwargs):
#         data = []
#         for des in self.ALWAYS_HAS:
#             if isinstance(des['amount'], int):
#                 amount = des['amount']
#             else:
#                 amount = random.randint(des['amount'][0], des['amount'][1])
#             data += self.get_random(des['field'], amount)
#         for des in self.OPTIONAL:
#             if des['field'] in kwargs:
#                 if isinstance(des['amount'], int):
#                     amount = des['amount']
#                 else:
#                     amount = random.randint(des['amount'][0], des['amount'][1])
#                 data += self.get_random(des['field'], amount)
#             else:
#                 # see if needs to be added
#                 if random.randint(0, 1):
#                     continue
#                 amount = 0
#                 for i in range(random.randint(des['amount'][0], des['amount'][0])):
#                     if des.get('occurrence') == "rare":
#                         amount += random.randint(0, random.randint(0, 1))
#                     else:
#                         amount += random.randint(0, 1)
#                 data += self.get_random(des['field'], amount)
#
#         return data
