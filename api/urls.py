from django.urls import path
from .views import *

urlpatterns = [
    path('dish', DishView.as_view()),
    path('dish/<int:pk>', DishDetailView.as_view()),
    path('menu/random', MenuRandomView.as_view()),
    path('menu', MenuView.as_view()),
    path('menu/<int:pk>', MenuDetailView.as_view()),
    path('menu/<int:pk>/list', ShopListView.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
]
