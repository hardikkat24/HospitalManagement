from django.contrib import admin
from .models import Profile, Appointment, Prescription, Invoice, Contact

admin.site.register(Profile)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Invoice)
admin.site.register(Contact)
