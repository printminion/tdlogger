'use strict';

var app = angular.module('tdloggerApp', []);

app.config(function ($routeProvider) {
  $routeProvider
    .when('/home',
      {
        templateUrl: 'static/messages/app/partials/home.html'
      })
    .when('/messages',
      {
        controller: 'MessageListController',
        templateUrl: 'static/messages/app/partials/messages.html'
      })
    .when('/messages/:messageId',
      {
        controller: 'MessageDetailController',
        templateUrl: 'static/messages/app/partials/message.html'
      })
    .when('/about',
      {
        templateUrl: 'static/messages/app/partials/about.html'
      })
    .otherwise({ redirectTo: '/home' });
});
