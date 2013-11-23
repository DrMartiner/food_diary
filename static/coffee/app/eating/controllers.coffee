'use strict';

EatingController = angular.module('foodDiaryApp')
    .controller 'EatingController', ($scope, EatingResource, EatingFoodResource) ->
        $scope.allEatings = {}

        $scope.loadEatings = () ->
            EatingResource.get (result) ->
                $scope.allEatings = t = _.groupBy result.objects, (obj) ->
                    return obj.pub_date[..9]

        $scope.createEating = () ->
            EatingResource.save {}, (eating) ->
                eating.expand = true
                pubDate = eating.pub_date[..9]
                if not $scope.allEatings[pubDate]
                    $scope.allEatings[pubDate] = []
                $scope.allEatings[pubDate].unshift eating

        $scope.deleteEating = (eatingId) ->
            EatingResource.delete {id: eatingId}, () ->
                for date, eatings of $scope.allEatings
                    eating = _.findWhere eatings, {id: eatingId}
                    if eating
                        $scope.allEatings[date] = _.without eatings, eating
                        if not $scope.allEatings[date].length
                            delete $scope.allEatings[date]

                        break

        $scope.deleteEatingFood = (eatingId, eatingFoodId)  ->
            EatingFoodResource.delete {id: eatingFoodId}, () ->
                for date, eatings of $scope.allEatings
                    eating = _.findWhere eatings, {id: eatingId}
                    if eating
                        eatingfood = _.findWhere eatings, {id: eatingFoodId}
                        eating.eatingfoods = _.without eating.eatingfoods, eatingfood

EatingFoodFormController = angular.module('foodDiaryApp')
    .controller 'EatingFoodFormController', ($scope, FoodResource, EatingFoodResource) ->
        $scope.foodId = null
        $scope.foodName = null
        $scope.foodCount = null

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
                        count: $scope.foodCount
                        eating_id: eatingId
                    EatingFoodResource.save data, addEatingFood