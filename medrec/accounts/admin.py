from django.contrib import admin
from django.contrib.auth.models import User

# Registering the default User model is optional; admin is enabled by default
admin.site.unregister(User)
admin.site.register(User)
