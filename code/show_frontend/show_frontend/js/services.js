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
        isFirst: true,
        selectedMachine: [],
        end_date: null,
        begin_date: null
    })

.value('singlePageInfo', {
        // cpu info
        percentage: generateDataPoints(["user", "nice", "system", "idle",
            "iowait", "irq", "softirq", "steal", "guest", "guest_nice"
        ]),

        //memory info
        usage: generateDataPoints(["total", "used", "abs_used", "free",
            "buffers", "cached", "active", "inactive", "swap_used"
        ]),

        // average load info
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

        // net info
        sentRate: {
            name: "sent rate",
            datapoints: []
        },
        recvRate: {
            name: "recv rate",
            datapoints: []
        },

        // disk rate info
        readRate: {
            name: "read rate",
            datapoints: []
        },
        writeRate: {
            name: "write rate",
            datapoints: []
        },

        // disk usage info
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

        graphWidth: 15,
        //加载单次数据,当数据数组长度超过graphwidth,
        //移除最早的数据, 使得动态加载时保持固定展示长度
        load: function(data) {
            cpuData = data.cpu;
            memoryData = data.memory;
            averageLoadData = data.average_load;
            diskData = data.disk;
            netData = data.net;

            // cpu load
            userPoint = this.percentage.user.datapoints;

            if (userPoint.length == 0 || cpuData.time.localeCompare(
                    userPoint[userPoint.length - 1].x)) {
                for (var key in cpuData) {
                    if (key == "time")
                        continue;
                    percentagePoint = this.percentage[key].datapoints;
                    percentagePoint.push({
                        x: cpuData["time"],
                        y: cpuData[key]
                    });
                    if (percentagePoint.length > this.graphWidth)
                        percentagePoint.shift();
                }
            }

            // memory load
            totalPoint = this.usage.total.datapoints;
            if (totalPoint.length == 0 || memoryData.time.localeCompare(
                    totalPoint[totalPoint.length - 1].x)) {
                for (var key in memoryData) {
                    if (key == "time")
                        continue;
                    usagePoint = this.usage[key].datapoints;
                    usagePoint.push({
                        x: memoryData["time"],
                        y: (memoryData[key] / (1024 * 1024)).toFixed(3)
                    });
                    if (usagePoint.length > this.graphWidth)
                        usagePoint.shift();
                }
            }

            // average_load load
            w1Point = this.w1Avg.datapoints;
            w2Point = this.w2Avg.datapoints;
            w3Point = this.w3Avg.datapoints;
            if (w1Point.length == 0 || averageLoadData.time.localeCompare(
                    w1Point[w1Point.length - 1].x)) {
                w1Point.push({
                    x: averageLoadData["time"],
                    y: averageLoadData["w1_avg"]
                });
                w2Point.push({
                    x: averageLoadData["time"],
                    y: averageLoadData["w2_avg"]
                });
                w3Point.push({
                    x: averageLoadData["time"],
                    y: averageLoadData["w3_avg"]
                });
                if (w1Point.length > this.graphWidth) {
                    w1Point.shift();
                    w2Point.shift();
                    w3Point.shift();
                }
            }

            // net load
            sentPoint = this.sentRate.datapoints;
            recvPoint = this.recvRate.datapoints;
            if (sentPoint.length == 0 || netData.time.localeCompare(
                    sentPoint[sentPoint.length - 1].x)) {
                sentPoint.push({
                    x: netData["time"],
                    y: (netData["t_sent_rate"] / 1024).toFixed(3)
                });
                recvPoint.push({
                    x: netData["time"],
                    y: (netData["t_recv_rate"] / 1024).toFixed(3)
                });
                if (sentPoint.length > this.graphWidth) {
                    sentPoint.shift();
                    recvPoint.shift();
                }
            }

            //disk rate load
            readPoint = this.readRate.datapoints;
            writePoint = this.writeRate.datapoints;
            if (readPoint.length == 0 || diskData.time.localeCompare(
                    readPoint[readPoint.length - 1].x)) {
                readPoint.push({
                    x: diskData["time"],
                    y: (diskData["t_read_rate"] / 1024).toFixed(3)
                });
                writePoint.push({
                    x: diskData["time"],
                    y: (diskData["t_write_rate"] / 1024).toFixed(3)
                });
                if (readPoint.length > this.graphWidth) {
                    readPoint.shift();
                    writePoint.shift();
                }
            }

            //disk usage load
            totalPoint = this.total.datapoints;
            usedPoint = this.used.datapoints;
            freePoint = this.free.datapoints;
            if (totalPoint.length == 0 || diskData.time.localeCompare(
                    totalPoint[totalPoint.length - 1].x)) {
                totalPoint.push({
                    x: diskData["time"],
                    y: (diskData["t_cap"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                usedPoint.push({
                    x: diskData["time"],
                    y: (diskData["t_used"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                freePoint.push({
                    x: diskData["time"],
                    y: (diskData["t_free"] / (1024 * 1024 * 1024)).toFixed(3)
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
            cpuData = data.cpu;
            memoryData = data.memory;
            averageLoadData = data.average_load;
            diskData = data.disk;
            netData = data.net;

            // cpu reInit
            for (var key in this.percentage)
                this.percentage[key].datapoints.length = 0;
            for (var i = 0; i < cpuData.length; i++) {
                for (var key in cpuData[i]) {
                    if (key == "time")
                        continue;
                    percentagePoint = this.percentage[key].datapoints;
                    percentagePoint.push({
                        x: cpuData[i]["time"],
                        y: cpuData[i][key]
                    });
                }
            }

            // memory reInit
            for (var key in this.usage)
                this.usage[key].datapoints.length = 0;
            for (var i = 0; i < memoryData.length; i++) {
                for (var key in memoryData[i]) {
                    if (key == "time")
                        continue;
                    usagePoint = this.usage[key].datapoints;
                    usagePoint.push({
                        x: memoryData[i]["time"],
                        y: (memoryData[i][key] / (1024 * 1024)).toFixed(3)
                    });
                }
            }
            //average_load reInit
            w1Point = this.w1Avg.datapoints;
            w2Point = this.w2Avg.datapoints;
            w3Point = this.w3Avg.datapoints;
            w1Point.length = 0;
            w2Point.length = 0;
            w3Point.length = 0;
            for (var i = 0; i < averageLoadData.length; i++) {
                w1Point.push({
                    x: averageLoadData[i]["time"],
                    y: averageLoadData[i]["w1_avg"]
                });
                w2Point.push({
                    x: averageLoadData[i]["time"],
                    y: averageLoadData[i]["w2_avg"]
                });
                w3Point.push({
                    x: averageLoadData[i]["time"],
                    y: averageLoadData[i]["w3_avg"]
                });
            }

            // net reInit
            sentPoint = this.sentRate.datapoints;
            recvPoint = this.recvRate.datapoints;
            sentPoint.length = 0;
            recvPoint.length = 0;
            for (var i = 0; i < netData.length; i++) {
                sentPoint.push({
                    x: netData[i]["time"],
                    y: (netData[i]["t_sent_rate"] / 1024).toFixed(3)
                });
                recvPoint.push({
                    x: netData[i]["time"],
                    y: (netData[i]["t_recv_rate"] / 1024).toFixed(3)
                });
            }

            //disk rate reInit
            readPoint = this.readRate.datapoints;
            writePoint = this.writeRate.datapoints;
            readPoint.length = 0;
            writePoint.length = 0;
            for (var i = 0; i < diskData.length; i++) {
                readPoint.push({
                    x: diskData[i]["time"],
                    y: (diskData[i]["t_read_rate"] / 1024).toFixed(3)
                });
                writePoint.push({
                    x: diskData[i]["time"],
                    y: (diskData[i]["t_write_rate"] / 1024).toFixed(3)
                });
            }

            // disk usage reInit
            totalPoint = this.total.datapoints;
            usedPoint = this.used.datapoints;
            freePoint = this.free.datapoints;
            totalPoint.length = 0;
            usedPoint.length = 0;
            freePoint.length = 0;
            for (var i = 0; i < diskData.length; i++) {
                totalPoint.push({
                    x: diskData[i]["time"],
                    y: (diskData[i]["t_cap"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                usedPoint.push({
                    x: diskData[i]["time"],
                    y: (diskData[i]["t_used"] / (1024 * 1024 * 1024)).toFixed(3)
                });
                freePoint.push({
                    x: diskData[i]["time"],
                    y: (diskData["t_free"] / (1024 * 1024 * 1024)).toFixed(3)
                });
            }
        },
        // 清空数据
        clear: function() {
            for (var key in this.percentage)
                this.percentage[key].datapoints.length = 0;
            for (var key in this.usage)
                this.usage[key].datapoints.length = 0;
            this.w1Avg.datapoints.length = 0;
            this.w2Avg.datapoints.length = 0;
            this.w3Avg.datapoints.length = 0;
            this.w1Avg.datapoints.length = 0;
            this.w2Avg.datapoints.length = 0;
            this.w3Avg.datapoints.length = 0;
            this.sentRate.datapoints.length = 0;
            this.recvRate.datapoints.length = 0;
            this.readRate.datapoints.length = 0;
            this.writeRate.datapoints.length = 0;
            this.total.datapoints.length = 0;
            this.used.datapoints.length = 0;
            this.free.datapoints.length = 0;
        }
    })
    .value('comparePageInfo', {
        // average_load
        w1Avg: [],
        w2Avg: [],
        w3Avg: [],
        // net
        sentRate: [],
        recvRate: [],

        //disk rate
        readRate: [],
        writeRate: [],

        append: function(machine, data) {
            averageLoadData = data.average_load;
            netData = data.net;
            diskData = data.disk;

            // average_load append
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
            for (var i = 0; i < averageLoadData.length; i++) {
                w1Point.push({
                    x: averageLoadData[i]["time"],
                    y: averageLoadData[i]["w1_avg"]
                });
                w2Point.push({
                    x: averageLoadData[i]["time"],
                    y: averageLoadData[i]["w2_avg"]
                });
                w3Point.push({
                    x: averageLoadData[i]["time"],
                    y: averageLoadData[i]["w3_avg"]
                });
            }

            // net append
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
            for (var i = 0; i < netData.length; i++) {
                readPoint.push({
                    x: netData[i]["time"],
                    y: netData[i]["t_sent_rate"]
                });
                writePoint.push({
                    x: netData[i]["time"],
                    y: netData[i]["t_recv_rate"]
                });
            }

            //disk rate append
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
            for (var i = 0; i < diskData.length; i++) {
                readPoint.push({
                    x: diskData[i]["time"],
                    y: diskData[i]["t_read_rate"]
                });
                writePoint.push({
                    x: diskData[i]["time"],
                    y: diskData[i]["t_write_rate"]
                });
            }
        },
        clear: function() {
            this.w1Avg = [];
            this.w2Avg = [];
            this.w3Avg = [];
            this.sentRate = [];
            this.recvRate = [];
            this.readRate = [];
            this.writeRate = [];
        },
        empty: function() {
            if (this.w1Avg.length == 0 && this.w2Avg.length == 0 &&
                this.w3Avg.length == 0 && this.sentRate.length == 0 &&
                this.recvRate.length == 0 && this.readRate.length == 0 && this.writeRate.length == 0) {
                return true;
            }
            return false;
        }
    })
    //定义后台数据交互服务
    .service('dataFactory', ['$http', function($http) {
        //数据api url
        // var urlBase = "http://123.58.165.132:8888";
        var urlBase = "http://localhost:8888";
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
