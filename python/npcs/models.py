from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

from core.models import Name
from utils.managers import RandomChoiceManager


class NpcRace(models.Model):
    name = models.CharField(max_length=64, unique=True)
    group = models.ForeignKey("core.Group", null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey("core.Size", null=True, blank=True, on_delete=models.SET_NULL)
    languages = models.ManyToManyField("core.Language")

    tags = TaggableManager()

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class NpcKlass(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)
    hit_die = models.PositiveSmallIntegerField(null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class NpcAttributes(models.Model):
    rpg_tinker = models.CharField(max_length=64, unique=True)
    values = ArrayField(models.PositiveSmallIntegerField(), size=6, null=True, blank=True)

    tags = TaggableManager()

    class Meta:
        ordering = ['-pk', ]

    def __str__(self):
        return self.rpg_tinker


class NpcDescription(models.Model):
    BASE = 'base'
    BODY = 'body'
    CONFLICT_PHYSICAL = 'conflict_physical'
    CONFLICT_VERBAL = 'conflict_verbal'
    DISABILITY = 'disability'
    EXPRESSION = 'expression'
    FACE = 'face'
    HAIR = 'hair'
    MARK = 'mark'
    OTHER = 'other'
    PERSONALITY_QUIRKS = 'personality_quirks'
    PHYSICAL_SKILLS = 'physical_skills'
    CATEGORIES = (
        (BASE, 'Base'),
        (BODY, 'Body'),
        (FACE, 'Face'),
        (HAIR, 'Hair'),
        (MARK, 'Mark'),
        (OTHER, 'Other'),
        (DISABILITY, 'Disability'),
        (EXPRESSION, 'Expression'),
        (PERSONALITY_QUIRKS, 'Personality Quirks'),
        (PHYSICAL_SKILLS, 'Physical Skills'),
        (CONFLICT_PHYSICAL, 'Conflict Style Physical'),
        (CONFLICT_VERBAL, 'Conflict Style Verbal'),
    )
    text = models.TextField(unique=True)
    category = models.CharField(max_length=32, choices=CATEGORIES)

    objects = RandomChoiceManager()

    class Meta:
        ordering = ['text', ]

    def __str__(self):
        return self.text


class Npc(models.Model):
    """Non playing character and its descriptions"""

    users = models.ManyToManyField(get_user_model(), through="npcs.UserNpcs")
    locked = models.BooleanField(default=False)

    # character stats
    alive = models.BooleanField(default=True)
    race = models.ForeignKey('npcs.NpcRace', null=True, blank=True, on_delete=models.SET_NULL)
    klass = models.ForeignKey('npcs.NpcKlass', null=True, blank=True, on_delete=models.SET_NULL)
    alignment = models.ForeignKey("core.Alignment", null=True, blank=True, on_delete=models.SET_NULL)
    level = models.PositiveSmallIntegerField(null=True, blank=True)
    attributes = models.ForeignKey("npcs.NpcAttributes", null=True, blank=True, on_delete=models.SET_NULL)
    sheet = models.TextField(null=True)

    # looks
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    gender = models.IntegerField(choices=Name.GENDERS, null=True, blank=True)
    descriptions = models.ManyToManyField("npcs.NpcDescription")

    tags = TaggableManager()

    def __str__(self):
        return self.name

    @property
    def description(self):
        # used by serializer to organise description manytomany
        data = []
        des_qs = self.descriptions.all()
        for category, display in NpcDescription.CATEGORIES:
            values = des_qs.filter(category=category).values("pk", "text")
            data.append({"category": category, "display": display, "values": values})
        return data


class UserNpcs(models.Model):
    npc = models.ForeignKey("npcs.Npc", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # why are they related
    owner = models.BooleanField(default=False)      # if nto owner its user
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
