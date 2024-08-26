from rest_framework import serializers

from cookpad.models import Recipe, Ingredient, RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredientId', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['recipeId', 'title', 'description', 'ingredients']
        extra_kwargs = {
            'recipeId': {'required': False},
        }

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
        )
        for ingredient_data in ingredients:
            ingredient = Ingredient.objects.get(ingredientId=ingredient_data['ingredientId'])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )
        return recipe


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = ['recipeId', 'title', 'description', 'ingredients']

    def update(self, instance, validated_data):
        recipeId = validated_data.pop('recipeId')
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        for ingredient_data in validated_data['ingredients']:
            try:
                recipeIngredient = RecipeIngredient.objects.get(
                    ingredient_id=ingredient_data['ingredient']['ingredientId'],
                    recipe_id=recipeId)
                recipeIngredient.quantity = ingredient_data['quantity']
                recipeIngredient.unit = ingredient_data['unit']
                recipeIngredient.save()
            except RecipeIngredient.DoesNotExist:
                RecipeIngredient.objects.create(
                    recipe_id=recipeId,
                    ingredient_id=ingredient_data['ingredient']['ingredientId'],
                    quantity=ingredient_data['quantity'],
                    unit=ingredient_data['unit']
                )
        instance.save()
        return instance
