import os
from django.db import transaction

from core.models import Size, Language, Name, Group
from npcs.models import NpcRace, NpcKlass, NpcDescription, NpcAttributes
from utils.helpers import chunks

NPC_RACES = (
    ("Human", "human", "Medium", ['Common', ], "strength dexterity constitution wisdom intelligence charisma"),
    ("Half Elf", "elf", "Medium", ['Common', ], "charisma strength constitution"),
    ("Half Orc", "orc", "Medium", ['Common', ], "strength constitution"),
    ("Drow", "drow", "Medium", ['Common', ], "dexterity charisma"),
    ("High Elf", "elf", "Medium", ['Common', ], "dexterity intelligence"),
    ("Wood Elf", "elf", "Medium", ['Common', ], "dexterity wisdom"),
    ("Hill Dwarf", "dwarf", "Medium", ['Common', ], "constitution wisdom"),
    ("Mountain Dwarf", "dwarf", "Medium", ['Common', ], "strength constitution"),
    ("Lightfoot Halfling", "halfling", "Small", ['Common', ], "dexterity charisma"),
    ("Stout Halfling", "halfling", "Small", ['Common', ], "dexterity charisma"),
    ("Forest Gnome", "gnome", "Small", ['Common', ], "dexterity intelligence"),
    ("Rock Gnome", "gnome", "Small", ['Common', ], "constitution intelligence"),
    ("Dragonborn", "dragonborn", "Medium", ['Common', ], "charisma intelligence"),
    ("Tiefling", "thiefling", "Medium", ['Common', ], "charisma intelligence"),
    ("Goliath", "goliath", "Medium", ['Common', ], "strength constitution"),
    ("Merfolk", "merfolk", "Medium", ['Common', ], ""),
    ("Orc", "orc", "Medium", ['Common', ], "strength"),
    # Monsters (for later)
    # ("Tabaxi", "tabaxi", "Medium", ['Common', ], "dexterity charisma"),
    # ("Kenku", "kenku", "Medium", ['Common', ], "dexterity wisdom"),
    # ("Aarakocra", "aarakocra", "Medium", ['Common', ], "dexterity wisdom"),
    # ("Bullywug", "bullywug", "Medium", ['Common', ], ""),
    # ("Gnoll", "gnoll", "Medium", ['Common', ], "strength"),
    # ("Hobgoblin", "goblin", "Medium", ['Common', ], ""),
    # ("Skeleton", "skeleton", "Medium", [], "strength"),
    # ("Zombie", "zombie", "Medium", [], "strength constitution"),
    # ("Goblin", "goblin", "Small", ['Common', ], "dexterity"),
    # ("Kobold", "kobold", "Small", ['Common', ], "dexterity"),
)

KLASSES = [
    ('Berserker', 12, "melee tank strength constitution"),
    ('Holy Champion', 10, "melee tank strength constitution"),
    ('Hermit', 8, "melee dexterity wisdom"),
    ('Militia', 8, "melee ranged strength constitution"),
    ('Knight', 10, "melee tank mounted constitution strength"),
    ('Pikeman', 8, "melee ranged strength constitution"),
    ('Soldier', 10, "melee tank strength constitution"),
    ('Pirate', 8, "melee ranged dexterity constitution"),
    ('Scout', 8, "ranged melee scout dexterity constitution"),
    ('Scoundrel', 8, "ranged melee scout dexterity intelligence"),
    ('Spy', 6, "ranged melee scout charisma dexterity"),
    ('Swordsman', 8, "melee ranged dexterity constitution"),
    ('Acolyte', 6, "caster healing divine wisdom constitution"),
    ('Arcanist', 6, "caster arcane intelligence charisma"),
    ('Evoker', 6, "caster arcane charisma constitution"),
    ('Minstrel', 8, "caster arcane support charisma dexterity"),
    ('Warden', 8, "caster healing divine support wisdom constitution"),
    ('Warchanter', 8, "melee support charisma constitution"),
    ('Aristocrat', 6, "noble charisma intelligence"),
    ('Artisan', 6, "commoner wisdom charisma"),
    ('Beggar', 8, "commoner constitution wisdom"),
    ('Farmer', 8, "commoner constitution strength"),
    ('Healer', 8, "commoner healing wisdom intelligence"),
    ('Innkeeper-Barmaid', 8, "commoner charisma wisdom"),
    ('Scholar', 6, "commoner intelligence wisdom"),
]

