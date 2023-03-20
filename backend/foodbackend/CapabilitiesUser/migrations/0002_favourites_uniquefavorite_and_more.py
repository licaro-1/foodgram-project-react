# Generated by Django 4.1.7 on 2023-03-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CapabilitiesUser', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favourites',
            constraint=models.UniqueConstraint(fields=('author', 'recipe'), name='UniqueFavorite'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('author', 'recipe'), name='UniqueShoppingCart'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='UniqueSubscribtion'),
        ),
    ]
