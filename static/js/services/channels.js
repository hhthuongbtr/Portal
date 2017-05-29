app.factory('channels', ['$http', function($http) { 
  return $http.get('/channel/json/') 
            .success(function(data) { 
              return data; 
            }) 
            .error(function(err) { 
              return err; 
            }); 
}]);