NPC_ATTRIBUTES = [
    ["Terrible Array", (8,8,8,8,7,7), ],
    ["Bad Array", (10,10,10,10,10,8), ],
    ["Poor Array", (12,12,11,10,10,8), ],
    ["Medium Array", (14,12,12,10,10,8), ],
    ["Standard Array", (15,14,13,12,10,8), ],
    ["Good Array", (16,14,12,11,10,10), ],
    ["Hero Array", (18,16,14,12,10,10), ],
    ["Epic Array", (20,16,14,14,12,10), ],
    ["Terrible Focused Array", (12,8,8,8,8,7), ],
    ["Bad Focused Array", (13,10,8,8,8,8), ],
    ["Lower Focused Array", (13,10,10,10,8,8), ],
    ["Medium Focused Array", (14,12,10,10,8,8), ],
    ["Higher Focused Array", (16,14,12,10,8,8), ],
    ["Random Array", [], ],
]


def create_npc_attributes():
    for data in NPC_ATTRIBUTES:
        NpcAttributes.objects.get_or_create(rpg_tinker=data[0], values=list(data[1]))


def create_npc_races():
    for data in NPC_RACES:
        group, _ = Group.objects.get_or_create(name=data[1], category=Group.RACE)
        size = Size.objects.get(name=data[2])
        race, _created = NpcRace.objects.get_or_create(name=data[0], group=group, size=size)
        race.tags.clear()
        race.tags.add(*data[4].split(" "))
        race.save()
        for name in data[3]:
            race.languages.add(Language.objects.get(name=name))


def create_npc_klass():
    for data in KLASSES:
        klass, _created = NpcKlass.objects.get_or_create(name=data[0])
        klass.hit_die = data[1]
        klass.tags.clear()
        klass.tags.add(*data[2].split(" "))
        klass.save()


def race_names():
    PREFIXES = ['fng', ]
    ALL_FILES = os.listdir('scrapers/names/')

    for group in Group.objects.filter(category=Group.RACE):
        categories = [Name.MALE, Name.FEMALE, Name.SURNAME]
        for value, name in Name.CATEGORIES:
            if group.names.filter(category=value).count() > 1000:
                continue
            if value not in categories:
                continue

            if name == "Surname":
                filename = ("%s_surnames.txt" % group.name).lower()
            else:
                filename = ("%s_%s_names.txt" % (group.name, name)).lower()
            find_files = [filename]
            find_files += ["%s_%s" % (pre, filename) for pre in PREFIXES]
            files = [name for name in find_files if name in ALL_FILES]
            if not files:
                print(group.name)
                continue

            for f in files:
                with open('scrapers/names/' + f, "r") as names_f:
                    names = names_f.readlines()

                counter = 0
                for chunk in chunks(names, 1000):
                    if counter > 5:
                        continue
                    counter += 1
                    with transaction.atomic():
                        for n in chunk:
                            Name.objects.get_or_create(group=group, category=value, name=n.replace("\n", ""))
                print("added %s" % f)


def npc_descriptions():
    CATEGORIES = (
        ("base", NpcDescription.BASE),
        ("body", NpcDescription.BODY),
        ("conflict_style_physical", NpcDescription.CONFLICT_PHYSICAL),
        ("conflict_style_verbal", NpcDescription.CONFLICT_VERBAL),
        ("disability", NpcDescription.DISABILITY),
        ("emotional_expressions", NpcDescription.EXPRESSION),
        ("face", NpcDescription.FACE),
        ("hair", NpcDescription.HAIR),
        ("marks", NpcDescription.MARK),
        ("other", NpcDescription.OTHER),
        ("personality_quirks", NpcDescription.PERSONALITY_QUIRKS),
        ("physical_skills", NpcDescription.PHYSICAL_SKILLS),
    )

    for filename, category in CATEGORIES:
        with open("scrapers/looks/%s.txt" % filename, "r") as f:
            print("adding %s" % filename)
            lines = f.readlines()
            for chunk in chunks(lines, 1000):
                with transaction.atomic():
                    for line in chunk:
                        NpcDescription.objects.get_or_create(text=line.replace("\n", ""), category=category)


create_npc_attributes()
create_npc_races()
create_npc_klass()
race_names()
npc_descriptions()
