/**
 * 路由模块,启动app,加载所需模块
 */
 
var routerApp = angular.module('routerApp', ['ui.router', 
    'angularjs-dropdown-multiselect', 
    'MachineInfo.services', 'MachineInfo.directives', 'MachineInfo'
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
                'detail@index': {
                    templateUrl: 'tpls/detail.html'
                },
                'topbar@index': {
                    templateUrl: 'tpls/topbar.html'
                }
            }
        })
        //平均负载信息子页面
        .state('index.average_load', {
            url: '/average_load',
            templateUrl: 'tpls/detail_part/average_load.html'
        })
        //cpu信息子页面
        .state('index.cpu', {
            url: '/cpu',
            templateUrl: 'tpls/detail_part/cpu.html'
        })
        //内存信息子页面
        .state('index.memory', {
            url: '/memory',
            templateUrl: 'tpls/detail_part/memory.html'
        })
        //磁盘使用信息子页面
        .state('index.disk_usage', {
            url: '/disk_usage',
            templateUrl: 'tpls/detail_part/disk_usage.html'
        })
        //磁盘速率信息子页面
        .state('index.disk_rate', {
            url: '/disk_rate',
            templateUrl: 'tpls/detail_part/disk_rate.html'
        })
        //网卡速率信息子页面
        .state('index.net', {
            url: '/net',
            templateUrl: 'tpls/detail_part/net.html'
        })
});
