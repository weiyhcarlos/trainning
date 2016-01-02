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
        //平均负载信息子页面
        .state('index.single.average_load', {
            url: '/average_load',
            templateUrl: 'tpls/single/detail_part/average_load.html'
        })
        //cpu信息子页面
        .state('index.single.cpu', {
            url: '/cpu',
            templateUrl: 'tpls/single/detail_part/cpu.html'
        })
        //内存信息子页面
        .state('index.single.memory', {
            url: '/memory',
            templateUrl: 'tpls/single/detail_part/memory.html'
        })
        //磁盘使用信息子页面
        .state('index.single.disk_usage', {
            url: '/disk_usage',
            templateUrl: 'tpls/single/detail_part/disk_usage.html'
        })
        //磁盘速率信息子页面
        .state('index.single.disk_rate', {
            url: '/disk_rate',
            templateUrl: 'tpls/single/detail_part/disk_rate.html'
        })
        //网卡速率信息子页面
        .state('index.single.net', {
            url: '/net',
            templateUrl: 'tpls/single/detail_part/net.html'
        })
        .state('index.compare', {
            url: '/compare',
            views: {
                'main@index': {
                    templateUrl: 'tpls/compare/detail.html'
                }
            }
        })
        .state('index.compare.disk_rate', {
            url: '/disk_rate',
            templateUrl: 'tpls/compare/detail_part/disk_rate.html'
        })
        .state('index.compare.net', {
            url: '/net',
            templateUrl: 'tpls/compare/detail_part/net.html'
        })
        .state('index.compare.average_load', {
            url: '/average_load',
            templateUrl: 'tpls/compare/detail_part/average_load.html'
        });
});
