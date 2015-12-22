# stage2 web设计

## 一.使用技术
后端:Flask提供Restful API  
前端:angularJS, bootstrap  

    Flask开发依赖:
    flask  
    flask-restful
    pymongo
    uwsgi
    //redis
部署:  
前端(nginx+angularJS)  
后端(nginx+uwsgi+flask)

## 二.规范
[flask pocoo风格][1]  
[HTTP status code][2]  
python命名:  
module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.  
JS命名:  
functionNamesLikeThis, variableNamesLikeThis, ClassNamesLikeThis, EnumNamesLikeThis, methodNamesLikeThis, 和 SYMBOLIC_CONSTANTS_LIKE_THIS.

## 三.数据库设计
    machine集合:
    {  
        "_id":"00:00:00:00:00:00",#MAC
        "cluster":`xxx`,
        "ip":"1.1.1.1",
        "hostname":"XXX"
    }

    cpu集合:
    {
        "_id":objectId(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "user":0,
        "nice":0,
        "system":0,
        "idle":0,
        "iowait":0,
        "irq":0,
        "softirq":0,
        "steal":0,
        "guest":0,
        "guest_nice":0
    }
    
    memory集合:
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "total":100,
        "used":100,
        "abs_used":100,
        "free":100,
        "buffers":100,
        "cached":100,
        "active":100,
        "inactive":100,
        "swap_used":100
    }
    
    disk集合:
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "t_cap":100,
        "t_used":100,
        "t_free":100,
        "t_read_rate":100,
        "t_write_rate":100,
        "per_disk_info":[
            {
                "disk_name":"sda1",
                "cap":1000,
                "used":100,
                "free":100,
                "read_rate":1,
                "write_rate":1,
            },
            {
                ...
            }
            ...
        ]
    }
    
    net集合:
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"，
        "t_sent_rate":200,
        "t_recv_rate":200,
        "per_net_info":[
            {
                "net_name":"eth0",
                "sent_rate":100,
                "recv_rate":100
            },
            {
                ...
            }
            ...
        ]
    }
    
    average_load集合: 
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "w1_avg": 0.22, 
        "w2_avg": 0.44, 
        "w3_avg": 0.53
    }
    
## 四.restful API设计(后端)
+ `/monitor/api/machines`  
说明:返回所有机器的基本信息  
请求方法: GET  
请求参数:  
无  
响应数据(成功):  

        Status: 200 OK
        [
                {
                    "mac":"00:00:00:00:00:00",
                    "cluster":`xxx`,
                    "ip":"1.1.1.1",
                    "hostname":"XXX",
                    "url":"/monitor/api/machines/:id"
                },
                {
                    ...
                },
                ...
        ]


+ `/monitor/api/machines/:id`  
说明:返回指定ID机器的最新收集信息  
请求方法: GET  
请求参数:  
无  
响应数据(成功):  

        Status: 200 OK
        {
            "mac":"00:00:00:00:00:00",
            "cluster":`xxx`,
            "ip":"1.1.1.1",
            "hostname":"XXX",
            "cpu": {
                "time": "2013-09-18 11:16:32",
                "user":0,
                "nice":0,
                "system":0,
                "idle":0,
                "iowait":0,
                "irq":0,
                "softirq":0,
                "steal":0,
                "guest":0,
                "guest_nice":0,                
            },
            "memory": {
                "time": "2013-09-18 11:16:32",
                "total":100,
                "used":100,
                "abs_used":100,
                "free":100,
                "buffers":100,
                "cached":100,
                "active":100,
                "inactive":100,
                "swap_used":100     
            },
            "disk": {
                "time": "2013-09-18 11:16:32",
                "t_cap":100,
                "t_free":100,
                "t_read_rate":100,
                "t_write_rate":100,
                "per_disk_info":[
                    {
                    "disk_name":"sda1",
                    "cap":1000,
                    "free":100,
                    "read_rate":1,
                    "write_rate":1,
                    },
                    {
                        ...
                    },
                    ...
                ]            
            },
            "net": {
                "time": "2013-09-18 11:16:32",
                "t_sent_rate":200,
                "t_recv_rate":200,
                "per_net_info":[
                    {
                    "net_name":"eth0",
                    "sent_rate":100,
                    "recv_rate":100,
                    },
                    {
                        ...
                    },
                    ...
                ]            
            },
            "average_load": {
                "time": "2013-09-18 11:16:32",
                "w1_avg": 0.22, 
                "w2_avg": 0.44, 
                "w3_avg": 0.53    
            }
        }
    响应数据(失败):
    
        Status: 400
        {
            "message":"invalid machine id"
        }
    
