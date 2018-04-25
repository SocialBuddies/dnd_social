from operator import itemgetter

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class Size(models.Model):
    TINY, SMALL, MEDIUM, LARGE, HUGE, GARGANTUAN = 1, 2, 3, 4, 5, 6
    SIZES = (
        (TINY, 'Tiny'),
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (HUGE, 'Huge'),
        (GARGANTUAN, 'Gargantuan'),
    )

    value = models.SmallIntegerField(choices=SIZES, unique=True)
    space = models.CharField(max_length=31)

    @property
    def name(self):
        return self.get_value_display()


class Alignment(models.Model):
    EVIL = 1
    NEUTRAL = 2
    GOOD = 3
    CHAOTIC = 1
    TRUE = 2
    LAWFUL = 3
    OBEDIENCES = [(LAWFUL, 'Lawful'), (TRUE, 'True'), (CHAOTIC, 'Chaotic'), ]
    ALIGNMENTS = [(GOOD, 'Good'), (NEUTRAL, 'Neutral'), (EVIL, 'Evil'), ]

    obedience = models.SmallIntegerField(choices=OBEDIENCES, null=True)
    alignment = models.SmallIntegerField(choices=ALIGNMENTS, null=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return "%s %s" % (self.get_obedience_display(), self.get_alignment_display())


class BonusTo(models.Model):
    COMBAT, DEFENSE, SKILL, ABILITY, SPECIAL, LANGUAGE = 'combat', 'defense', 'skill', 'ability', 'special', 'language'
    CATEGORIES = (
        (COMBAT, 'Combat'),
        (DEFENSE, 'Defense'),
        (SKILL, 'Skill'),
        (ABILITY, 'Ability'),
        (SPECIAL, 'Special'),
    )

    category = models.CharField(max_length=31, choices=CATEGORIES)
    fields = ArrayField(models.CharField(max_length=31))


class Language(models.Model):
    CELESTIAL = 'celestial'
    COMMON = 'common'
    DRACONIC = 'draconic'
    DWARVISH = 'dwarvish'
    ELVISH = 'elvish'
    INFERNAL = 'infernal'
    NO_SCRIPT = 'no_script'
    SCRIPTS = [
        (CELESTIAL, 'Celestial'),
        (COMMON, 'Common'),
        (DRACONIC, 'Draconic'),
        (DWARVISH, 'Dwarvish'),
        (ELVISH, 'Elvish'),
        (INFERNAL, 'Infernal'),
        (NO_SCRIPT, 'No script'),
    ].sort(key=itemgetter(1))

    STANDARD, EXOTIC = True, False
    CATEGORIES = [(STANDARD, 'Standard'), (EXOTIC, 'Exotic')]

    name = models.CharField(max_length=63, unique=True)
    script = models.CharField(max_length=31, choices=SCRIPTS, blank=True)
    category = models.BooleanField(choices=CATEGORIES)

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    adult = models.SmallIntegerField(null=True)
    death = models.SmallIntegerField(null=True)
    languages = models.ManyToManyField('core.Language')
    speed = models.TextField(blank=True, null=True)
    alignment = models.ForeignKey('core.Alignment', null=True)
    alignment_description = models.TextField(blank=True, null=True)
    abilities = models.ForeignKey('core.Abilities', null=True)
    trained_skills = models.ForeignKey('core.TrainedSkills', null=True)

    choices = JSONField(default={})

    def __str__(self):
        return self.name


class Abilities(models.Model):
    strength = models.SmallIntegerField()
    dexterity = models.SmallIntegerField()
    constitution = models.SmallIntegerField()
    intelligence = models.SmallIntegerField()
    wisdom = models.SmallIntegerField()
    charisma = models.SmallIntegerField()


class TrainedSkills(models.Model):
    STR_SKILLS = ['athletics', ]
    DEX_SKILLS = ['acrobatics', 'sleight_of_hand', 'stealth']
    CON_SKILLS = []
    INT_SKILLS = ['arcana', 'history', 'investigation', 'nature', 'religion']
    WIS_SKILLS = ['animal_handling', 'insight', 'medicine', 'perception', 'survival']
    CHA_SKILLS = ['deception', 'intimidation', 'performance' 'persuasion']
    SKILLS = STR_SKILLS + DEX_SKILLS + CON_SKILLS + INT_SKILLS + WIS_SKILLS + CHA_SKILLS
    SKILL_CHOICES = [(s, s.title().replace('_', ' ')) for s in SKILLS]

    acrobatics = models.BooleanField(default=False)
    animal_handling = models.BooleanField(default=False)
    arcana = models.BooleanField(default=False)
    athletics = models.BooleanField(default=False)
    deception = models.BooleanField(default=False)
    history = models.BooleanField(default=False)
    insight = models.BooleanField(default=False)
    intimidation = models.BooleanField(default=False)
    investigation = models.BooleanField(default=False)
    medicine = models.BooleanField(default=False)
    nature = models.BooleanField(default=False)
    perception = models.BooleanField(default=False)
    performance = models.BooleanField(default=False)
    persuasion = models.BooleanField(default=False)
    religion = models.BooleanField(default=False)
    sleight_of_hand = models.BooleanField(default=False)
    stealth = models.BooleanField(default=False)
    survival = models.BooleanField(default=False)


class Feature(models.Model):
    name = models.CharField(max_length=127, unique=True)


class PartFeature(models.Model):
    feature = models.ForeignKey('core.Feature')
    bonus_to = models.ForeignKey('core.BonusTo')
    description = models.TextField()


class SkillBonus(models.Model):
    # possible relations (instead of generic relation)
    race = models.ForeignKey('core.Race')

    name = models.CharField(max_length=64)
    skill = models.CharField(max_length=31, choices=TrainedSkills.SKILL_CHOICES)
    bonus = models.TextField()

    def __str__(self):
        return "%s %d" % (self.get_skill_display(), self.value)


class Proficiency(models.Model):
    WEAPON, ARMOR, TOOL, SKILL = 1, 2, 3, 4
    CATEGORIES = (
        (WEAPON, 'Weapon'),
        (ARMOR, 'Armor'),
        (TOOL, 'Tool'),
        (SKILL, 'Skill'),
    )
    name = models.CharField(max_length=63, unique=True)
    category = models.SmallIntegerField(choices=CATEGORIES)
    fields = ArrayField(models.CharField(max_length=31))


class Spell(models.Model):
    name = models.CharField(max_length=64, unique=True)
    level = models.SmallIntegerField()
    # klasses = models.ManyToManyField()
    casting_time = models.CharField(max_length=64)
    range = models.CharField(max_length=64)
    components = models.CharField(max_length=64)
    duration = models.CharField(max_length=64)
    description = models.TextField()
    higher_level = models.TextField(blank=True, null=True)
