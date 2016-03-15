/**
 * 路由模块,启动app,加载所需模块
 */

var routerApp = angular.module('routerApp', ['ui.router',
    'angularjs-dropdown-multiselect',
    'MachineInfo.services', 'MachineInfo.directives',
    'MachineInfo_single', 'MachineInfo_compare'
]);

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
                'main@index': {
                    templateUrl: 'tpls/home.html'
                },
                'topbar@index': {
                    templateUrl: 'tpls/topbar.html'
                }
            }
        })
        .state('index.single', {
            url: '/single',
            views: {
                'main@index': {
                    templateUrl: 'tpls/single/detail.html'
                }
            }
        })
        .state('index.compare', {
            url: '/compare',
            views: {
                'main@index': {
                    templateUrl: 'tpls/compare/detail.html'
                }
            }
        });
});
