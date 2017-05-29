app.controller('channelCtrl', ['$scope', 'channels', function($scope, channels, $timeout) {
  channels.success(function(data) {
    $scope.myData = data.channels;
    console.log($scope.myData);
  });
}]);