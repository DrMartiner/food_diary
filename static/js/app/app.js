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

  angular.module('foodDiaryApp', []).config([
    '$httpProvider', function($httpProvider) {
      return $httpProvider.defaults.headers.post['X-CSRFToken'] = getCookie('csrftoken');
    }
  ]).constant('apiName', 'v1');

}).call(this);
