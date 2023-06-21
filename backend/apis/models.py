from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re



class UserManager(BaseUserManager):

    def create_user(self, dni, name, surname, username, email, telephone, photo, password=None):
        if not email:
            raise ValueError('The user must have an email')

        user = self.model(
            dni=dni,
            name=name,
            surname=surname,
            username=username,
            email=self.normalize_email(email),
            telephone=telephone,
            photo=photo

        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, dni, name, surname, username, email, telephone, photo, password):
        user = self.create_user(
            dni=dni,
            name=name,
            surname=surname,
            username=username,
            email=self.normalize_email(email),
            telephone=telephone,
            photo=photo,
            password=password
        )

        user.isAdministrator = True
        user.save()
        return user
    
    


class User(AbstractBaseUser):
    dni = models.CharField(max_length=9, null=False, blank=False, unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    telephone = PhoneNumberField(null = False, blank = False)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    isActive = models.BooleanField(default=True)
    isAdministrator = models.BooleanField(default=False)

    
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'surname', 'dni', 'telephone', 'photo']

    def __str__(self):
        return f'{self.name} {self.surname}, con username: {self.username}'
    
    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if len(self.password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres')
            
        nif_regex = re.compile(r'^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$', re.IGNORECASE)
        nie_regex = re.compile(r'^[XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$', re.IGNORECASE)
        if not nif_regex.match(self.dni) and not nie_regex.match(self.dni):
            raise ValidationError('El formato del DNI no es válido')
    
    @property
    def is_staff(self):
        return self.isAdministrator




class Student(User):

    def __str__(self):
        return self.username



class Owner(User):

    def __str__(self):
        return self.username
    

    
class PropertyType(models.TextChoices):
    PROPERTY = "Inmueble completo"
    ROOM = "Habitacion"
    BED = "Cama"



class Rule(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    
    def __str__(self):
        return self.name
    


class Photo(models.Model):
    photo = models.ImageField(upload_to='properties/', null=False, blank=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=False, blank=False, related_name="photos_for_properties")

    def __str__(self):
        return f'El propietario de esta foto es: {self.owner}'
    




class Service(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
    


# ManyToMany crea la tabla PhotoXProperty automaticamente
class Property(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    localization = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    type = models.CharField(max_length=20 ,choices=PropertyType.choices, default="-", null=False)
    dormitories = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    size = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    baths = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=False, related_name='properties')
    rules = models.ManyToManyField(Rule, blank=True, related_name='rules')
    photos = models.ManyToManyField(Photo, blank=False)
    services = models.ManyToManyField(Service, blank=True)

    class Meta:
        unique_together = ('localization', 'type', 'price', 'size')
        verbose_name_plural = "Properties"
    
    def __str__(self):
        return f'{self.title}. (Owner: {self.owner})'
    

    

#Related_name sirve para poner nombre a la relacion inversa. Por ejemplo, podria acceder a todos los mensajes enviados por
# un user concreto de la siguiente forma: admin.sentMessagesU.all() 
class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    userSender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentMessagesU',null=False, blank=False)
    userRecipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivedMessagesU', null=False, blank=False)

    def __str__(self):
        return self.content



class UserValoration(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    title = models.CharField(max_length=50, null=False)
    review = models.CharField(max_length=1000, null=False)
    date = models.DateField(auto_now_add=True ,null=False, blank=False)
    valuer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='userRatings')
    valued = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='evaluationsReceived')

    def __str__(self):
        return f'{self.title}. Puntuación: {str(self.value)}'



class PropertyValoration(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    title = models.CharField(max_length=50, null=False)
    review = models.CharField(max_length=1000, null=False)
    date = models.DateField(auto_now_add=True ,null=False, blank=False)
    valuer = models.ForeignKey(Student, on_delete=models.CASCADE, null=False, related_name='propertyAssessment')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=False, related_name='propertyRatings')

    def __str__(self):
        return f'{self.title}. Puntuación: {str(self.value)}'
    


# on_delete = cascade --> si borro un student, se borran todas sus reservas grupales.
# admin es un user que debe tener isAdministrator = True
class GroupReservation(models.Model):
    size = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(2)])
    destination = models.CharField(max_length=50 ,blank=False, null=False)
    budget = models.IntegerField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    duration = models.CharField(max_length=30, blank=False, null=False)
    student = models.ForeignKey(Student, null=False, on_delete=models.CASCADE, related_name="groupReservationStudent")
    admin = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="groupReservationAssigned") 

    def __str__(self):
        return self.student.username


class Experience(models.Model):
    date = models.DateField(auto_now_add=True ,null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    place = models.CharField(max_length=30, null=False, blank=False)
    culture = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    transport = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    prices = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    gastronomy = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    leisure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    turism = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False, related_name="studentExperiences")

    class Meta:
        unique_together = ('place', 'student')

    def __str__(self):
        return self.content
    


class InterestServiceType(models.TextChoices):
    HEALTH = "Salud"
    FEEDING = "Alimentación"
    SPORT = "Deporte"
    ENTERTAINMENT = "Entretenimiento"
    TRANSPORT = "Transporte"
    EDUCATION = "Educación"


class InterestService(models.Model):
    name = models.CharField(max_length=70, null=False, blank=False)
    direction = models.CharField(max_length=200, null=False, blank=False)
    type = models.CharField(max_length=20 ,choices=InterestServiceType.choices, default="-", null=False)

    class Meta:
        unique_together = ('name', 'direction', 'type')


    def __str__(self):
        return f'{self.name}. Type: {self.type}'


class InterestServiceProperty(models.Model):
    distance = models.CharField(max_length=15 ,null=False, blank=False)
    busTime = models.CharField(max_length=20, null=False, blank=False)
    carTime = models.CharField(max_length=20 ,null=False, blank=False)
    walkTime = models.CharField(max_length=20, null=False, blank=False)
    interestService = models.ForeignKey(InterestService, on_delete=models.CASCADE, null=False)
    property = models.ForeignKey(Property, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('distance', 'busTime', 'carTime', 'walkTime', 'interestService', 'property')

    def __str__(self):
        return f'Property: {self.property}. Servicio de interés: {self.interestService}'


class CleaningFrecuency(models.TextChoices):
    ONCEAWEEK = "Una vez por semana"
    TWICEAWEEK = "Dos veces por semana"
    MANYTIMESPERWEEK = "Varias veces por semana"
    EVERYDAY = "Todos los días"


class Gender(models.TextChoices):
    MALE = "Masculino"
    FEMALE = "Femenino"
    OTHER = "Otro"
    ANY = "Cualquiera"


class StudentAnnouncement(models.Model):
    description = models.TextField(null=False, blank=False)
    photo = models.ImageField(upload_to='studentsAnnouncement/', null=True, blank=True)
    age = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    pet = models.BooleanField(null=False)
    smoker = models.BooleanField(null=False)
    flatSocialize = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    goOut = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    invitationFrecuency = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    bathCleaningFrecuency = models.CharField(max_length=26 ,choices=CleaningFrecuency.choices, default="-", null=False)
    kitchenCleaningFrecuency = models.CharField(max_length=26 ,choices=CleaningFrecuency.choices, default="-", null=False)
    gender = models.CharField(max_length=11 ,choices=Gender.choices, default="-", null=False)
    wantedGender = models.CharField(max_length=11 ,choices=Gender.choices, default="-", null=False)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'Student: {self.student}'
