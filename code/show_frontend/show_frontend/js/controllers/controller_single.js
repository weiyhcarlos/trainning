/**
 * 单机控制器模块,定义各页面逻辑
 */
angular.module('MachineInfo_single', ['angular-echarts', 'smart-table',
        'ngAnimate', 'ui.bootstrap', 'ui.bootstrap.datetimepicker', 'MachineInfo.services'
    ])
    // 控制全局按钮及信息处理
    .controller('TopController', function($scope, $interval, $state,
        stateValue, dataFactory, singlePageInfo) {
        $scope.open = {
            begin_date: false,
            end_date:false
        };

        $scope.openCalendar = function(e, date) {
            $scope.open[date] = true;
        };

        // 当查询日期没有初始化时进行初始化,否则沿用上次使用的值
        if (!stateValue.end_date) {
            var date = new Date();
            stateValue.end_date = new Date(date.getFullYear(), date.getMonth(),
                    date.getDate(), date.getHours(), date.getMinutes()),
                stateValue.begin_date = new Date(date.getFullYear(), date.getMonth(),
                    date.getDate(), date.getHours(), date.getMinutes() - 1)
        }

        $scope.alerts = [];

        $scope.closeAlert = function(index) {
            $scope.alerts.splice(index, 1);
        };

        // 查询按钮及实时按钮.触发相应值供子页面控制器监听
        $scope.setSearch = function() {
            var timeDiff =
                stateValue.end_date.getTime() - stateValue.begin_date.getTime();
            if (timeDiff <= 1000 * 3600 && timeDiff > 0) {
                stateValue.operatorCount++;
                stateValue.realTime = false;
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
        $scope.setRealTime = function() {
            stateValue.operatorCount++;
            stateValue.realTime = true;
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

        $scope.stateValue = stateValue;

        //获得机器信息列表,初始化select指令
        dataFactory.getMachines()
            .success(function(machines) {
                $scope.machineList = machines;
                // 如果selectedMachine未初始化,赋值为列表中第一个
                // 如果已初始化,更新为带有新的$$hashkey的object
                // 否则select指令不会选中
                if (stateValue.selectedMachine == null)
                    stateValue.selectedMachine = machines[0];
                else {
                    stateValue.selectedMachine =
                        internalObjectFromArray(machines,
                            stateValue.selectedMachine);
                }
            });
    })
    // 控制基础信息处理
    .controller('BaseController', function($scope, stateValue) {
        $scope.stateValue = stateValue;
    })
    .controller('SingleController', function($interval, $scope, $state,
        dataFactory, stateValue, singlePageInfo) {
        $scope.barConfig = {
            // title: '',
            // subtitle: '',
            // debug: true,
            stack: true
        };
        $scope.lineConfig = {
            // title: '',
            // subtitle: '',
            // debug: true,
            showXAxis: true,
            showYAxis: true,
            showLegend: true,
            stack: false
        };
        $scope.areaConfig = {
            // title: 'Area Chart',
            // subtitle: 'Area Chart Subtitle',
            // yAxis: { scale: true },
            debug: true,
            stack: true
        };

        $scope.isLoading = false;

        function updateData($interval) {
            return $interval(function() {
                dataFactory.getMachine(stateValue.selectedMachine.url)
                    .success(function(machine) {
                        if ($scope.isLoading)
                            $scope.isLoading = false;
                        singlePageInfo.load(machine);
                        $scope.cpuBarMultiple = Object.keys(singlePageInfo.percentage).map(
                            function(key) {
                                return singlePageInfo.percentage[key];
                            });
                        $scope.averageLoadLineMultiple = [singlePageInfo.w1Avg,
                            singlePageInfo.w2Avg, singlePageInfo.w3Avg
                        ];
                        $scope.diskRateAreaMultiple = [singlePageInfo.readRate, singlePageInfo.writeRate];
                        $scope.diskUsageLineMultiple = [singlePageInfo.total, singlePageInfo.used,
                            singlePageInfo.free
                        ];
                        $scope.netAreaMultiple = [singlePageInfo.sentRate, singlePageInfo.recvRate];
                        $scope.memoryBarMultiple = Object.keys(singlePageInfo.usage).map(
                            function(key) {
                                return singlePageInfo.usage[key];
                            });
                    });
            }, 3000);
        }

        //监听operatorCount,判断实时或查询
        $scope.$watch(function() {
            return stateValue.operatorCount;
        }, function(newValue, oldValue) {
            // 如果变化的值相同(angularjs 刷新state时 值不变也会触发监听事件),
            // 代表保留上次结果, 用已有的cpuInfo赋值,跳过处理
            if (newValue != 0 && angular.equals(newValue, oldValue)) {
                $scope.cpuBarMultiple = Object.keys(singlePageInfo.percentage).map(
                    function(key) {
                        return singlePageInfo.percentage[key];
                    });
                $scope.averageLoadLineMultiple = [singlePageInfo.w1Avg,
                    singlePageInfo.w2Avg, singlePageInfo.w3Avg
                ];
                $scope.diskRateAreaMultiple = [singlePageInfo.readRate, singlePageInfo.writeRate];
                $scope.diskUsageLineMultiple = [singlePageInfo.total, singlePageInfo.used,
                    singlePageInfo.free
                ];
                $scope.netAreaMultiple = [singlePageInfo.sentRate, singlePageInfo.recvRate];
                $scope.memoryBarMultiple = Object.keys(singlePageInfo.usage).map(
                    function(key) {
                        return singlePageInfo.usage[key];
                    });
            } else {
                // 触发查询时,请求数据并reload 当前state
                if (stateValue.realTime == false) {
                    if (stateValue.begin_date && stateValue.end_date) {
                        $interval.cancel(currentInterval);
                        dataFactory.getModule(stateValue.selectedMachine.url,
                                "cpu,average_load,memory,net,disk", stateValue.begin_date, stateValue.end_date)
                            .success(function(data) {
                                singlePageInfo.reInit(data);
                                $state.reload();
                            });
                    }
                    // 触发实时时,清空遗留数据. 如果判断为用户触发按钮, reload 当前 state
                } else {
                    singlePageInfo.clear();
                    if (newValue == 0) {
                        $scope.isLoading = true;
                        currentInterval = updateData($interval);
                    } else {
                        stateValue.operatorCount = 0;
                        $state.reload();
                    }
                }
            }
        });

        // 当离开当前state时, 停止interval
        $scope.$on("$destroy", function(event) {
            if (typeof currentInterval != 'undefined')
                $interval.cancel(currentInterval);
            $interval.cancel(currentInterval);
        });
    });
