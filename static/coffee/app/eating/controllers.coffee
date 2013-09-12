'use strict';

EatingController = angular.module('foodDiaryApp')
    .controller 'EatingController', ($scope, FoodResource, EatingResource, EatingFoodResource) ->
        $scope.eatings = []
        $scope.foodId = null
        $scope.foodName = null
        $scope.foodCount = null

        $scope.loadEatings = () ->
            EatingResource.get (result) ->
                $scope.eatings = result.objects

        $scope.createEating = () ->
            EatingResource.save {}, (eating) ->
                eating.expand = true
                $scope.eatings.unshift eating

        $scope.deleteEating = (eatingId) ->
            EatingResource.delete {id: eatingId}, () ->
                for eating in $scope.eatings
                    if eating.id == eatingId
                        index = $scope.eatings.indexOf eating
                        $scope.eatings.splice index, 1
                        break

        $scope.deleteEatingFood = (eatingId, eatingFoodId)  ->
            EatingFoodResource.delete {id: eatingFoodId}, () ->
                for eating in $scope.eatings
                    if eating.id == eatingId
                        for eatingfood in eating.eatingfoods
                            if eatingfood.id == eatingFoodId
                                index = eating.eatingfoods.indexOf eatingfood
                                eating.eatingfoods.splice index, 1
                                break
                        break

        $scope.createEatingFood = (eatingId) ->
            addEatingFood = (eatingFood) ->
                eatingFood.name = $scope.foodName
                for eating in $scope.eatings
                    if eating.id == eatingId
                        index = $scope.eatings.indexOf eating
                        $scope.eatings[index].eatingfoods.unshift eatingFood
                        break
                $scope.foodId = null
                $scope.foodName = null
                $scope.foodCount = null

            if $scope.foodId
                data =
                    food_id: $scope.foodId
                    count: $scope.foodCount
                    eating_id: eatingId
                EatingFoodResource.save data, addEatingFood

            else
                FoodResource.save {name: $scope.foodName}, (food) ->
                    data =
                        food_id: food.id
                        eating_id: eatingId
                    EatingFoodResource.save data, addEatingFood