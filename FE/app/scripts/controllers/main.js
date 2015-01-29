'use strict';

function Elastic($http){
  return{
    serach: function(keyword,cb){
      console.log(keyword);
      $http.post('http://localhost:9200/music_search/mp3_v7/_search',
      {
        'query' : {
          'prefix' : { '_all': keyword }
        }
      }).success(cb).error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        console.log('ERR : with '+keyword);
      });
    }
  };
}

/**
 * @ngdoc function
 * @name feApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the feApp
 */
angular.module('feApp')
  .controller('MainCtrl', ['$http', '$scope', function ($http,$scope) {
    $scope.model = { keyword: ''};
    var model={};
   model.search =  function(){
   var elastic=new Elastic($http);
   $scope.results =elastic.serach($scope.model.keyword,function(data){
  $scope.results=data.hits.hits;
   });
 };

 model.play = function(src){
  $scope.model.curSong=src;
  };
  model.curSong='';
  $scope.model=model;

  }]);
