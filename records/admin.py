from django.contrib import admin
from .models import SoldierProfile, Assessment, Unit, TrainingProgram

admin.site.register(Unit)
admin.site.register(TrainingProgram)
admin.site.register(SoldierProfile)
admin.site.register(Assessment)
