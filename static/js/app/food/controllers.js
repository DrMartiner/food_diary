(function() {
  var FoodController;

  FoodController = angular.module('foodDiaryApp').controller('FoodController', function($scope, $resource, FoodResource) {
    $scope.foods = [];
    $scope.foodName = '';
    $scope.loadFoods = function() {
      return FoodResource.get(function(result) {
        return $scope.foods = result.objects;
      });
    };
    $scope.createFood = function() {
      return FoodResource.save({
        name: $scope.foodName
      }, function(food) {
        $scope.foods.unshift(food);
        return $scope.foodName = null;
      });
    };
    return $scope.deleteFood = function(foodId) {
      return FoodResource["delete"]({
        id: foodId
      }, function() {
        var food, index, _i, _len, _ref, _results;
        _ref = $scope.foods;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          food = _ref[_i];
          if (food.id === foodId) {
            index = $scope.foods.indexOf(food);
            $scope.foods.splice(index, 1);
            break;
          } else {
            _results.push(void 0);
          }
        }
        return _results;
      });
    };
  });

}).call(this);
