angular.module('MachineInfo.directives', [])
    .directive('myCurrentTime', ['$interval', 'dateFilter',
        function($interval, dateFilter) {
            // return the directive link function
            return function(scope, element, attrs) {
                var format = "M/d/yy h:mm:ss a", // date format
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
