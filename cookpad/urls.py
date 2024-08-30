from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.RecipeListCreateAPIView.as_view(), name='recipes'),
    path('ingredients/', views.IngredientListCreateAPIView.as_view(), name='ingredients'),
    path('recipes/<int:recipeId>/', views.RecipeDetailAPIView.as_view(), name='recipeDetail'),
]
