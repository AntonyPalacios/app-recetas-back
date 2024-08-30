from django.db import models


# Create your models here.
class Ingredient(models.Model):
    ingredientId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Recipe(models.Model):
    recipeId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=100)