+ `/monitor/api/machines/:id/search?module=&begin_date=&end_date=`  
 说明:根据所选时间段返回指定ID机器的CPU信息  
请求方法: GET  
请求参数:  
    module=["cpu", "average_load", "disk", "net", "memory"]中的一个--必须  
    start_time:开始时间段 -- 必须  
    end_time:结束时间段 -- 必须  
响应数据(成功):  
1.module=cpu:  

        Status: 200 OK
        [
            {
                "time":"2013-09-18 11:16:32",
                "user":0,
                "nice":0,
                "system":0,
                "idle":0,
                "iowait":0,
                "irq":0,
                "softirq":0,
                "steal":0,
                "guest":0,
                "guest_nice":0
            },
            ...
        ]
    
    2.module=memory:

        Status: 200 OK
        [
            {
                "time":"2013-09-18 11:16:32",
                "total":100,
                "used":100,
                "abs_used":100,
                "free":100,
                "buffers":100,
                "cached":100,
                "active":100,
                "inactive":100,
                "swap_used":100  
            },
            ...
        ]


    3.module=disk:

        Status: 200 OK
        [
            {
                "time":"2013-09-18 11:16:32",
                "t_cap":100,
                "t_used":100,
                "t_free":100,
                "t_read_rate":100,
                "t_write_rate":100,
                "per_disk_info":[
                    {
                    "disk_name":"sda1",
                    "cap":1000,
                    "used":100,
                    "free":100,
                    "read_rate":1,
                    "write_rate":1,
                    },
                    {
                        ...
                    },
                    ...
                ] 
            },
            ...
        ]

    4.module=net:

        Status: 200 OK
        [
            {
                "time":"2013-09-18 11:16:32",
                "t_sent_rate":200,
                "t_recv_rate":200,
                "per_net_info":[
                    {
                    "net_name":"eth0",
                    "sent_rate":100,
                    "recv_rate":100,
                    },
                    {
                        ...
                    },
                    ...
                ] 
            },
            ...
        ]
        
    5.module=average_load:

        Status: 200 OK
        [
            {
                "time":"2013-09-18 11:16:32",
                "w1_avg": 0.22, 
                "w2_avg": 0.44, 
                "w3_avg": 0.53 
            },
            ...
        ]
响应数据(失败):

        Status:400
        参数提供个数不正确时:
        {
            "message":"No begin_date provided"
        }
        参数值不合法时:
        {
            "message": "invalid time args"
        }
        machine_id不存在时:
        {
            "message":"invalid machine id"
        }
        
## 五.前端设计
### 页面设计
+ index
    + topbar
    + detail
        + 侧边栏 和 选择栏
        + 图表页
            + base info 页面    
            + average load 页面
            + cpu 页面
            + disk rate 页面
            + disk usage 页面
            + memory 页面
            + net 页面


### angularJS模块
#### **router**
> 路由 (ui-router)
#### **controllers**
>+ TopController  
机器选择,实时更新及查找条件处理
+ BaseController  
机器基本信息展示
+ AverageLoadController  
机器负载 line chart 实时展示,查找展示
+ CpuController  
Cpu使用率 bar chart 实时展示,查找展示
+ DiskRateController  
磁盘读写速率 area chart 实时展示,查找展示
+ DiskUsageController  
磁盘使用 line chart 实时展示,查找展示
+ NetController  
网卡读写速率 area chart 实时展示,查找展示
+ MemoryController  
内存使用 bar chart 实时展示,查找展示

#### **directives**
> 自定义指令
#### **filters**
> 自定义过滤器
#### **services**
> 数据请求service, 图表value



  [1]: http://docs.jinkan.org/docs/flask/styleguide.html
  [2]: http://www.restapitutorial.com/httpstatuscodes.html
