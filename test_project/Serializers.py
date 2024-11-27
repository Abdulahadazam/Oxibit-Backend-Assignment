from rest_framework import serializers
from api.models import Users, Book, Review, BookAttributes, BookCategory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'password', 'role']






class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'publication_date', 'isbn','categories', 'created_by']





class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password', 'role']  
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating', 'review_text']



class BookAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAttributes
        fields = ['id', 'book', 'genre', 'language', 'number_of_pages']



class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ['id', 'name']