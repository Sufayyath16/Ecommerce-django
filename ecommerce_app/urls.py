from django.urls import path
from.import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact,name='contact'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    
    
    path('product2/',views.product2,name='product2'),
    path('single/',views.single,name='single'),
    path('single2/',views.single2,name='single2'),
    
]
