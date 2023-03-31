from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator



class User(AbstractBaseUser):
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=30, blank=False, null=False)
    telephone = PhoneNumberField(null = False, blank = False)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    isActive = models.BooleanField(default=True)



class Admin(AbstractBaseUser):
    dni = models.CharField(max_length=9, null=False, blank=False, unique=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    password = models.CharField(max_length=30, blank=False, null=False)
    

    def __str__(self):
        return self.name + self.surname
    
    

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
    name = models.CharField(max_length=35, null=False)




class Photo(models.Model):
    photo = models.ImageField(upload_to='properties/', null=False, blank=False)


class Service(models.Model):
    name = models.CharField(max_length=35, null=False)



# ManyToMany crea la tabla PhotoXProperty automaticamente
class Property(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    localization = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    type = models.CharField(max_length=20 ,choices=PropertyType.choices, default="-", null=False)
    dormitories = models.IntegerField(null=False)
    size = models.IntegerField(null=False)
    baths = models.IntegerField(null=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=False)
    rules = models.ManyToManyField(Rule, blank=True)
    photos = models.ManyToManyField(Photo, blank=False)
    services = models.ManyToManyField(Service, blank=True)

    

#Related_name sirve para poner nombre a la relacion inversa. Por ejemplo, podria acceder a todos los mensajes enviados por
# un admin concreto de la siguiente forma: admin.mensajesEnviadosA.all() 
class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    userSender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentMessagesU',null=True, blank=True)
    userRecipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivedMessagesU', null=True, blank=True)
    adminSender = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='sentMessagesA', null=True, blank=True)
    adminRecipient = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='receivedMessagesA',null=True, blank=True)




class UserValoration(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    title = models.CharField(max_length=25, null=False)
    review = models.CharField(max_length=1000, null=False)
    date = models.DateField(auto_now_add=True ,null=False, blank=False)
    valuer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='userRatings')
    valued = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='evaluationsReceived')




class PropertyValoration(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    title = models.CharField(max_length=25, null=False)
    review = models.CharField(max_length=1000, null=False)
    date = models.DateField(auto_now_add=True ,null=False, blank=False)
    valuer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='propertyAssessment')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=False, related_name='propertyRatings')



# on_delete = cascade --> si borro un student, se borran todas sus reservas grupales.
class GroupReservation(models.Model):
    size = models.IntegerField(blank=False, null=False)
    destination = models.CharField(max_length=50 ,blank=False, null=False)
    budget = models.IntegerField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    duration = models.CharField(max_length=30, blank=False, null=False)
    student = models.ForeignKey(Student, null=False, on_delete=models.CASCADE, related_name="groupReservationStudent")
    admin = models.ForeignKey(Admin, null=False, on_delete=models.DO_NOTHING, related_name="groupReservationAssigned") 



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



class InterestServiceType(models.TextChoices):
    HEALTH = "Salud"
    FEEDING = "Alimentación"
    SPORT = "Deporte"
    ENTERTAINMENT = "Entretenimiento"
    TRANSPORT = "Transporte"
    EDUCATION = "Educación"


class InterestService(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    direction = models.CharField(max_length=150, null=False, blank=False)
    type = models.CharField(max_length=17 ,choices=InterestServiceType.choices, default="-", null=False)


class InterestServiceProperty(models.Model):
    distance = models.CharField(max_length=7 ,null=False, blank=False)
    busTime = models.CharField(max_length=20, null=False, blank=False)
    carTime = models.CharField(max_length=20 ,null=False, blank=False)
    walkTime = models.CharField(max_length=20, null=False, blank=False)
    interestService = models.ForeignKey(InterestService, on_delete=models.CASCADE, null=False)
    property = models.ForeignKey(Property, null=False, on_delete=models.CASCADE)



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
    photo = models.ImageField(upload_to='studentsAnnouncement/', null=False, blank=False)
    age = models.IntegerField(null=False)
    pet = models.BooleanField()
    smoker = models.BooleanField()
    flatSocialize = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    goOut = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    invitationFrecuency = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    bathCleaningFrecuency = models.CharField(max_length=26 ,choices=CleaningFrecuency.choices, default="-", null=False)
    kitchenCleaningFrecuency = models.CharField(max_length=26 ,choices=CleaningFrecuency.choices, default="-", null=False)
    gender = models.CharField(max_length=11 ,choices=Gender.choices, default="-", null=False)
    wantedGender = models.CharField(max_length=11 ,choices=Gender.choices, default="-", null=False)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=False)
