# Generated by Django 2.0.2 on 2018-03-27 17:48

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.BooleanField()),
                ('strength', models.SmallIntegerField()),
                ('dexterity', models.SmallIntegerField()),
                ('constitution', models.SmallIntegerField()),
                ('wisdom', models.SmallIntegerField()),
                ('intelligence', models.SmallIntegerField()),
                ('charisma', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AbilityScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('short', models.CharField(blank=True, max_length=32, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obedience', models.CharField(max_length=16)),
                ('alignment', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DamageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(blank=True, max_length=64, null=True)),
                ('sub_type', models.CharField(blank=True, max_length=64, null=True)),
                ('range', models.CharField(blank=True, max_length=128, null=True)),
                ('dice_count', models.PositiveSmallIntegerField(null=True)),
                ('dice_value', models.PositiveSmallIntegerField(null=True)),
                ('properties', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), blank=True, null=True, size=None)),
                ('bonus', models.SmallIntegerField(blank=True, null=True)),
                ('dex_bonus', models.SmallIntegerField(blank=True, null=True)),
                ('stealth', models.NullBooleanField(default=None)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('weight', models.PositiveIntegerField(blank=True, null=True)),
                ('damage_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.DamageType')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('race', 'Race')], max_length=25)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Klass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('hit_die', models.PositiveSmallIntegerField()),
                ('choices', django.contrib.postgres.fields.jsonb.JSONField(default={})),
            ],
        ),
        migrations.CreateModel(
            name='KlassLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField()),
                ('ability_bonuses', models.SmallIntegerField(default=0)),
                ('prof_bonus', models.SmallIntegerField()),
                ('choices', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('features', models.ManyToManyField(to='core.Feature')),
                ('klass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Klass')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('type', models.CharField(blank=True, max_length=64, null=True)),
                ('script', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MagicSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.SmallIntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Surname')])),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='names', to='core.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Proficiency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('speed', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('alignment_desc', models.TextField(blank=True, null=True)),
                ('age_desc', models.TextField(blank=True, null=True)),
                ('size_desc', models.TextField(blank=True, null=True)),
                ('language_desc', models.TextField(blank=True, null=True)),
                ('choices', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('ability_bonus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Abilities')),
                ('languages', models.ManyToManyField(to='core.Language')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Race')),
                ('proficiencies', models.ManyToManyField(to='core.Proficiency')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64)),
                ('value', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('space', models.CharField(max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('ability_score', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.AbilityScore')),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('higher_level', models.TextField(blank=True, null=True)),
                ('page', models.CharField(blank=True, max_length=32, null=True)),
                ('range', models.TextField(blank=True, null=True)),
                ('components', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), blank=True, null=True, size=None)),
                ('material', models.TextField(blank=True, null=True)),
                ('ritual', models.BooleanField(default=False)),
                ('duration', models.CharField(blank=True, max_length=256, null=True)),
                ('concentration', models.CharField(blank=True, max_length=256, null=True)),
                ('casting_time', models.CharField(blank=True, max_length=128, null=True)),
                ('level', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.MagicSchool')),
            ],
        ),
        migrations.CreateModel(
            name='SpellCasting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('known', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), size=10)),
                ('slots', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), size=10)),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Size'),
        ),
        migrations.AddField(
            model_name='klasslevel',
            name='spell_casting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.SpellCasting'),
        ),
        migrations.AddField(
            model_name='klass',
            name='proficiencies',
            field=models.ManyToManyField(to='core.Proficiency'),
        ),
        migrations.AddField(
            model_name='klass',
            name='saving_throws',
            field=models.ManyToManyField(to='core.AbilityScore'),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together={('name', 'category')},
        ),
        migrations.AddField(
            model_name='equipment',
            name='requirements',
            field=models.ManyToManyField(to='core.Requirement'),
        ),
        migrations.AlterUniqueTogether(
            name='name',
            unique_together={('group', 'name', 'category')},
        ),
    ]
