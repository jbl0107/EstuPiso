# Generated by Django 4.1.7 on 2023-06-19 17:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('dni', models.CharField(max_length=9, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/')),
                ('isActive', models.BooleanField(default=True)),
                ('isAdministrator', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterestService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('direction', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('Salud', 'Health'), ('Alimentación', 'Feeding'), ('Deporte', 'Sport'), ('Entretenimiento', 'Entertainment'), ('Transporte', 'Transport'), ('Educación', 'Education')], default='-', max_length=20)),
            ],
            options={
                'unique_together': {('name', 'direction', 'type')},
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='properties/')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('apis.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('apis.user',),
        ),
        migrations.CreateModel(
            name='UserValoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('title', models.CharField(max_length=50)),
                ('review', models.CharField(max_length=1000)),
                ('date', models.DateField(auto_now_add=True)),
                ('valued', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluationsReceived', to=settings.AUTH_USER_MODEL)),
                ('valuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userRatings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('localization', models.CharField(max_length=100)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('type', models.CharField(choices=[('Inmueble completo', 'Property'), ('Habitacion', 'Room'), ('Cama', 'Bed')], default='-', max_length=20)),
                ('dormitories', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('size', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('baths', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('photos', models.ManyToManyField(to='apis.photo')),
                ('rules', models.ManyToManyField(blank=True, related_name='rules', to='apis.rule')),
                ('services', models.ManyToManyField(blank=True, to='apis.service')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='apis.owner')),
            ],
            options={
                'verbose_name_plural': 'Properties',
                'unique_together': {('localization', 'type', 'price', 'size')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('userRecipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receivedMessagesU', to=settings.AUTH_USER_MODEL)),
                ('userSender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentMessagesU', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnnouncement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='studentsAnnouncement/')),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('pet', models.BooleanField()),
                ('smoker', models.BooleanField()),
                ('flatSocialize', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('goOut', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('invitationFrecuency', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('bathCleaningFrecuency', models.CharField(choices=[('Una vez por semana', 'Onceaweek'), ('Dos veces por semana', 'Twiceaweek'), ('Varias veces por semana', 'Manytimesperweek'), ('Todos los días', 'Everyday')], default='-', max_length=26)),
                ('kitchenCleaningFrecuency', models.CharField(choices=[('Una vez por semana', 'Onceaweek'), ('Dos veces por semana', 'Twiceaweek'), ('Varias veces por semana', 'Manytimesperweek'), ('Todos los días', 'Everyday')], default='-', max_length=26)),
                ('gender', models.CharField(choices=[('Masculino', 'Male'), ('Femenino', 'Female'), ('Otro', 'Other'), ('Cualquiera', 'Any')], default='-', max_length=11)),
                ('wantedGender', models.CharField(choices=[('Masculino', 'Male'), ('Femenino', 'Female'), ('Otro', 'Other'), ('Cualquiera', 'Any')], default='-', max_length=11)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='apis.student')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyValoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('title', models.CharField(max_length=50)),
                ('review', models.CharField(max_length=1000)),
                ('date', models.DateField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyRatings', to='apis.property')),
                ('valuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyAssessment', to='apis.student')),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos_for_properties', to='apis.owner'),
        ),
        migrations.CreateModel(
            name='InterestServiceProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.CharField(max_length=15)),
                ('busTime', models.CharField(max_length=20)),
                ('carTime', models.CharField(max_length=20)),
                ('walkTime', models.CharField(max_length=20)),
                ('interestService', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.interestservice')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apis.property')),
            ],
            options={
                'unique_together': {('distance', 'busTime', 'carTime', 'walkTime', 'interestService', 'property')},
            },
        ),
        migrations.CreateModel(
            name='GroupReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(validators=[django.core.validators.MinValueValidator(2)])),
                ('destination', models.CharField(max_length=50)),
                ('budget', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('duration', models.CharField(max_length=30)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='groupReservationAssigned', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupReservationStudent', to='apis.student')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('content', models.TextField()),
                ('place', models.CharField(max_length=30)),
                ('culture', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('transport', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('prices', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('gastronomy', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('leisure', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('turism', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentExperiences', to='apis.student')),
            ],
            options={
                'unique_together': {('place', 'student')},
            },
        ),
    ]
