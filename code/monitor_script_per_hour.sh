#!/bin/bash

#分析日志,格式为以"|"分割的14个字段
#分析每台主机每个接口的每个小时的访问量及平均响应时间(当前时间之前一个小时内)
#最近一个小时内，当访问量不超过5，打印警告，平均响应时间超过500ms，打印警告
#如果访问量及平均响应时间由警告恢复正常，打印恢复信息

#警告信息及恢复信息
RESPONSE_ALARM_MESSAGE="The average response time is more than 500ms. now is: "
RESPONSE_RECOVER_MESSAGE="the average response time return to normal, now is: "
VISIT_ALARM_MESSAGE="the visit is no more than 5 times per hour. now is: "
VISIT_RECOVER_MESSAGE="the visit return to normal. now is: "

#上次处理时日志的行数
PRE_LINE_NUM=0

#声明数组存储接口响应时间和访问次数
declare -A totalResponseTime
declare -A totalVisit

#声明数组存储接口报警信息，值为true或false
declare -A isAlarmByMuchResponseTime
declare -A isAlarmByFewVisitTime

#取得日志文件名
if [ -n "$1" ]
  then LOG_FILE=$1
else
  echo "please input the log file name!"
  exit 1
fi

#处理日志文件的每一行，保存相应信息
handle_log_line() {
    #处理得到接口标志（接口名和功能号），响应时间
    interface=$(echo $1 | awk -F '|' '{printf("%s %s",$4,$5)}')
    time=$(echo $1 | awk -F '|' '{print $13}')

    #echo $interface ":"

    #得到最近一小时内的各接口的访问次数和响应时间
    if [ -z "${totalResponseTime[$interface]}" ]; then
      totalResponseTime[$interface]=$time
      totalVisit[$interface]=1
      if [ -z "${isAlarmByMuchResponseTime[$interface]}" ]; then
        isAlarmByMuchResponseTime[$interface]=false
      fi
      if [ -z "${isAlarmByFewVisitTime[$interface]}" ]; then
        isAlarmByFewVisitTime[$interface]=false
      fi
    else
      let totalResponseTime[$interface]+=$time
      let totalVisit[$interface]++
    fi
    #echo ${totalResponseTime[$interface]}, ${totalVisit[$interface]}, \
    #${isAlarmByMuchResponseTime[$interface]}, \
    #${isAlarmByFewVisitTime[$interface]}
}

#判断接口是否上次报警，判断需不需要打印报警信息或者恢复信息
update_message() {
    #echo "*********begin update message*********"
    #处理响应时间
    for i in "${!totalResponseTime[@]}"; do
        average_response=$((${totalResponseTime[$i]} / ${totalVisit[$i]}))
        #echo $i,$average_response, ${isAlarmByMuchResponseTime[$i]}
        if [ "${isAlarmByMuchResponseTime[$i]}" = false -a \
            $average_response -ge 500 ]; then
          echo $RESPONSE_ALARM_MESSAGE $i $average_response "ms"
          isAlarmByMuchResponseTime[$i]=true
        elif [ "${isAlarmByMuchResponseTime[$i]}" = true -a \
            $average_response -lt 500 ]; then
          echo $RESPONSE_RECOVER_MESSAGE $i $average_response "ms"
          isAlarmByMuchResponseTime[$i]=false
        fi
    done
    #处理访问次数
    for i in "${!totalVisit[@]}"; do
        if [ "${isAlarmByFewVisitTime[$i]}" = false -a \
            ${totalVisit[$i]} -le 5 ]; then
          echo $VISIT_ALARM_MESSAGE $i ${totalVisit[$i]} "times"
          isAlarmByFewVisitTime[$i]=true
        elif [ "${isAlarmByFewVisitTime[$i]}" = true -a \
            ${totalVisit[$i]} -gt 5 ]; then
          echo $VISIT_RECOVER_MESSAGE $i ${totalVisit[$i]} "times"
          isAlarmByFewVisitTime[$i]=false
        fi
    done
}


#更新接口平均响应时间并判断是否需要打印信息
update_log() {
  unset totalResponseTime
  unset totalVisit

  declare -A totalResponseTime
  declare -A totalVisit

  last_hour_date=$(date -d "last-hour" "+%Y%m%d %H%M%S")
  #echo last_hour_date, $last_hour_date
  IFS=$'\n'
  for line in `echo "$(cat $LOG_FILE)" | \
      awk -v var="$last_hour_date" -F '|' '{if($1>var)print $0}'`
  do
    handle_log_line "$line"
  done
  update_message
}

#如有新增日志，进行处理
if [[ -f "$LOG_FILE" ]]; then
  while true; do
    line_num=`cat $LOG_FILE | wc -l`
    if [ $line_num -gt $PRE_LINE_NUM ]; then
      update_log
      PRE_LINE_NUM=$line_num
    fi
    sleep 1
  done
else
  echo "log file doesn't exist!"
  exit 1
fi
