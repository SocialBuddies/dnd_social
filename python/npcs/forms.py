from django import forms
from taggit.models import TaggedItem

from npcs.models import Npc
from npcs.factories.npcs import NpcFactory


class CreateNpcForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=TaggedItem.objects.all().order_by('tag').values_list("tag__name").distinct())
    # build autocomplete later
    # base = forms.ModelChoiceField(
    #     queryset=NpcDescription.objects.filter(category="base"),
    #     widget=autocomplete.ModelSelect2(url='npcs_api:autocomplete_npc_description')
    # )
    # base = forms.CharField(max_length=200, required=False)
    # body = forms.CharField(max_length=200, required=False)
    # conflict_physical = forms.CharField(max_length=200, required=False)
    # conflict_verbal = forms.CharField(max_length=200, required=False)
    # disability = forms.CharField(max_length=200, required=False)
    # expression = forms.CharField(max_length=200, required=False)
    # face = forms.CharField(max_length=200, required=False)
    # hair = forms.CharField(max_length=200, required=False)
    # mark = forms.CharField(max_length=200, required=False)
    # other = forms.CharField(max_length=200, required=False)
    # personality_quirks = forms.CharField(max_length=200, required=False)
    # physical_skills = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Npc
        fields = ['name', 'surname', 'gender', 'attributes', 'race', 'klass', 'level', 'alignment', ]

    def save(self, commit=True):
        factory = NpcFactory()
        npc = factory.randomize(super().save(commit=False))
        if commit:
            npc.save()
        return npc
