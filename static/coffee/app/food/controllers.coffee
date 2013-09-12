FoodController = angular.module('foodDiaryApp')
    .controller 'FoodController', ($scope, $resource, FoodResource) ->
        $scope.foods = []
        $scope.foodName = ''

        $scope.loadFoods = () ->
            FoodResource.get (result) ->
                $scope.foods = result.objects

        $scope.createFood = () ->
            FoodResource.save {name: $scope.foodName}, (food) ->
                $scope.foods.unshift food
                $scope.foodName = null

        $scope.deleteFood = (foodId) ->
            FoodResource.delete {id: foodId}, () ->
                for food in $scope.foods
                    if food.id == foodId
                        index = $scope.foods.indexOf food
                        $scope.foods.splice index, 1
                        break

