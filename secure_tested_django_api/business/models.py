from multiprocessing import managers
from pyexpat import model
from tabnanny import verbose
from time import time
from turtle import title
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class PublishedManager(models.Manager):   # Customer.objects.filter(status='published')
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Customer(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Bisexual')
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    TITLE_CHOICES = (
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('miss', 'Miss.'),
        ('dr', 'Dr.'),
        ('sir', 'Sir.'),
        ('ms', 'Ms.')
    )

    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default='mr')
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.PROTECT, default=1)
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    # implement custom managers

    # Customer.objects.all()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return "{} {}".format(self.name, self.last_name)


    

