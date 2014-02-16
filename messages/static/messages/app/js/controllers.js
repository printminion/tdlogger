'use strict';

app.controller('MessageListController', function ($scope, $location, Message, Status) {
    var page_size = 6;

    Array.prototype.chunk = function (page_size) {
        var R = [];
        for (var i = 0; i < this.length; i += page_size)
            R.push(this.slice(i, i + page_size));
        return R;
    };

    var page = $location.search().page;
    if (page) {
        $scope.page = page;
    } else {
        $scope.page = 1;
    }

    $scope.prev_page = $scope.page - 1;
    $scope.next_page = parseInt($scope.page) + 1;

    var upperlimit = 0;
    $scope.isOutside = function (page) {
        return page <= 0 || page > upperlimit;
    };

    $scope.loadMessage = function (messageId) {
        Message.get(messageId, function (data) {
            $scope.message = data[0];
        });
    };

    Message.query($scope.page, page_size, function (data) {
        upperlimit = data.count / page_size + 1;
        if ($scope.isOutside($scope.prev_page)) {
            $scope.prev_page_url = '#' + $location.url();
        } else {
            $scope.prev_page_url = '#/messages?page=' + $scope.prev_page;
        }
        if ($scope.isOutside($scope.next_page)) {
            $scope.next_page_url = '#' + $location.url();
        } else {
            $scope.next_page_url = '#/messages?page=' + $scope.next_page;
        }
        $scope.message_rows = data.chunk(100);
    });

    Status.get(undefined, function (data) {
        $scope.status = data.payload;
        drawVisualization(data.payload.messages);
    });
});

app.controller('MessageDetailController',
    function ($scope, $routeParams, Message) {
        Message.get($routeParams.messageId, function (data) {
            $scope.message = data[0];
        });
    });

app.controller('NavbarController', function ($scope, $location) {
    $scope.getActive = function (path) {
        return $location.url().split('?')[0] == path;
    }
});
