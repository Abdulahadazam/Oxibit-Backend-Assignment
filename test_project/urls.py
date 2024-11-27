from django.contrib import admin
from django.urls import path
from api.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Books Management
    path('listrole/', list_roles),
    path('getbooks/', getBooks),
    path('getbookdetails/<int:book_id>', getBookDetail),
    path('createbook/', createBook),
    path('updatebook/<int:book_id>', updateBook),
    path('deletebook/<int:book_id>', deleteBook),

    # User Role Management
    path('api/roles', createRole),
    path('api/roles/<int:role_id>', deleteRole),

    # User Management
    path('api/users', getUsers),
    # path('api/users', createUser),
    path('api/users/<int:user_id>', updateUser),
    path('api/users/<int:user_id>', deleteUser),

    # Categories Management
    path('api/categories', getCategories),
    path('api/categories', createCategory),
    path('api/categories/<int:category_id>', updateCategory),
    path('api/categories/<int:category_id>', deleteCategory),

    # Reviews Management
    path('api/reviews', createReview),
    path('api/reviews/<int:review_id>', getReview),
    path('api/reviews/<int:review_id>', updateReview),
    path('api/reviews/<int:review_id>', deleteReview),

    # Authentication
    path('auth/signup/', auth_signup_view),
    path('auth/login/', auth_login_view),
    path('auth/logout/', auth_logout_view),
    # path('auth/verify/<str:token>/', auth_verify_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
