var routerApp = angular.module('routerApp', ['ui.router', 'ngAnimate', 'ui.bootstrap', 'angularjs-dropdown-multiselect',
    'MachineInfo.services', 'MachineInfo.directives', 'MachineInfo'
]);
/**
 * 由于整个应用都会和路由打交道，所以这里把$state和$stateParams这两个对象放到$rootScope上，方便其它地方引用和注入。
 * 这里的run方法只会在angular启动的时候运行一次。
 * @param  {[type]} $rootScope
 * @param  {[type]} $state
 * @param  {[type]} $stateParams
 * @return {[type]}
 */
routerApp.run(function($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
});

routerApp.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/index');
    $stateProvider
    // 主页--包含导航栏和主体内容
        .state('index', {
            url: '/index',
            views: {
                '': {
                    templateUrl: 'tpls/index.html'
                },
                'detail@index': {
                    templateUrl: 'tpls/detail.html'
                },
                'topbar@index': {
                    templateUrl: 'tpls/topbar.html'
                }
            }
        })
        .state('index.average_load', {
            url: '/average_load',
            templateUrl: 'tpls/detail_part/average_load.html'
        })
        .state('index.cpu', {
            url: '/cpu',
            templateUrl: 'tpls/detail_part/cpu.html'
        })
        .state('index.memory', {
            url: '/memory',
            templateUrl: 'tpls/detail_part/memory.html'
        })
        .state('index.disk_usage', {
            url: '/disk_usage',
            templateUrl: 'tpls/detail_part/disk_usage.html'
        })
        .state('index.disk_rate', {
            url: '/disk_rate',
            templateUrl: 'tpls/detail_part/disk_rate.html'
        })
        .state('index.net', {
            url: '/net',
            templateUrl: 'tpls/detail_part/net.html'
        })
});
