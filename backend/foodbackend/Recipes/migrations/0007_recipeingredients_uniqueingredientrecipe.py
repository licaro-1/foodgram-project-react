# Generated by Django 4.1.7 on 2023-03-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes', '0006_alter_recipeingredients_ingredient_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='UniqueIngredientRecipe'),
        ),
    ]
