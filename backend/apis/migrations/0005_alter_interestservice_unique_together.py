# Generated by Django 4.1.7 on 2023-04-05 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_alter_interestservice_direction_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='interestservice',
            unique_together={('name', 'direction', 'type')},
        ),
    ]