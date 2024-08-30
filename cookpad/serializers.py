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
        print(validated_data)
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        ingredients = validated_data['ingredients']
        for ingredient_data in ingredients:
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
