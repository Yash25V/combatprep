from django.db import models
from django.conf import settings

class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SoldierProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    rank = models.CharField(max_length=50, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='soldiers')
    service_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    enlistment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.rank if self.rank else ''} {self.user.get_full_name()} - {self.service_number}"

class TrainingProgram(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    officer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_programs')
    assigned_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='training_programs')

    def __str__(self):
        return f"{self.name} ({self.date})"

class Assessment(models.Model):
    soldier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessments', limit_choices_to={'role': 'SOLDIER'})
    officer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='conducted_assessments')
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessments')
    date_recorded = models.DateField(auto_now_add=True)
    physical_fitness_score = models.IntegerField(help_text="Score out of 100")
    technical_skills_score = models.IntegerField(help_text="Score out of 100")
    training_score = models.IntegerField(help_text="Score out of 100")
    comments = models.TextField(blank=True, null=True)
    
    @property
    def readiness_score(self):
        return round((self.physical_fitness_score + self.technical_skills_score + self.training_score) / 3.0, 2)

    def __str__(self):
        return f"Assessment for {self.soldier.username} on {self.date_recorded}"

