# Generated by Django 3.2.3 on 2021-09-19 22:05

from django.db import migrations, models

import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time_cooking',
            field=models.PositiveIntegerField(validators=[recipes.validators.value_must_not_be_null], verbose_name='recipe preparation time'),
        ),
    ]