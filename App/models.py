from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class korisnici(AbstractUser):
    ROLES = (('men','mentor'),('stu','student'))
    STATUS = (('none', 'None'), ('izv', 'Izvanredni'), ('red', 'Redovni'))
    role = models.CharField(max_length=50,choices=ROLES)
    status = models.CharField(max_length=50,choices=STATUS)

class predmeti(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name = models.CharField(max_length=255)
    kod = models.CharField(max_length=16)
    program = models.TextField()
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50,choices=IZBORNI)
    def __str__(self):
        return '%s, Kod: %s, Program: %s, ECTS: %s, Sem_red: %s, Sem_izv: %s, Izborni: %s' % (self.name, self.kod
        ,self.program,self.ects,self.sem_red,self.sem_izv,self.izborni)


class upisi(models.Model):
    student_id = models.ForeignKey(korisnici,on_delete=models.CASCADE, blank=True,null=True)
    predmet_id = models.ForeignKey(predmeti,on_delete=models.CASCADE, blank=True,null=True)
    status = models.CharField(max_length=64)




