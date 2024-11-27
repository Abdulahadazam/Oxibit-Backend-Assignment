from django.shortcuts import render
from api.models import *
from test_project.Serializers import UsersSerializer,BookSerializer,ReviewSerializer,BookAttributesSerializer,BookCategorySerializer,UserSignUpSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token



@api_view(["POST"])
@permission_classes([AllowAny])
def auth_signup_view(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        role = request.data.get("role", "reader")  

        
        if Users.objects.filter(email=email).exists():
            return Response({"error": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)

        
        user = Users.objects.create_user(
            username=email,  # Using email as username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True,  
        )

        
        return Response(
            {"message": "Signup successful. You can now log in."},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
def auth_login_view(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)  
                csrf_token = get_token(request)

                session_id = request.session.session_key

                return Response(
                    {
                        "message": "Login successful",
                        "role": user.role,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "csrf_token": csrf_token,  
                        "sessionid": session_id,  
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "User account is inactive"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def auth_logout_view(request):
    try:
        logout(request)  

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_roles(request):
    roles = Users.ROLE_CHOICES
    return Response({"roles": roles}, status=status.HTTP_200_OK)

# books apis 
# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def getBooks(request):
#     print('hum andar hai')
#     books = Book.objects.all()
#     if books.exists():
#         return Response(BookSerializer(books, many=True).data, status=status.HTTP_200_OK)
#     else:
#         return Response({"error": "No books found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBookDetail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return Response(BookSerializer(book).data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createBook(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateBook(request, book_id):
    print(book_id)
    book = get_object_or_404(Book, id=book_id)
    serializer = BookSerializer(book, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# POST /api/roles
@api_view(['POST'])
@permission_classes([IsAdminUser])  # Admin-only access
def createRole(request):
    role_name = request.data.get("role")
    if role_name in [choice[0] for choice in Users.ROLE_CHOICES]:
        return Response({"error": "Role already exists"}, status=status.HTTP_400_BAD_REQUEST)
    Users.ROLE_CHOICES.append((role_name, role_name.capitalize()))
    return Response({"message": "Role created successfully"}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAdminUser]) 
def deleteRole(request, role_id):
    roles = Users.ROLE_CHOICES
    for idx, role in enumerate(roles):
        if idx == role_id:
            Users.ROLE_CHOICES.pop(idx)
            return Response({"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAdminUser])  
def getUsers(request):
    users = Users.objects.all()
    return Response(UsersSerializer(users, many=True).data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def createUser(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    serializer = UsersSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])  
def deleteUser(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCategories(request):
    categories = BookCategory.objects.all()
    serializer = BookCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])  # Admin-only access
def createCategory(request):
    serializer = BookCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUT /api/categories/{category_id}
@api_view(['PUT'])
@permission_classes([IsAdminUser])  # Admin-only access
def updateCategory(request, category_id):
    category = get_object_or_404(BookCategory, id=category_id)
    serializer = BookCategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])  # Admin-only access
def deleteCategory(request, category_id):
    category = get_object_or_404(BookCategory, id=category_id)
    category.delete()
    return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createReview(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReview(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    serializer = ReviewSerializer(review)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAdminUser])  
def updateReview(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])  
def deleteReview(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def getBooks(request):
    books = Book.objects.all()
    if books.exists():
        book_data = []
        for book in books:
            reviews = book.reviews.all()  
            serialized_reviews = [
                {
                    "user": review.user.username,
                    "rating": review.rating,
                    "review_text": review.review_text,
                }
                for review in reviews
            ]
            book_data.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "description": book.description,
                    "publication_date": book.publication_date,
                    "isbn": book.isbn,
                    "categories": [category.name for category in book.categories.all()],
                    "created_by": book.created_by.username if book.created_by else None,
                    "reviews": serialized_reviews,
                    "image": book.image.url if book.image else None,  # Include image URL
                }
            )
        return Response(book_data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No books found"}, status=status.HTTP_404_NOT_FOUND)