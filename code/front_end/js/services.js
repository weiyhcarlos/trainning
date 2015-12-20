/**
 *  Module
 *
 * Description
 */
angular.module('MachineInfo.services', [])
    .value('stateValue', {
        realTime: true,
        operatorCount: 0,
        selectedMachine: null,
        end_date: null,
        begin_date: null
    })
    .value('cpuInfo', {
        percentage: {
            user: {
                name: "user",
                datapoints: []
            },
            nice: {
                name: "nice",
                datapoints: []
            },
            system: {
                name: "system",
                datapoints: []
            },
            idle: {
                name: "idle",
                datapoints: []
            },
            iowait: {
                name: "iowait",
                datapoints: []
            },
            irq: {
                name: "irq",
                datapoints: []
            },
            softirq: {
                name: "softirq",
                datapoints: []
            },
            steal: {
                name: "steal",
                datapoints: []
            },
            guest: {
                name: "guest",
                datapoints: []
            },
            guest_nice: {
                name: "guest_nice",
                datapoints: []
            }
        },
        graphWidth: 20,
        load: function(data) {
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
            console.log(this.percentage);
        },
        clear: function() {
            for (var key in this.percentage)
                this.percentage[key].datapoints.length = 0;
        }
    })
    .value('memoryInfo', {
        usage: {
            total: {
                name: "total",
                datapoints: []
            },
            used: {
                name: "used",
                datapoints: []
            },
            abs_used: {
                name: "abs_used",
                datapoints: []
            },
            free: {
                name: "free",
                datapoints: []
            },
            buffers: {
                name: "buffers",
                datapoints: []
            },
            cached: {
                name: "cached",
                datapoints: []
            },
            active: {
                name: "active",
                datapoints: []
            },
            inactive: {
                name: "inactive",
                datapoints: []
            },
            swap_used: {
                name: "swap_used",
                datapoints: []
            }
        },
        graphWidth: 20,
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
                        y: data[key]
                    });
                    if (usagePoint.length > this.graphWidth)
                        usagePoint.shift();
                }
            }
        },
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
                        y: data[i][key]
                    });
                }
            }
            console.log(this.usage);
        },
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
        clear: function() {
            this.w1Avg.datapoints.length = 0;
            this.w2Avg.datapoints.length = 0;
            this.w3Avg.datapoints.length = 0;
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
        load: function(data) {
            sentPoint = this.sentRate.datapoints;
            recvPoint = this.recvRate.datapoints;
            if (sentPoint.length == 0 || data.time.localeCompare(
                    sentPoint[sentPoint.length - 1].x)) {
                sentPoint.push({
                    x: data["time"],
                    y: data["t_sent_rate"]
                });
                recvPoint.push({
                    x: data["time"],
                    y: data["t_recv_rate"]
                });
                if (sentPoint.length > this.graphWidth) {
                    sentPoint.shift();
                    recvPoint.shift();
                }
            }
        },
        reInit: function(data) {
            sentPoint = this.sentRate.datapoints;
            recvPoint = this.recvRate.datapoints;
            sentPoint.length = 0;
            recvPoint.length = 0;
            for (var i = 0; i < data.length; i++) {
                sentPoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_sent_rate"]
                });
                recvPoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_recv_rate"]
                });
            }
        },
        clear: function() {
            this.sentRate.datapoints.length = 0;
            this.recvRate.datapoints.length = 0;
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
        load: function(data) {
            readPoint = this.readRate.datapoints;
            writePoint = this.writeRate.datapoints;
            if (readPoint.length == 0 || data.time.localeCompare(
                    readPoint[readPoint.length - 1].x)) {
                readPoint.push({
                    x: data["time"],
                    y: data["t_read_rate"]
                });
                writePoint.push({
                    x: data["time"],
                    y: data["t_write_rate"]
                });
                if (readPoint.length > this.graphWidth) {
                    readPoint.shift();
                    writePoint.shift();
                }
            }
        },
        reInit: function(data) {
            readPoint = this.readRate.datapoints;
            writePoint = this.writeRate.datapoints;
            readPoint.length = 0;
            writePoint.length = 0;
            for (var i = 0; i < data.length; i++) {
                readPoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_read_rate"]
                });
                writePoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_read_rate"]
                });
            }
        },
        clear: function() {
            this.readRate.datapoints.length = 0;
            this.writeRate.datapoints.length = 0;
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
        load: function(data) {
            totalPoint = this.total.datapoints;
            usedPoint = this.used.datapoints;
            freePoint = this.free.datapoints;
            if (totalPoint.length == 0 || data.time.localeCompare(
                    totalPoint[totalPoint.length - 1].x)) {
                totalPoint.push({
                    x: data["time"],
                    y: data["t_cap"]
                });
                usedPoint.push({
                    x: data["time"],
                    y: data["t_used"]
                });
                freePoint.push({
                    x: data["time"],
                    y: data["t_free"]
                });
                if (totalPoint.length > this.graphWidth) {
                    totalPoint.shift();
                    usedPoint.shift();
                    freePoint.shift();
                }
            }
        },
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
                    y: data[i]["t_cap"]
                });
                usedPoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_used"]
                });
                freePoint.push({
                    x: data[i]["time"],
                    y: data[i]["t_free"]
                });
            }
        },
        clear: function() {
            this.total.datapoints.length = 0;
            this.used.datapoints.length = 0;
            this.free.datapoints.length = 0;
        }
    })
    .service('dataFactory', ['$http', function($http) {
        var urlBase = "http://test.com:8888";

        this.getMachines = function() {
            return $http.get(urlBase + "/monitor/api/machines");
        };

        this.getMachine = function(machineUrl) {
            return $http.get(urlBase + machineUrl);
        }

        this.getModule = function(machineUrl, module, beginDate, endDate) {
            console.log(beginDate.format("isoDateTime"), endDate.format("isoDateTime"));
            targetUrl = urlBase + machineUrl + "/search?module=" + module + "&begin_date=" + beginDate.format("isoDateTime").replace(/T/g, " ") + "&end_date=" +
                endDate.format("isoDateTime").replace(/T/g, " ");
            console.log(targetUrl);
            return $http.get(targetUrl);
        }
    }]);
