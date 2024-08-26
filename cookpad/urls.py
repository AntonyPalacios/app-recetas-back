from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view(), name='recipes'),
    path('ingredients/', views.IngredientList.as_view(), name='ingredients'),
    path('recipes/<int:recipeId>/', views.RecipeDetail.as_view(), name='recipeDetail'),
]
