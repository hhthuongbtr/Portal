app.directive('channelinfo', function() { 
  return { 
    restrict: 'E', 
    scope: { 
      info: '=' 
    }, 
    templateUrl: 'js/directives/channelinfo.html' 
  }; 
});
