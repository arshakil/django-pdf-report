from django.urls import path
from Brands.brand import views
urlpatterns = [
    path('test/', views.generate_obj_pdf),
]

