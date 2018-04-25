import random

from django.db.models import Count
from django.db.models.query import QuerySet
from taggit.managers import _TaggableManager


class FieldRandomizer(object):
    """
    This can sett custom random choices
    When using this class, methods called <field>_choices will be set into a method calls get_<field>
    Only initialising it once.
    You can overwrite these method returns by setting <field>_choices in kwargs as a list
    And it will pick a random result from those

    Other kwargs get set to self.kwargs, so it can be used within the default methods to adjust choices

    example:
    class SomeRandomizer(FieldRandomizer):
        def some_choices(self):
            return [1, 2, 3, 4, ]

    randomizer = SomeRandomizer()
    randomizer.get_some()
    > 2
    randomizer = SomeRandomizer(some_choices=[6, 7, 8, ])
    randomizer.get_some()
    > 7
    """

    FIELDS = []

    def __init__(self, *args, **kwargs):
        if not self.FIELDS:
            raise Exception("FIELDS is required to know what methods to set")

        self.tags = kwargs.pop("tags", [])
        self.kwargs = kwargs

        # set get_field methods
        for field in self.FIELDS:
            f_choices = field + "_choices"
            try:
                if f_choices in kwargs:
                    choices = kwargs[f_choices]
                elif hasattr(self, "get_%s" % field):
                    continue
                else:
                    choices = getattr(self, f_choices)()

                setattr(self, "get_%s" % field, self.random_choice(choices, field))
            except AttributeError:
                raise Exception("FIELD(%s) is set but there is no method named %s" % (field, f_choices))

    @staticmethod
    def model_has_tags(queryset):
        return hasattr(queryset.model, 'tags') and isinstance(queryset.model.tags, _TaggableManager)

    def random_qs_choice(self, qs):
        count = qs.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return qs[random_index]

    def random_choice(self, choices, field):
        """
        Returns a random choice basted in input choices.
        If choices is a queryset, check if tags are passed and model has tags field.
        If so, use extra filter on queryset, if no objects are left, random from original queryset
        if original queryset has no objects, return random choice from all model instance (model.objects.all())
        :param choices: list or queryset to random a choice from
        :param field: field that is being randomised
        :return: a single choice
        """

        qs, count = choices, 0
        if isinstance(choices, QuerySet):
            if self.tags and self.model_has_tags(choices):
                qs = choices.filter(tags__name__in=self.tags)

                # make sure new qs, or even original has at least 1 result
                if not qs.exists():
                    if not choices.exists():
                        # no initial choices, resetting to all to make sure generator doesnt crash
                        qs = qs.model.objects.all()
                    else:
                        qs = choices

            # get ids list and apply weight
            pks = qs.values_list("pk", flat=True)
            if field + "_weight" in self.kwargs:
                # apply weight
                for pk, weight in self.kwargs[field + "_weight"].items():
                    if pk in pks:
                        pks += [pk] * weight

        def _func():
            try:
                if isinstance(choices, QuerySet):
                    return qs.get(pk=random.choice(pks))
                else:
                    return random.choice(choices)
            except Exception as exc:
                print(exc)
                import pdb
                pdb.set_trace()
        return _func

    def randomize(self, instance, commit=True):
        # add non set fields
        for field in self.FIELDS:
            if not getattr(instance, field):
                setattr(instance, field, getattr(self, "get_%s" % field)())

        if commit:
            instance.save()
        return instance


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
