# Generated by Django 4.1.7 on 2023-04-05 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyvaloration',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='propertyvaloration',
            name='valuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyAssessment', to='apis.student'),
        ),
        migrations.AlterField(
            model_name='uservaloration',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]