# Generated by Django 4.1.7 on 2023-04-03 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_alter_rule_name_alter_service_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name_plural': 'Properties'},
        ),
        migrations.AlterUniqueTogether(
            name='property',
            unique_together={('localization', 'type', 'price', 'size')},
        ),
    ]
