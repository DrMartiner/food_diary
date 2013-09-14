(function() {
  'use strict';
  var EatingController, EatingFoodFormController;

  EatingController = angular.module('foodDiaryApp').controller('EatingController', function($scope, EatingResource, EatingFoodResource) {
    $scope.eatings = [];
    $scope.loadEatings = function() {
      return EatingResource.get(function(result) {
        return $scope.eatings = result.objects;
      });
    };
    $scope.createEating = function() {
      return EatingResource.save({}, function(eating) {
        eating.expand = true;
        return $scope.eatings.unshift(eating);
      });
    };
    $scope.deleteEating = function(eatingId) {
      return EatingResource["delete"]({
        id: eatingId
      }, function() {
        var eating, index, _i, _len, _ref, _results;
        _ref = $scope.eatings;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          eating = _ref[_i];
          if (eating.id === eatingId) {
            index = $scope.eatings.indexOf(eating);
            $scope.eatings.splice(index, 1);
            break;
          } else {
            _results.push(void 0);
          }
        }
        return _results;
      });
    };
    return $scope.deleteEatingFood = function(eatingId, eatingFoodId) {
      return EatingFoodResource["delete"]({
        id: eatingFoodId
      }, function() {
        var eating, eatingfood, index, _i, _j, _len, _len1, _ref, _ref1;
        _ref = $scope.eatings;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          eating = _ref[_i];
          if (eating.id === eatingId) {
            _ref1 = eating.eatingfoods;
            for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
              eatingfood = _ref1[_j];
              if (eatingfood.id === eatingFoodId) {
                index = eating.eatingfoods.indexOf(eatingfood);
                eating.eatingfoods.splice(index, 1);
                return;
              }
            }
          }
        }
      });
    };
  });

  EatingFoodFormController = angular.module('foodDiaryApp').controller('EatingFoodFormController', function($scope, FoodResource, EatingFoodResource) {
    $scope.foodId = null;
    $scope.foodName = null;
    $scope.foodCount = null;
    return $scope.createEatingFood = function(eatingId) {
      var addEatingFood, data;
      addEatingFood = function(eatingFood) {
        var eating, index, _i, _len, _ref;
        eatingFood.name = $scope.foodName;
        _ref = $scope.eatings;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          eating = _ref[_i];
          if (eating.id === eatingId) {
            index = $scope.eatings.indexOf(eating);
            $scope.eatings[index].eatingfoods.unshift(eatingFood);
            break;
          }
        }
        $scope.foodId = null;
        $scope.foodName = null;
        return $scope.foodCount = null;
      };
      if ($scope.foodId) {
        data = {
          food_id: $scope.foodId,
          count: $scope.foodCount,
          eating_id: eatingId
        };
        return EatingFoodResource.save(data, addEatingFood);
      } else {
        return FoodResource.save({
          name: $scope.foodName
        }, function(food) {
          data = {
            food_id: food.id,
            count: $scope.foodCount,
            eating_id: eatingId
          };
          return EatingFoodResource.save(data, addEatingFood);
        });
      }
    };
  });

}).call(this);