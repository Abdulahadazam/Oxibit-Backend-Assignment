
from django.contrib import admin
from .models import Users,Book,Review,BookAttributes,BookCategory

admin.site.register(Users)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(BookAttributes)
admin.site.register(BookCategory)