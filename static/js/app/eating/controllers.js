(function() {
  'use strict';
  var EatingController, EatingFoodFormController;

  EatingController = angular.module('foodDiaryApp').controller('EatingController', function($scope, EatingResource, EatingFoodResource) {
    $scope.allEatings = {};
    $scope.loadEatings = function() {
      return EatingResource.get(function(result) {
        var t;
        return $scope.allEatings = t = _.groupBy(result.objects, function(obj) {
          return obj.pub_date.slice(0, 10);
        });
      });
    };
    $scope.createEating = function() {
      return EatingResource.save({}, function(eating) {
        var pubDate;
        eating.expand = true;
        pubDate = eating.pub_date.slice(0, 10);
        if (!$scope.allEatings[pubDate]) {
          $scope.allEatings[pubDate] = [];
        }
        return $scope.allEatings[pubDate].unshift(eating);
      });
    };
    $scope.deleteEating = function(eatingId) {
      return EatingResource["delete"]({
        id: eatingId
      }, function() {
        var date, eating, eatings, _ref, _results;
        _ref = $scope.allEatings;
        _results = [];
        for (date in _ref) {
          eatings = _ref[date];
          _results.push((function() {
            var _i, _len, _results1;
            _results1 = [];
            for (_i = 0, _len = eatings.length; _i < _len; _i++) {
              eating = eatings[_i];
              if (eating.id === eatingId) {
                $scope.allEatings[date] = _.without(eatings, eating);
                if (!$scope.allEatings[date].length) {
                  _results1.push(delete $scope.allEatings[date]);
                } else {
                  _results1.push(void 0);
                }
              } else {
                _results1.push(void 0);
              }
            }
            return _results1;
          })());
        }
        return _results;
      });
    };
    return $scope.deleteEatingFood = function(eatingId, eatingFoodId) {
      return EatingFoodResource["delete"]({
        id: eatingFoodId
      }, function() {
        var date, eating, eatingfood, eatings, _i, _j, _len, _len1, _ref, _ref1;
        _ref = $scope.allEatings;
        for (date in _ref) {
          eatings = _ref[date];
          for (_i = 0, _len = eatings.length; _i < _len; _i++) {
            eating = eatings[_i];
            _ref1 = eating.eatingfoods;
            for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
              eatingfood = _ref1[_j];
              if (eatingfood.id === eatingFoodId) {
                _.without(eating.eatingfoods, eatingfood);
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
