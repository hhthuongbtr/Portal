app.factory('agents', ['$http', function($http) { 
  return $http.get('/agent/json/') 
            .success(function(data) { 
              return data; 
            }) 
            .error(function(err) { 
              return err; 
            }); 
}]);