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

angular.module('foodDiaryApp', [])
    .config(['$httpProvider', ($httpProvider) ->
        $httpProvider.defaults.headers.post['X-CSRFToken'] = getCookie 'csrftoken'
    ])
    .constant('apiName', 'v1')
