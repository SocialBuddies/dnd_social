from operator import itemgetter

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from utils.managers import RandomChoiceManager


class Name(models.Model):
    MALE = 1
    FEMALE = 2
    SURNAME = 3
    GENDERS = ((MALE, 'Male'), (FEMALE, 'Female'), )
    CATEGORIES = ((MALE, 'Male'), (FEMALE, 'Female'), (SURNAME, "Surname"))

    name = models.CharField(max_length=50)
    category = models.SmallIntegerField(choices=CATEGORIES)
    group = models.ForeignKey('core.Group', related_name="names", null=True, on_delete=models.SET_NULL)

    objects = RandomChoiceManager()

    class Meta:
        unique_together = ['group', 'name', 'category']

    def __str__(self):
        return self.name


class Group(models.Model):
    RACE = 'race'
    CATEGORIES = ((RACE, "Race"), )
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=25, choices=CATEGORIES)

    class Meta:
        ordering = ['name', ]
        unique_together = ['name', 'category']

    def __str__(self):
        return self.name


class AbilityScore(models.Model):
    """Ability score flavor"""

    name = models.CharField(max_length=32)
    short = models.CharField(max_length=32, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)


class Skill(models.Model):
    """ Skills in dnd and their description """

    name = models.CharField(max_length=32, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    ability_score = models.ForeignKey("core.AbilityScore", null=True, blank=True, on_delete=models.SET_NULL)


class Abilities(models.Model):
    """Keeps track of abilities. bonus is used when they are not a full calculated set of abilities"""

    bonus = models.BooleanField()
    strength = models.SmallIntegerField()
    dexterity = models.SmallIntegerField()
    constitution = models.SmallIntegerField()
    wisdom = models.SmallIntegerField()
    intelligence = models.SmallIntegerField()
    charisma = models.SmallIntegerField()


class Size(models.Model):
    name = models.CharField(max_length=32, unique=True)
    space = models.CharField(max_length=31)

    def __str__(self):
        return self.name


class Proficiency(models.Model):
    """Character proficiencies"""

    WEAPON = ""
    ARMOR = ""
    SKILL = ""
    TYPES = ((WEAPON, ""), (ARMOR, ""), (SKILL, ""))

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    """Special qualities a character possesses"""

    name = models.CharField(max_length=64)
    desc = models.TextField(null=True, blank=True)


class Race(models.Model):
    """ Holds tradition races from dnd 5 """

    parent = models.ForeignKey("core.Race", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64, unique=True)
    speed = models.PositiveSmallIntegerField(null=True, blank=True)
    ability_bonus = models.ForeignKey("core.Abilities", null=True, blank=True, on_delete=models.SET_NULL)

    desc = models.TextField(null=True, blank=True)
    alignment_desc = models.TextField(null=True, blank=True)
    age_desc = models.TextField(null=True, blank=True)
    size = models.ForeignKey("core.Size", null=True, blank=True, on_delete=models.SET_NULL)
    size_desc = models.TextField(null=True, blank=True)
    language_desc = models.TextField(null=True, blank=True)

    # multiples possible
    proficiencies = models.ManyToManyField('core.Proficiency')
    languages = models.ManyToManyField('core.Language')
    # traits = models.ManyToManyField("core.Trait")

    choices = JSONField(default=[])


class Klass(models.Model):
    """Character classes"""

    name = models.CharField(max_length=64, unique=True)
    hit_die = models.PositiveSmallIntegerField()

    # multiple possible
    proficiencies = models.ManyToManyField('core.Proficiency')
    saving_throws = models.ManyToManyField('core.AbilityScore')

    choices = JSONField(default={})

    def __str__(self):
        return self.name


class KlassLevel(models.Model):
    """Things a klass gains per level"""

    klass = models.ForeignKey("core.Klass", null=True, blank=True, on_delete=models.SET_NULL)
    level = models.SmallIntegerField()
    ability_bonuses = models.SmallIntegerField(default=0)   # total abilty bonuses gained by levels
    prof_bonus = models.SmallIntegerField()
    spell_casting = models.ForeignKey("core.SpellCasting", null=True, blank=True, on_delete=models.SET_NULL)
    # specific = models.ForeignKey("core.KlassSpecific", null=True, blank=True)

    # multiple
    features = models.ManyToManyField("core.Feature")

    choices = JSONField(default={})


class SpellCasting(models.Model):
    """Holds spell casting values for klass(level)"""

    known = ArrayField(models.PositiveSmallIntegerField(), size=10)     # holds known spells from cantrip till 9
    slots = ArrayField(models.PositiveSmallIntegerField(), size=10)     # holds spell slots from cantrip till 9

    def __new__(cls, *args, **kwargs):
        super(cls, SpellCasting).__init__(*args, **kwargs)

        def get_spell_value(field, level):
            @property
            def spell_value(self):
                # method will eb renamed by setattr
                return getattr(self, field)[level]

        # add shortcut methods for retrieving
        for level in range(10):
            for field in ['known', 'slots']:
                if level == 0:
                    setattr(cls, "%s_cantrips" % field, get_spell_value(field, level))
                else:
                    setattr(cls, "%s_level_%s" % (field, level), get_spell_value(field, level))


class DamageType(models.Model):
    """Damage types that can be dealt to others"""

    name = models.CharField(max_length=64)
    desc = models.TextField(null=True, blank=True)


class MagicSchool(models.Model):
    """ the schools of magic"""

    name = models.CharField(max_length=64)
    desc = models.TextField(null=True, blank=True)


class Spell(models.Model):
    """spells characters can cast"""

    name = models.CharField(max_length=64, unique=True)
    desc = models.TextField(null=True, blank=True)
    higher_level = models.TextField(null=True, blank=True)
    page = models.CharField(max_length=32, null=True, blank=True)   # what book/page can you find it
    range = models.TextField(null=True, blank=True)
    components = ArrayField(models.CharField(max_length=32), null=True, blank=True)
    material = models.TextField(null=True, blank=True)
    ritual = models.BooleanField(default=False)
    duration = models.CharField(max_length=256, null=True, blank=True)
    concentration = models.CharField(max_length=256, null=True, blank=True)
    casting_time = models.CharField(max_length=128, null=True, blank=True)
    level = models.PositiveSmallIntegerField(null=True, blank=True)
    school = models.ForeignKey("core.MagicSchool", null=True, blank=True, on_delete=models.SET_NULL)


class Requirement(models.Model):
    """What requirements are needed to do a given thing"""

    ABILITY = ""
    SKILL = ""
    PROFICIENCY = ""

    type = models.CharField(max_length=64)
    value = models.SmallIntegerField()  # use 0 or 1 as booleans


class Equipment(models.Model):
    """equipment in dnd weapons/armors/transport etc"""

    name = models.CharField(max_length=256)
    type = models.CharField(max_length=64, null=True, blank=True)
    sub_type = models.CharField(max_length=64, null=True, blank=True)

    # proficiencies count as OR
    requirements = models.ManyToManyField("core.Requirement")

    # weapon specific
    range = models.CharField(max_length=128, null=True, blank=True)
    dice_count = models.PositiveSmallIntegerField(null=True)
    dice_value = models.PositiveSmallIntegerField(null=True)
    damage_type = models.ForeignKey("core.DamageType", null=True, blank=True, on_delete=models.SET_NULL)
    properties = ArrayField(models.CharField(max_length=32), null=True, blank=True)

    # armor specific
    bonus = models.SmallIntegerField(null=True, blank=True)
    dex_bonus = models.SmallIntegerField(null=True, blank=True)     # max
    stealth = models.NullBooleanField(default=None)     # True, None, False = advantage, normal, disadvantage

    # price is always set in copper and will be calculated to readable price
    price = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)     # in lb


class Condition(models.Model):
    """Conditions taht can be applied to characters/npcs/monsters etc"""

    name = models.CharField(max_length=64, unique=True)
    desc = models.TextField(null=True, blank=True)


class Language(models.Model):
    """ dnd languages and scripts """

    name = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=64, null=True, blank=True)
    script = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class Alignment(models.Model):
    """ ethical orientations"""

    obedience = models.CharField(max_length=16)
    alignment = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self.alignment == self.obedience:
            return "True %s" % self.alignment
        return "%s %s" % (self.obedience, self.alignment)


# class Klass(models.Model):
#     name = models.CharField(max_length=128, unique=True)
#     for_npcs = models.BooleanField(default=False)
#     for_players = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ['name', ]
#
#     def __str__(self):
#         return self.name
#
#
# class Race(models.Model):
#     name = models.CharField(max_length=128, unique=True)
#     size = models.ForeignKey('core.Size', null=True, on_delete=models.SET_NULL)
#     group = models.ForeignKey('core.Group', null=True, on_delete=models.SET_NULL)
#     languages = models.ManyToManyField('core.Language')
#
#     class Meta:
#         ordering = ['name', ]
#
#     def __str__(self):
#         return self.name
