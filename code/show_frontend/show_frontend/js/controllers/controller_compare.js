/**
 * 对比控制器模块,定义各页面逻辑
 */
angular.module('MachineInfo_compare', ['angular-echarts', 'smart-table',
        'angularjs-dropdown-multiselect', 'ngAnimate',
        'ui.bootstrap', 'MachineInfo.services'
    ])
    // 控制全局按钮及信息处理
    .controller('TopCompareController', function($scope, $interval, $state,
        stateValueCompare, dataFactory, averageLoadCompareInfo,
        netCompareInfo, diskRateCompare) {
        // 当查询日期没有初始化时进行初始化,否则沿用上次使用的值
        if (!stateValueCompare.end_date) {
            var date = new Date();
            stateValueCompare.end_date = new Date(date.getFullYear(), date.getMonth(),
                    date.getDate(), date.getHours(), date.getMinutes()),
                stateValueCompare.begin_date = new Date(date.getFullYear(), date.getMonth(),
                    date.getDate(), date.getHours(), date.getMinutes() - 1)
        }

        $scope.alerts = [];

        $scope.closeAlert = function(index) {
            $scope.alerts.splice(index, 1);
        };

        // 对比按钮
        $scope.setCompare = function() {
            var timeDiff =
                stateValueCompare.end_date.getTime() - stateValueCompare.begin_date.getTime();
            if (timeDiff <= 1000 * 3600 && timeDiff > 0) {
                stateValueCompare.isSearch = true;
                // 清空遗留数据
                averageLoadCompareInfo.clear();
                diskRateCompare.clear();
                netCompareInfo.clear();
                $state.reload();
            } else if (timeDiff <= 0) {
                $scope.alerts.push({
                    type: "success",
                    msg: "开始时间晚于结束时间"
                });
            } else {
                $scope.alerts.push({
                    type: "success",
                    msg: "请选择不多于一个小时的查询时间段"
                });
            }
        }

        // 忽略angularjs内置值如$$hashkey进行obj比较, 
        // 返回arr中相同的对象
        function internalObjectFromArray(arr, obj) {
            for (var i = 0; i < arr.length; i++) {
                if (angular.equals(arr[i], obj)) {
                    return arr[i];
                }
            };
            return null;
        }

        $scope.stateValueCompare = stateValueCompare;
        // $scope.machineList=[{'ip':1}];
        //获得机器信息列表,初始化select指令
        dataFactory.getMachines()
            .success(function(machines) {
                $scope.machineList = machines;

                // 如果selectedMachine未初始化,赋值为列表中第一个
                // 如果已初始化,更新为带有新的$$hashkey的object
                // 否则select指令不会选中
                if (stateValueCompare.selectedMachine.length == 0) {
                    stateValueCompare.selectedMachine.push(machines[0]);
                } else {
                    newSelected = [];

                    for (var i = 0; i < stateValueCompare.selectedMachine.length; i++) {
                        newSelected.push(internalObjectFromArray(machines,
                            stateValueCompare.selectedMachine[i]));
                    }
                    stateValueCompare.selectedMachine = newSelected;
                }
            });
        $scope.showSetting = {
            displayProp: 'ip',
            idProp: 'ip',
            externalIdProp: '',
            enableSearch: true
        };
    })
    // 控制基础信息处理
    .controller('BaseCompareController', function($scope, stateValueCompare) {
        $scope.stateValueCompare = stateValueCompare;
    })
    // 控制平均负载信息处理
    .controller('AverageLoadCompareController', function($scope, $state, $interval,
        stateValueCompare, dataFactory, averageLoadCompareInfo) {
        $scope.lineConfig = {
            // title: '',
            // subtitle: '',
            // debug: true,
            showXAxis: true,
            showYAxis: true,
            showLegend: true,
            stack: false
        };

        // 进度条标识
        $scope.isLoading = false;

        // 记录所选机器信息是否加载完成，0代表完成
        $scope.loaded = 0;

        //查询时触发，当机器信息全部加载完时reload
        function updateChart($interval) {
            return $interval(function() {
                if ($scope.loaded == 0) {
                    stateValueCompare.isSearch = false;
                    $state.reload();
                }
            }, 1000);
        }

        if (stateValueCompare.isSearch) {
            //加载进度条
            $scope.isLoading = true;
            for (var i = 0; i < stateValueCompare.selectedMachine.length; i++) {
                $scope.loaded++;
                // 匿名函数，使i pass by value在异步过程中保持正确下标
                (function(i) {
                    dataFactory.getModule(stateValueCompare.selectedMachine[i].url,
                            "average_load", stateValueCompare.begin_date,
                            stateValueCompare.end_date)
                        .success(function(data) {
                            averageLoadCompareInfo.append(
                                stateValueCompare.selectedMachine[i].ip, data);
                            $scope.loaded--;
                        });
                })(i);
            }
            currentInterval = updateChart($interval);
        } else {
            //当有信息时渲染图表
            if (!averageLoadCompareInfo.empty()) {
                $scope.lineMultipleW1 = averageLoadCompareInfo.w1Avg;
                $scope.lineMultipleW2 = averageLoadCompareInfo.w2Avg;
                $scope.lineMultipleW3 = averageLoadCompareInfo.w3Avg;
            }
        }

        // 当离开当前state时, 停止interval
        $scope.$on("$destroy", function(event) {
            if (typeof currentInterval != 'undefined')
                $interval.cancel(currentInterval);
        });
    })
    .controller('DiskRateCompareController', function($interval, $scope, $state,
        stateValueCompare, diskRateCompare, dataFactory) {
        $scope.areaConfig = {
            // title: '',
            // subtitle: '',
            // debug: true,
            showXAxis: true,
            showYAxis: true,
            showLegend: true,
            stack: false
        };

        // 进度条标识
        $scope.isLoading = false;

        // 记录所选机器信息是否加载完成，0代表完成
        $scope.loaded = 0;

        //查询时触发，当机器信息全部加载完时reload
        function updateChart($interval) {
            return $interval(function() {
                if ($scope.loaded == 0) {
                    stateValueCompare.isSearch = false;
                    $state.reload();
                }
            }, 1000);
        }

        if (stateValueCompare.isSearch) {
            //加载进度条
            $scope.isLoading = true;
            for (var i = 0; i < stateValueCompare.selectedMachine.length; i++) {
                $scope.loaded++;
                // 匿名函数，使i pass by value在异步过程中保持正确下标
                (function(i) {
                    dataFactory.getModule(stateValueCompare.selectedMachine[i].url,
                            "disk", stateValueCompare.begin_date,
                            stateValueCompare.end_date)
                        .success(function(data) {
                            diskRateCompare.append(
                                stateValueCompare.selectedMachine[i].ip, data);
                            $scope.loaded--;
                        });
                })(i);
            }
            currentInterval = updateChart($interval);
        } else {
            //当有信息时渲染图表
            if (!diskRateCompare.empty()) {
                $scope.areaMultipleRead = diskRateCompare.readRate;
                $scope.areaMultipleWrite = diskRateCompare.writeRate;
            }
        }
        // 当离开当前state时, 停止interval
        $scope.$on("$destroy", function(event) {
            if (typeof currentInterval != 'undefined')
                $interval.cancel(currentInterval);
        });
    })
    .controller('NetCompareController', function($interval, $scope, $state,
        stateValueCompare, dataFactory, netCompareInfo) {
        $scope.lineConfig = {
            // title: '',
            // subtitle: '',
            // debug: true,
            showXAxis: true,
            showYAxis: true,
            showLegend: true,
            stack: false
        };

        // 进度条标识
        $scope.isLoading = false;

        // 记录所选机器信息是否加载完成，0代表完成
        $scope.loaded = 0;

        //查询时触发，当机器信息全部加载完时reload
        function updateChart($interval) {
            return $interval(function() {
                if ($scope.loaded == 0) {
                    stateValueCompare.isSearch = false;
                    $state.reload();
                }
            }, 1000);
        }

        if (stateValueCompare.isSearch) {
            //加载进度条
            $scope.isLoading = true;
            for (var i = 0; i < stateValueCompare.selectedMachine.length; i++) {
                $scope.loaded++;
                // 匿名函数，使i pass by value在异步过程中保持正确下标
                (function(i) {
                    dataFactory.getModule(stateValueCompare.selectedMachine[i].url,
                            "net", stateValueCompare.begin_date,
                            stateValueCompare.end_date)
                        .success(function(data) {
                            netCompareInfo.append(
                                stateValueCompare.selectedMachine[i].ip, data);
                            $scope.loaded--;
                        });
                })(i);
            }
            currentInterval = updateChart($interval);
        } else {
            //当有信息时渲染图表
            if (!netCompareInfo.empty()) {
                $scope.areaMultipleSent = netCompareInfo.sentRate;
                $scope.areaMultipleRecv = netCompareInfo.recvRate;
            }
        }
        // 当离开当前state时, 停止interval
        $scope.$on("$destroy", function(event) {
            if (typeof currentInterval != 'undefined')
                $interval.cancel(currentInterval);
        });
    });
