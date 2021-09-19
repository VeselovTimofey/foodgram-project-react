# Generated by Django 3.2.3 on 2021-09-12 17:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='ingredient name')),
                ('unit', models.CharField(max_length=50, verbose_name='ingredient unit')),
            ],
            options={
                'verbose_name': 'ingredient',
                'verbose_name_plural': 'ingredients',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, validators=[recipes.validators.value_is_russia], verbose_name='recipe name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='recipe image')),
                ('description', models.TextField(verbose_name='recipe description')),
                ('time_cooking', models.PositiveIntegerField(validators=[recipes.validators.value_is_not_null], verbose_name='recipe preparation time')),
                ('slug', models.SlugField(max_length=75, unique=True, verbose_name='recipe slug')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='publication time of the recipe')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='recipe author')),
            ],
            options={
                'verbose_name': 'recipe',
                'verbose_name_plural': 'recipes',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='tag name')),
                ('color', models.CharField(default='orange', max_length=50, verbose_name='tag color')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who_are_subscribed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='who are subscribed to')),
                ('who_subscribes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_subscribes', to=settings.AUTH_USER_MODEL, verbose_name='who subscribe')),
            ],
            options={
                'verbose_name': 'subscribe',
                'verbose_name_plural': 'subscribes',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='ingredient amount')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_in_recipes', to='recipes.ingredient', verbose_name='this ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='recipes.recipe', verbose_name='recipe for this ingredient')),
            ],
            options={
                'verbose_name': 'unique ingredient in the recipe',
                'verbose_name_plural': 'unique ingredients in the recipe',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='recipe ingredients'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='recipe tags'),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchaser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to=settings.AUTH_USER_MODEL, verbose_name='purchaser')),
                ('purchases', models.ManyToManyField(related_name='purchases', to='recipes.Recipe', verbose_name='purchases')),
            ],
            options={
                'verbose_name': 'purchase',
                'verbose_name_plural': 'purchases',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='favorite recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='favorite user')),
            ],
            options={
                'verbose_name': 'favorite',
                'verbose_name_plural': 'favorites',
            },
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('who_subscribes', 'who_are_subscribed_to'), name='unique_subscribe'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite_user_recipe'),
        ),
    ]
