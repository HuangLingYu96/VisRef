from django.contrib import admin
from .models import Ref
from .models import Cit
from .models import Sum

# Register your models here.
admin.site.register(Ref)
admin.site.register(Cit)
admin.site.register(Sum)
