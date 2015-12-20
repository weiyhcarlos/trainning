angular.module('MachineInfo', ['angular-echarts', 'smart-table', 'MachineInfo.services'])
    .controller('TopController', function($scope, $interval, $state, stateValue, dataFactory,
        cpuInfo, memoryInfo, averageLoadInfo, netInfo) {
        if (!stateValue.end_date) {
            var date = new Date();
            stateValue.end_date = new Date(date.getFullYear(), date.getMonth(),
                    date.getDate(), date.getHours(), date.getMinutes()),
                stateValue.begin_date = new Date(date.getFullYear(), date.getMonth(),
                    date.getDate(), date.getHours(), date.getMinutes() - 1)
        }

        $scope.setSearch = function() {
            stateValue.operatorCount++;
            stateValue.realTime = false;
        }
        $scope.setRealTime = function() {
            stateValue.operatorCount++;
            stateValue.realTime = true;
        }

        function arrayObjectIndexOf(arr, obj) {
            for (var i = 0; i < arr.length; i++) {
                if (angular.equals(arr[i], obj)) {
                    return i;
                }
            };
            return -1;
        }

        $scope.stateValue = stateValue;
        dataFactory.getMachines()
            .success(function(machines) {
                $scope.machineList = machines;
                if (stateValue.selectedMachine == null)
                    stateValue.selectedMachine = machines[0];
                else {
                    stateValue.selectedMachine = machines[
                        arrayObjectIndexOf(machines, stateValue.selectedMachine)];
                }
                console.log($scope.stateValue.selectedMachine);
            });
    })
    .controller('BaseController', function($scope, stateValue) {
        $scope.stateValue = stateValue;
    })
    .controller('CpuController', function($interval, $scope, $state, dataFactory, stateValue, cpuInfo) {
        $scope.barConfig = {
            // title: 'Bar Chart',
            // subtitle: 'Bar Chart Subtitle',
            debug: true,
            stack: true
        };

        function updateData($interval) {
            return $interval(function() {
                dataFactory.getMachine(stateValue.selectedMachine.url)
                    .success(function(machine) {
                        cpuInfo.load(machine.cpu);
                        $scope.barMultiple = Object.keys(cpuInfo.percentage).map(function(key) {
                            return cpuInfo.percentage[key];
                        });
                        console.log(cpuInfo);
                    });
            }, 3000);
        }

        $scope.$watch(function() {
            return stateValue.operatorCount;
        }, function(newValue, oldValue) {
            console.log("watching operatorCount change. ");
            if (newValue != 0 && angular.equals(newValue, oldValue)) {
                $scope.barMultiple = Object.keys(cpuInfo.percentage).map(function(key) {
                    return cpuInfo.percentage[key];
                });
            } else {
                if (stateValue.realTime == false) {
                    if (stateValue.begin_date && stateValue.end_date) {
                        $interval.cancel(currentInterval);
                        dataFactory.getModule(stateValue.selectedMachine.url,
                                "cpu", stateValue.begin_date, stateValue.end_date)
                            .success(function(data) {
                                console.log(data);
                                cpuInfo.reInit(data);
                                $state.reload();
                                $scope.barMultiple = Object.keys(cpuInfo.percentage).map(function(key) {
                                    return cpuInfo.percentage[key];
                                });

                            });
                    }
                } else {
                    cpuInfo.clear();
                    if (newValue == 0) 
                        currentInterval = updateData($interval);
                    else {
                        stateValue.operatorCount = 0;
                        $state.reload();
                    }
                }
            }
        });

        $scope.$on("$destroy", function(event) {
            // alert("I am leaving");
            $interval.cancel(currentInterval);
        });

    })
    .controller('AverageLoadController', function($scope, $state, $interval, stateValue, dataFactory, averageLoadInfo) {
        $scope.lineConfig = {
            // title: 'Line Chart',
            // subtitle: 'Line Chart Subtitle',
            debug: true,
            showXAxis: true,
            showYAxis: true,
            showLegend: true,
            stack: false
        };

        function updateData($interval) {
            return $interval(function() {
                dataFactory.getMachine(stateValue.selectedMachine.url)
                    .success(function(machine) {
                        averageLoadInfo.load(machine.average_load);
                        $scope.lineMultiple = [averageLoadInfo.w1Avg, averageLoadInfo.w2Avg, averageLoadInfo.w3Avg];
                        console.log(averageLoadInfo);
                    });
            }, 3000);
        }

        $scope.$watch(function() {
            return stateValue.operatorCount;
        }, function(newValue, oldValue) {
            console.log("watching operatorCount change. ");
            if (newValue != 0 && angular.equals(newValue, oldValue)) {
                // console.log(newValue, stateValue.operatorCount);
                $scope.lineMultiple = [averageLoadInfo.w1Avg, averageLoadInfo.w2Avg, averageLoadInfo.w3Avg];
            } else {
                if (stateValue.realTime == false) {
                    if (stateValue.begin_date && stateValue.end_date) {
                        $interval.cancel(currentInterval);
                        dataFactory.getModule(stateValue.selectedMachine.url,
                                "average_load", stateValue.begin_date, stateValue.end_date)
                            .success(function(data) {
                                console.log(data);
                                averageLoadInfo.reInit(data);
                                $state.reload();
                                $scope.lineMultiple = [averageLoadInfo.w1Avg, averageLoadInfo.w2Avg, averageLoadInfo.w3Avg];
                                // console.log(stateValue.realTime+ "" + stateValue.operatorCount);

                            });
                        // console.log("stop currentInterval");
                    }
                } else {
                    averageLoadInfo.clear();
                    if (newValue == 0)
                        currentInterval = updateData($interval);
                    else {
                        stateValue.operatorCount = 0;
                        $state.reload();
                    }
                }
            }
        });

        $scope.$on("$destroy", function(event) {
            // alert("I am leaving");
            $interval.cancel(currentInterval);
        });
    })
    .controller('DiskRateController', function($interval, $scope, $state, stateValue, diskRate, dataFactory) {
        $scope.areaConfig = {
            // title: 'Area Chart',
            // subtitle: 'Area Chart Subtitle',
            // yAxis: { scale: true },
            debug: true,
            stack: true
        };

        function updateData($interval) {
            return $interval(function() {
                dataFactory.getMachine(stateValue.selectedMachine.url)
                    .success(function(machine) {
                        diskRate.load(machine.disk);
                        $scope.areaMultiple = [diskRate.readRate, diskRate.writeRate];
                        console.log(diskRate);
                    });
            }, 3000);
        }

        $scope.$watch(function() {
            return stateValue.operatorCount;
        }, function(newValue, oldValue) {
            console.log("watching operatorCount change. ");
            if (newValue != 0 && angular.equals(newValue, oldValue)) {
                // console.log(newValue, stateValue.operatorCount);
                $scope.areaMultiple = [diskRate.readRate, diskRate.writeRate];
            } else {
                if (stateValue.realTime == false) {
                    if (stateValue.begin_date && stateValue.end_date) {
                        $interval.cancel(currentInterval);
                        dataFactory.getModule(stateValue.selectedMachine.url,
                                "disk", stateValue.begin_date, stateValue.end_date)
                            .success(function(data) {
                                console.log(data);
                                diskRate.reInit(data);
                                $state.reload();
                                $scope.areaMultiple = [diskRate.sentRate, diskRate.recvRate];
                                // console.log(stateValue.realTime+ "" + stateValue.operatorCount);

                            });
                        // console.log("stop currentInterval");
                    }
                } else {
                    diskRate.clear();
                    if (newValue == 0)
                        currentInterval = updateData($interval);
                    else {
                        stateValue.operatorCount = 0;
                        $state.reload();
                    }
                }
            }
        });

        $scope.$on("$destroy", function(event) {
            // alert("I am leaving");
            $interval.cancel(currentInterval);
        });
    })
    .controller('DiskUsageController', function($interval, $scope, $state, stateValue, diskUsage, dataFactory) {
        $scope.lineConfig = {
            // title: 'Line Chart',
            // subtitle: 'Line Chart Subtitle',
            debug: true,
            showXAxis: true,
            showYAxis: true,
            showLegend: true,
            stack: false
        };

        function updateData($interval) {
            return $interval(function() {
                dataFactory.getMachine(stateValue.selectedMachine.url)
                    .success(function(machine) {
                        diskUsage.load(machine.disk);
                        $scope.lineMultiple = [diskUsage.total, diskUsage.used, diskUsage.free];
                        console.log(diskUsage);
                    });
            }, 3000);
        }

        $scope.$watch(function() {
            return stateValue.operatorCount;
        }, function(newValue, oldValue) {
            console.log("watching operatorCount change. ");
            if (newValue != 0 && angular.equals(newValue, oldValue)) {
                // console.log(newValue, stateValue.operatorCount);
                $scope.lineMultiple = [diskUsage.total, diskUsage.used, diskUsage.free];
            } else {
                if (stateValue.realTime == false) {
                    if (stateValue.begin_date && stateValue.end_date) {
                        $interval.cancel(currentInterval);
                        dataFactory.getModule(stateValue.selectedMachine.url,
                                "disk", stateValue.begin_date, stateValue.end_date)
                            .success(function(data) {
                                console.log(data);
                                diskUsage.reInit(data);
                                $state.reload();
                                $scope.lineMultiple = [diskUsage.total, diskUsage.used, diskUsage.free];
                                // console.log(stateValue.realTime+ "" + stateValue.operatorCount);

                            });
                        // console.log("stop currentInterval");
                    }
                } else {
                    diskUsage.clear();
                    if (newValue == 0)
                        currentInterval = updateData($interval);
                    else {
                        stateValue.operatorCount = 0;
                        $state.reload();
                    }
                }
            }
        });

        $scope.$on("$destroy", function(event) {
            // alert("I am leaving");
            $interval.cancel(currentInterval);
        });
    })
    .controller('NetController', function($interval, $scope, $state, $stateParams,
        stateValue, dataFactory, netInfo) {
        $scope.areaConfig = {
            // title: 'Area Chart',
            // subtitle: 'Area Chart Subtitle',
            // yAxis: { scale: true },
            debug: true,
            stack: true
        };

        function updateData($interval) {
            return $interval(function() {
                dataFactory.getMachine(stateValue.selectedMachine.url)
                    .success(function(machine) {
                        netInfo.load(machine.net);
                        $scope.areaMultiple = [netInfo.sentRate, netInfo.recvRate];
                        console.log(netInfo);
                    });
            }, 3000);
        }

        $scope.$watch(function() {
            return stateValue.operatorCount;
        }, function(newValue, oldValue) {
            console.log("watching operatorCount change. ");
            if (newValue != 0 && angular.equals(newValue, oldValue)) {
                // console.log(newValue, stateValue.operatorCount);
                $scope.areaMultiple = [netInfo.sentRate, netInfo.recvRate];
            } else {
                if (stateValue.realTime == false) {
                    if (stateValue.begin_date && stateValue.end_date) {
                        $interval.cancel(currentInterval);
                        dataFactory.getModule(stateValue.selectedMachine.url,
                                "net", stateValue.begin_date, stateValue.end_date)
                            .success(function(data) {
                                console.log(data);
                                netInfo.reInit(data);
                                $state.reload();
                                $scope.areaMultiple = [netInfo.sentRate, netInfo.recvRate];
                                // console.log(stateValue.realTime+ "" + stateValue.operatorCount);

                            });
                        // console.log("stop currentInterval");
                    }
                } else {
                    netInfo.clear();
                    if (newValue == 0)
                        currentInterval = updateData($interval);
                    else {
                        stateValue.operatorCount = 0;
                        $state.reload();
                    }
                }
            }
        });

        $scope.$on("$destroy", function(event) {
            // alert("I am leaving");
            $interval.cancel(currentInterval);
        });
    })
    .controller('MemoryController', function($interval, $scope, $state, dataFactory, stateValue, memoryInfo) {
        $scope.barConfig = {
            // title: 'Bar Chart',
            // subtitle: 'Bar Chart Subtitle',
            debug: true,
            stack: true
        };

        function updateData($interval) {
            return $interval(function() {
                dataFactory.getMachine(stateValue.selectedMachine.url)
                    .success(function(machine) {
                        memoryInfo.load(machine.memory);
                        $scope.barMultiple = Object.keys(memoryInfo.usage).map(function(key) {
                            return memoryInfo.usage[key];
                        });
                        console.log(memoryInfo);
                    });
            }, 3000);
        }

        $scope.$watch(function() {
            return stateValue.operatorCount;
        }, function(newValue, oldValue) {
            console.log("watching operatorCount change. ");
            if (newValue != 0 && angular.equals(newValue, oldValue)) {
                // console.log(newValue, stateValue.operatorCount);
                $scope.barMultiple = Object.keys(memoryInfo.usage).map(function(key) {
                    return memoryInfo.usage[key];
                });
            } else {
                if (stateValue.realTime == false) {
                    if (stateValue.begin_date && stateValue.end_date) {
                        $interval.cancel(currentInterval);
                        dataFactory.getModule(stateValue.selectedMachine.url,
                                "memory", stateValue.begin_date, stateValue.end_date)
                            .success(function(data) {
                                console.log(data);
                                memoryInfo.reInit(data);
                                $state.reload();
                                $scope.barMultiple = Object.keys(memoryInfo.usage).map(function(key) {
                                    return memoryInfo.usage[key];
                                });
                                // console.log(stateValue.realTime+ "" + stateValue.operatorCount);

                            });
                        // console.log("stop currentInterval");
                    }
                } else {
                    memoryInfo.clear();
                    if (newValue == 0)
                        currentInterval = updateData($interval);
                    else {
                        stateValue.operatorCount = 0;
                        $state.reload();
                    }
                }
            }
        });

        $scope.$on("$destroy", function(event) {
            // alert("I am leaving");
            $interval.cancel(currentInterval);
        });
    });
