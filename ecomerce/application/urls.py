from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm

urlpatterns = [
    path('home/', views.home_page, name="home"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path("about/", views.about_page, name="about"),
    path("contact/", views.contact_page, name="contact"),
    path("profile/", views.ProfileView.as_view(), name="profile"),

    #registration authentication    
    path("registration/", views.CustomerRegistration.as_view(), name="registration",),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm), name='login'),
    path("logout", views.Logout, name="logout"),
    
    #wishlist  
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    #cart
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.Order_placed, name='order'),

    path('address/', views.Address, name='address'),





]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
