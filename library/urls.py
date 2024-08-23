from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.available_books, name='available_books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/review/', views.add_review, name='add_review'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<int:book_id>/success/', views.successful_borrow, name='successful_borrow'),
    
    path('profile/', views.profile, name='profile'),
    path('subscription/', views.subscription_details, name='subscription_details'),
    path('subscription/renew/', views.renew_subscription, name='renew_subscription'),
    path('subscription/new/', views.new_subscription, name='new_subscription'),
    path('subscription/process/', views.renew_subscription, name='process_subscription'),
    
    path('creative-works/', views.creative_works, name='creative_works'),
    path('creative-works/<int:pk>/', views.creative_work_detail, name='creative_work_detail'),
    path('creative-works/add/', views.add_creative_work, name='add_creative_work'),
    path('creative-works/<int:pk>/like/', views.like_creative_work, name='like_creative_work'),
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
