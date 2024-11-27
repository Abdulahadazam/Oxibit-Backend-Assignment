from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class Users(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('reader', 'Reader'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')

class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    categories = models.ManyToManyField(BookCategory, related_name="books")
    created_by = models.ForeignKey(Users, related_name='managed_books', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}"


class BookAttributes(models.Model):
    book = models.OneToOneField(Book, related_name='attributes', on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    number_of_pages = models.IntegerField()

    def __str__(self):
        return f"{self.book.title} Attributes"



# class BookCategoryRelation(models.Model):
#     book = models.ForeignKey(Book, related_name='categories', on_delete=models.CASCADE)
#     category = models.ForeignKey(BookCategory, related_name='books', on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ['book', 'category']

#     def __str__(self):
#         return f"{self.book.title} - {self.category.name}"
