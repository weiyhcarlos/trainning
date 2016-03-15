/**
 * 指令模块,自定义指令
 */
angular.module('MachineInfo.directives', [])
    //实时更新时间指令
    .directive('myCurrentTime', ['$interval', 'dateFilter',
        function($interval, dateFilter) {
            // r返回指令Link 函数
            return function(scope, element, attrs) {
                var format = "M/d/yy h:mm:ss a",
                    stopTime;
                function updateTime() {
                    element.text(dateFilter(new Date(), format));
                }
                stopTime = $interval(updateTime, 1000);
                element.on('$destroy', function() {
                    $interval.cancel(stopTime);
                });
            }
        }
    ]);
