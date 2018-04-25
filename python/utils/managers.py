from django.db import models
from django.db.models.aggregates import Count
from random import randint


class RandomChoiceQueryset(models.QuerySet):
    def random(self):
        # way faster method than order_by("?").first()
        count = self.aggregate(count=Count('id'))['count']
        if count == 0:
            return

        random_index = randint(0, count - 1) if count > 1 else 0
        return self[random_index]


class RandomChoiceManager(models.Manager):
    def get_queryset(self):
        return RandomChoiceQueryset(self.model, using=self._db)

    def random(self):
        # way faster method than order_by("?").first()
        count = self.aggregate(count=Count('id'))['count']
        if count == 0:
            return

        random_index = randint(0, count - 1) if count > 1 else 0
        return super().get_queryset()[random_index]
