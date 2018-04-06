from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




class Elementy(models.Model):
    background = models.ImageField(upload_to='media', blank=True, null=True)
    character1 = models.ImageField(upload_to='media', blank=True, null=True)
    character2 = models.ImageField(upload_to='media',blank=True, null=True)
    chat1 = models.ImageField(upload_to='media', blank=True, null=True)
    chat2= models.ImageField(upload_to='media', blank=True, null=True)
    text1 = models.CharField('Tekst dla pierwszej postaci', max_length = 100, default = " ", blank=True)
    text2 = models.CharField('Tekst dla drugiej postaci', max_length = 100, default = " ", blank=True)


class Comic(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    element = models.ForeignKey(Elementy, on_delete=models.CASCADE, null= True)
    comics = models.ImageField(upload_to='media')
    title = models.CharField('Tytul', max_length=50)
    created = models.DateTimeField('Data utworzenia', auto_now_add= True)
    publiczny = models.BooleanField(default=1)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'komiks' #nazwa obiektu w języku polski
        verbose_name_plural = u'komiksy'
        ordering = ['-created'] #od najnowszych

    def get_absolute_url(self):
        return reverse('home')



#class Profil(models.Model):
