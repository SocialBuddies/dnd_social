from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from core.models import Klass, Race
from npcs.factories.npcs import NpcFactory
from core.models import Race, Klass, Alignment


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['pk', 'name']


class KlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = ['pk', 'name']


class AlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alignment
        fields = ['pk', 'name']
