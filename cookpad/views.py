from django.db import transaction
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, RecipeCreateSerializer, IngredientSerializer, RecipeIngredientSerializer


# Create your views here.


class RecipeList(APIView):

    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = RecipeCreateSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            serializer.create(validated_data=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientList(APIView):

    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):

    def get_object(self, pk):
        try:
            return Recipe.objects.get(recipeId=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, recipeId, format=None):
        recipe = self.get_object(recipeId)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, recipeId, format=None):
        recipe = self.get_object(recipeId)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.update(recipe, request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipeId, format=None):
        recipe = self.get_object(recipeId)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
