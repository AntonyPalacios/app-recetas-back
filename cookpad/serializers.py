from rest_framework import serializers

from cookpad.models import Recipe, Ingredient, RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    ingredientId = serializers.IntegerField(required=False)

    class Meta:
        model = Ingredient
        fields = ['ingredientId', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['recipeId', 'title', 'description', 'ingredients']

    def create(self, validated_data):
        recipe = Recipe.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
        )
        if 'ingredients' not in validated_data:
            return recipe

        ingredients = validated_data['ingredients']
        for ingredient_data in ingredients:
            ingredient = Ingredient.objects.get(ingredientId=ingredient_data['ingredient']['ingredientId'])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )
        return recipe

    def update(self, instance, validated_data):
        recipeId = instance.recipeId
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.save()

        ingredients = validated_data['ingredients']
        newIngredientsId = {item['ingredient']['ingredientId'] for item in ingredients}
        recipeIngredients = RecipeIngredient.objects.filter(recipe_id=recipeId)
        existingIngredientsId = {item.ingredient_id for item in recipeIngredients}

        toRemove = existingIngredientsId - newIngredientsId
        toAdd = newIngredientsId - existingIngredientsId

        RecipeIngredient.objects.filter(recipe_id=recipeId,ingredient_id__in=toRemove).delete()

        for item in ingredients:
            ingredient_id = item['ingredient']['ingredientId']
            quantity = item['quantity']
            unit = item['unit']

            # Si el ingrediente ya existe, lo actualizamos
            if ingredient_id in existingIngredientsId:
                recipe_ingredient = recipeIngredients.get(ingredient_id=ingredient_id)
                recipe_ingredient.quantity = quantity
                recipe_ingredient.unit = unit
                recipe_ingredient.save()
            else:
                # Si no existe, lo creamos
                RecipeIngredient.objects.create(
                    recipe_id=recipeId,
                    ingredient_id=ingredient_id,
                    quantity=quantity,
                    unit=unit
                )

        return instance
