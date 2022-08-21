from django.contrib import admin
from .models import Position, Candidate, Voter, Votes

# Register your models here.

admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Voter)
admin.site.register(Votes)
