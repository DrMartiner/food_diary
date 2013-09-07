(function() {
  'use strict';
  var EatingController;

  EatingController = angular.module('foodDiaryApp').controller('EatingController', function($scope, $http, apiName) {
    $scope.eatings = [];
    return $scope.loadEatings = function() {
      var url;
      url = Django.url('api_dispatch_list', {
        api_name: apiName,
        resource_name: 'eating'
      });
      return $http({
        url: url,
        method: 'GET',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
      }).success(function(data) {
        return $scope.eatings = data.objects;
      });
    };
  });

}).call(this);
