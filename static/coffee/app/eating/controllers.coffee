'use strict';

EatingController = angular.module('foodDiaryApp')
    .controller 'EatingController', ($scope, $http, apiName) ->
        $scope.eatings = []

        $scope.loadEatings = () ->
            url = Django.url 'api_dispatch_list',
                api_name: apiName
                resource_name: 'eating'
            $http
                url: url
                method: 'GET'
                headers:
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            .success (data) ->
                $scope.eatings = data.objects