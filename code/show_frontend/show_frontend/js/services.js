/**
 * 服务模块,自定义服务
 */

function generateDataPoints(keyList) {
    var dict = {};
    for (var i = 0; i < keyList.length; i++) {
        dict[keyList[i]] = {
            name: keyList[i],
            datapoints: []
        };
    }

    return dict;
}

angular.module('MachineInfo.services', [])
    //存储全局state变量
    .value('stateValue', {
        realTime: true,
        operatorCount: 0,
        selectedMachine: null,
        end_date: null,
        begin_date: null
    })
    .value('stateValueCompare', {
        isSearch: false,
        selectedMachine: [],
        end_date: null,
        begin_date: null
    })
    .value('cpuInfo', {
        percentage: generateDataPoints(["user","nice", "system", "idle",
         "iowait", "irq", "softirq", "steal", "guest", "guest_nice" ]),
        graphWidth: 20,
        //加载单次数据,当数据数组长度超过graphwidth,
        //移除最早的数据, 使得动态加载时保持固定展示长度
        load: function(data) {
            // console.log(percentage);
            userPoint = this.percentage.user.datapoints;
            if (userPoint.length == 0 || data.time.localeCompare(
                    userPoint[userPoint.length - 1].x)) {
                for (var key in data) {
                    if (key == "time")
                        continue;
                    percentagePoint = this.percentage[key].datapoints;
                    percentagePoint.push({
                        x: data["time"],
                        y: data[key]
                    });
                    if (percentagePoint.length > this.graphWidth)
                        percentagePoint.shift();
                }
            }
        },
        // 使用新的数据数组进行初始化
        reInit: function(data) {
            for (var key in this.percentage)
                this.percentage[key].datapoints.length = 0;
            for (var i = 0; i < data.length; i++) {
                for (var key in data[i]) {
                    if (key == "time")
                        continue;
                    percentagePoint = this.percentage[key].datapoints;
                    percentagePoint.push({
                        x: data[i]["time"],
                        y: data[i][key]
                    });
                }
            }
        },
        // 清空数据
        clear: function() {
            for (var key in this.percentage)
                this.percentage[key].datapoints.length = 0;
        }
    })
    .value('memoryInfo', {
        usage: generateDataPoints(["total", "used", "abs_used", "free",
            "buffers", "cached", "active", "inactive", "swap_used"]),
        graphWidth: 20,
        //加载单次数据,当数据数组长度超过graphwidth,
        //移除最早的数据, 使得动态加载时保持固定展示长度
        load: function(data) {
            totalPoint = this.usage.total.datapoints;
            if (totalPoint.length == 0 || data.time.localeCompare(
                    totalPoint[totalPoint.length - 1].x)) {
                for (var key in data) {
                    if (key == "time")
                        continue;
                    usagePoint = this.usage[key].datapoints;
                    usagePoint.push({
                        x: data["time"],
                        y: (data[key] / (1024 * 1024)).toFixed(3)
                    });
                    if (usagePoint.length > this.graphWidth)
                        usagePoint.shift();
                }
            }
        },
        // 使用新的数据数组进行初始化
        reInit: function(data) {
            for (var key in this.usage)
                this.usage[key].datapoints.length = 0;
            for (var i = 0; i < data.length; i++) {
                for (var key in data[i]) {
                    if (key == "time")
                        continue;
                    usagePoint = this.usage[key].datapoints;
                    usagePoint.push({
                        x: data[i]["time"],
                        y: (data[i][key] / (1024 * 1024)).toFixed(3)
                    });
                }
            }
        },
        // 清空数据
        clear: function() {
            for (var key in this.usage)
                this.usage[key].datapoints.length = 0;
        }
    })
    .value('averageLoadInfo', {
        w1Avg: {
            name: "average load 1",
            datapoints: []
        },
        w2Avg: {
            name: "average load 5",
            datapoints: []
        },
        w3Avg: {
            name: "average load 15",
            datapoints: []
        },
        graphWidth: 20,
        //加载单次数据,当数据数组长度超过graphwidth,
        //移除最早的数据, 使得动态加载时保持固定展示长度
        load: function(data) {
            w1Point = this.w1Avg.datapoints;
            w2Point = this.w2Avg.datapoints;
            w3Point = this.w3Avg.datapoints;
            if (w1Point.length == 0 || data.time.localeCompare(
                    w1Point[w1Point.length - 1].x)) {
                w1Point.push({
                    x: data["time"],
                    y: data["w1_avg"]
                });
                w2Point.push({
                    x: data["time"],
                    y: data["w2_avg"]
                });
                w3Point.push({
                    x: data["time"],
                    y: data["w3_avg"]
                });
                if (w1Point.length > this.graphWidth) {
                    w1Point.shift();
                    w2Point.shift();
                    w3Point.shift();
                }
            }
        },
        // 使用新的数据数组进行初始化
        reInit: function(data) {
            w1Point = this.w1Avg.datapoints;
            w2Point = this.w2Avg.datapoints;
            w3Point = this.w3Avg.datapoints;
            w1Point.length = 0;
            w2Point.length = 0;
            w3Point.length = 0;
            for (var i = 0; i < data.length; i++) {
                w1Point.push({
                    x: data[i]["time"],
                    y: data[i]["w1_avg"]
                });
                w2Point.push({
                    x: data[i]["time"],
                    y: data[i]["w2_avg"]
                });
                w3Point.push({
                    x: data[i]["time"],
                    y: data[i]["w3_avg"]
                });
            }
        },
        // 清空数据
        clear: function() {
            this.w1Avg.datapoints.length = 0;
            this.w2Avg.datapoints.length = 0;
            this.w3Avg.datapoints.length = 0;
        }
    })
    .value('averageLoadCompareInfo', {
        w1Avg: [],
        w2Avg: [],
        w3Avg: [],
        append: function(machine, data) {
            this.w1Avg.push({
                name: machine,
                datapoints: []
            });
            this.w2Avg.push({
                name: machine,
                datapoints: []
            });
            this.w3Avg.push({
                name: machine,
                datapoints: []
            });
            w1Point = this.w1Avg[this.w1Avg.length - 1].datapoints;
            w2Point = this.w2Avg[this.w2Avg.length - 1].datapoints;
            w3Point = this.w3Avg[this.w3Avg.length - 1].datapoints;
            for (var i = 0; i < data.length; i++) {
                w1Point.push({
                    x: data[i]["time"],
                    y: data[i]["w1_avg"]
                });
                w2Point.push({
                    x: data[i]["time"],
                    y: data[i]["w2_avg"]
                });
                w3Point.push({
                    x: data[i]["time"],
                    y: data[i]["w3_avg"]
                });
            }
        },
        clear: function() {
            this.w1Avg = [];
            this.w2Avg = [];
            this.w3Avg = [];
        },
        empty: function() {
            if (this.w1Avg.length == 0 && this.w2Avg.length == 0 &&
                this.w3Avg.length == 0) {
                return true;
            }
            return false;
        }
    })
    .value('netInfo', {
        sentRate: {
            name: "sent rate",
            datapoints: []
        },
        recvRate: {
            name: "recv rate",
            datapoints: []
        },
        graphWidth: 20,
        //加载单次数据,当数据数组长度超过graphwidth,
        //移除最早的数据, 使得动态加载时保持固定展示长度
        load: function(data) {
            sentPoint = this.sentRate.datapoints;
            recvPoint = this.recvRate.datapoints;
            if (sentPoint.length == 0 || data.time.localeCompare(
                    sentPoint[sentPoint.length - 1].x)) {
                sentPoint.push({
                    x: data["time"],
                    y: (data["t_sent_rate"] / 1024).toFixed(3)
                });
                recvPoint.push({
                    x: data["time"],
                    y: (data["t_recv_rate"] / 1024).toFixed(3)
                });
                if (sentPoint.length > this.graphWidth) {
                    sentPoint.shift();
                    recvPoint.shift();
                }
            }
        },
        // 使用新的数据数组进行初始化
        reInit: function(data) {
            sentPoint = this.sentRate.datapoints;
            recvPoint = this.recvRate.datapoints;
            sentPoint.length = 0;
            recvPoint.length = 0;
            for (var i = 0; i < data.length; i++) {
                sentPoint.push({
                    x: data[i]["time"],
                    y: (data[i]["t_sent_rate"] / 1024).toFixed(3)
                });
                recvPoint.push({
                    x: data[i]["time"],
                    y: (data[i]["t_recv_rate"] / 1024).toFixed(3)
                });
            }
        },
        // 清空数据
        clear: function() {
            this.sentRate.datapoints.length = 0;
            this.recvRate.datapoints.length = 0;
        }
    })
    .value('netCompareInfo', {
        sentRate: [],
        recvRate: [],
        append: function(machine, data) {
            this.sentRate.push({
                name: machine,
                datapoints: []
            });
            this.recvRate.push({
                name: machine,
                datapoints: []
            });
            readPoint = this.sentRate[this.sentRate.length - 1].datapoints;
            writePoint = this.recvRate[this.recvRate.length - 1].datapoints;
            for (var i = 0; i < data.length; i++) {
                readPoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_sent_rate"]
                });
                writePoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_recv_rate"]
                });
            }
        },
        clear: function() {
            this.sentRate = [];
            this.recvRate = [];
        },
        empty: function() {
            if (this.sentRate.length == 0 && this.recvRate.length == 0) {
                return true;
            }
            return false;
        }
    })
    .value('diskRate', {
        readRate: {
            name: "read rate",
            datapoints: []
        },
        writeRate: {
            name: "write rate",
            datapoints: []
        },
        graphWidth: 20,
        //加载单次数据,当数据数组长度超过graphwidth,
        //移除最早的数据, 使得动态加载时保持固定展示长度
        load: function(data) {
            readPoint = this.readRate.datapoints;
            writePoint = this.writeRate.datapoints;
            if (readPoint.length == 0 || data.time.localeCompare(
                    readPoint[readPoint.length - 1].x)) {
                readPoint.push({
                    x: data["time"],
                    y: (data["t_read_rate"] / 1024).toFixed(3)
                });
                writePoint.push({
                    x: data["time"],
                    y: (data["t_write_rate"] / 1024).toFixed(3)
                });
                if (readPoint.length > this.graphWidth) {
                    readPoint.shift();
                    writePoint.shift();
                }
            }
        },
        // 使用新的数据数组进行初始化
        reInit: function(data) {
            readPoint = this.readRate.datapoints;
            writePoint = this.writeRate.datapoints;
            readPoint.length = 0;
            writePoint.length = 0;
            for (var i = 0; i < data.length; i++) {
                readPoint.push({
                    x: data[i]["time"],
                    y: (data[i]["t_read_rate"] / 1024).toFixed(3)
                });
                writePoint.push({
                    x: data[i]["time"],
                    y: (data[i]["t_write_rate"] / 1024).toFixed(3)
                });
            }
        },
        // 清空数据
        clear: function() {
            this.readRate.datapoints.length = 0;
            this.writeRate.datapoints.length = 0;
        }
    })
    .value('diskRateCompare', {
        readRate: [],
        writeRate: [],
        append: function(machine, data) {
            this.readRate.push({
                name: machine,
                datapoints: []
            });
            this.writeRate.push({
                name: machine,
                datapoints: []
            });
            readPoint = this.readRate[this.readRate.length - 1].datapoints;
            writePoint = this.writeRate[this.writeRate.length - 1].datapoints;
            for (var i = 0; i < data.length; i++) {
                readPoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_read_rate"]
                });
                writePoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_write_rate"]
                });
            }
        },
        clear: function() {
            this.readRate = [];
            this.writeRate = [];
        },
        empty: function() {
            if (this.readRate.length == 0 && this.writeRate.length == 0) {
                return true;
            }
            return false;
        }
    })
    .value('diskUsage', {
        total: {
            name: "total",
            datapoints: []
        },
        used: {
            name: "used",
            datapoints: []
        },
        free: {
            name: "free",
            datapoints: []
        },
        graphWidth: 20,
        //加载单次数据,当数据数组长度超过graphwidth,
        //移除最早的数据, 使得动态加载时保持固定展示长度
        load: function(data) {
            totalPoint = this.total.datapoints;
            usedPoint = this.used.datapoints;
            freePoint = this.free.datapoints;
            if (totalPoint.length == 0 || data.time.localeCompare(
                    totalPoint[totalPoint.length - 1].x)) {
                totalPoint.push({
                    x: data["time"],
                    y: (data["t_cap"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                usedPoint.push({
                    x: data["time"],
                    y: (data["t_used"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                freePoint.push({
                    x: data["time"],
                    y: (data["t_free"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                if (totalPoint.length > this.graphWidth) {
                    totalPoint.shift();
                    usedPoint.shift();
                    freePoint.shift();
                }
            }
        },
        // 使用新的数据数组进行初始化
        reInit: function(data) {
            totalPoint = this.total.datapoints;
            usedPoint = this.used.datapoints;
            freePoint = this.free.datapoints;
            totalPoint.length = 0;
            usedPoint.length = 0;
            freePoint.length = 0;
            for (var i = 0; i < data.length; i++) {
                totalPoint.push({
                    x: data[i]["time"],
                    y: (data[i]["t_cap"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                usedPoint.push({
                    x: data[i]["time"],
                    y: (data[i]["t_used"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                freePoint.push({
                    x: data[i]["time"],
                    y: (data["t_free"] / (1024 * 1024 * 1024)).toFixed(3)
                });
            }
        },
        // 清空数据
        clear: function() {
            this.total.datapoints.length = 0;
            this.used.datapoints.length = 0;
            this.free.datapoints.length = 0;
        }
    })
    //定义后台数据交互服务
    .service('dataFactory', ['$http', function($http) {
        //数据api url
        var urlBase = "http://123.58.165.132:8888";

        // 获取机器信息列表 
        this.getMachines = function() {
            return $http.get(urlBase + "/monitor/api/machines");
        };

        //获取单个机器最新信息
        this.getMachine = function(machineUrl) {
            return $http.get(urlBase + machineUrl);
        }

        //获得单个模块指定日期区间的数据
        this.getModule = function(machineUrl, module,
            beginDate, endDate) {
            targetUrl = urlBase + machineUrl + "/search?module=" +
                module + "&begin_date=" +
                beginDate.format("isoDateTime").replace(/T/g, " ") +
                "&end_date=" + endDate.format("isoDateTime").replace(/T/g, " ");
            return $http.get(targetUrl);
        }
    }]);
