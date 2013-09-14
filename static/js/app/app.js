(function() {
  'use strict';
  var getCookie;

  getCookie = function(name) {
    var cookie, cookieValue, cookies, _i, _len;
    cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      cookies = document.cookie.split(';');
      for (_i = 0, _len = cookies.length; _i < _len; _i++) {
        cookie = cookies[_i];
        cookie = $.trim(cookie);
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  angular.module('foodDiaryApp', ['ngResource']).constant('apiName', 'v1').config([
    '$httpProvider', function($httpProvider) {
      $httpProvider.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');
      $httpProvider.defaults.headers.common['Content-Type'] = 'application/json';
      $httpProvider.defaults.headers.post['Content-Type'] = 'application/json';
      return $httpProvider.defaults.headers.put['Content-Type'] = 'application/json';
    }
  ]).factory('FoodResource', function($resource, apiName) {
    var url;
    url = Django.url('api_dispatch_list', {
      api_name: apiName,
      resource_name: 'food'
    });
    url += '/:id/';
    return $resource(url, {});
  }).factory('EatingResource', function($resource, apiName) {
    var url;
    url = Django.url('api_dispatch_list', {
      api_name: apiName,
      resource_name: 'eating'
    });
    url += '/:id/';
    return $resource(url, {});
  }).factory('EatingFoodResource', function($resource, apiName) {
    var url;
    url = Django.url('api_dispatch_list', {
      api_name: apiName,
      resource_name: 'eatingfood'
    });
    url += '/:id/';
    return $resource(url, {});
  });

}).call(this);
