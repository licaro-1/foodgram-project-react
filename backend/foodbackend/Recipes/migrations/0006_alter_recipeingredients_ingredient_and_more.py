# Generated by Django 4.1.7 on 2023-03-20 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes', '0005_alter_recipeingredients_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='Recipes.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='Recipes.recipe'),
        ),
    ]
