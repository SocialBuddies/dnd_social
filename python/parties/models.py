from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Party(models.Model):
    """ Parties are groups of users where there is a role difference between game masters and players """

    name = models.CharField(max_length=64)
    game_masters = models.ManyToManyField("users.User", related_name="gm_parties")
    players = models.ManyToManyField("users.User", related_name="player_parties")

    def __str__(self):
        return self.name


class Handout(models.Model):
    """
    Link objects to players in a party. Users in received have access to the handout
    any game master from the party can handout and change who has access 
    """

    NPC = 1
    ITEM = 2
    TEXT = 3
    CATEGORIES = (
        (NPC, "NPC"),
        (ITEM, "Item"),
        (TEXT, "Text"),
    )
    category = models.PositiveSmallIntegerField()
    party = models.ForeignKey("parties.Party", related_name="handouts")
    received = models.ManyToManyField("users.User", related_name="player_parties")

    # relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
