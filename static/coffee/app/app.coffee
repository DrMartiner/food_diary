'use strict';

getCookie = (name) ->
    cookieValue = null
    if document.cookie && document.cookie != ''
        cookies = document.cookie.split ';'
        for cookie in cookies
            cookie = $.trim(cookie)
            if cookie.substring(0, name.length + 1) == (name + '=')
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
    return cookieValue

angular.module('foodDiaryApp', ['ngResource'])
    .constant('apiName', 'v1')
    .config(['$httpProvider', ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-CSRFToken'] = getCookie 'csrftoken'
        $httpProvider.defaults.headers.common['Content-Type'] = 'application/json'
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/json'
        $httpProvider.defaults.headers.put['Content-Type'] = 'application/json'
    ])
    .factory('FoodResource', ($resource, apiName) ->
        url = Django.url 'api_dispatch_list',
            api_name: apiName
            resource_name: 'food'
        url += '/:id/'
        return $resource url, {}
    )
    .factory('EatingResource', ($resource, apiName) ->
        url = Django.url 'api_dispatch_list',
            api_name: apiName
            resource_name: 'eating'
        url += '/:id/'
        return $resource url, {}
    )
    .factory('EatingFoodResource', ($resource, apiName) ->
        url = Django.url 'api_dispatch_list',
            api_name: apiName
            resource_name: 'eatingfood'
        url += '/:id/'
        return $resource url, {}
    )