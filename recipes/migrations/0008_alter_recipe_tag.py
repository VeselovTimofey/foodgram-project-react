# Generated by Django 3.2.3 on 2021-07-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20210716_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(related_name='recipe_tag', to='recipes.Tag'),
        ),
    ]
