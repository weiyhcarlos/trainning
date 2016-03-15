## 一. 数据提交接口

+ /upload  
说明:上传相应模块的机器模块采集信息  
请求方法: POST  
请求参数:  
　　module:["cpu", "average_load", "disk", "net", "memory"]中的一个或多个，用逗号隔开--必须  
data: 收集的相应模块的信息--必须  
响应数据(成功):  

        Status: 200 OK
        {
            "message":""
        }
	响应数据(失败):

        Status:400
        参数不是json时:
        {
            "message":"invalid json data"
        }
        模块与模块数据不匹配时:
        {
            "message": "incomplete json data"
        }
        请求参数为空时:
        {
            "message":"empty json data"
        }

## 二.查询接口

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
　　module:["cpu", "average_load", "disk", "net", "memory"]中的一个或多个，用逗号隔开--必须  
　　start_time:开始时间段 -- 必须  
　　end_time:结束时间段 -- 必须  
 
	响应数据(成功):  

	1.module=cpu:  

        Status: 200 OK
        {
        "cpu":[
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
        }
  
    2.module=memory:

        Status: 200 OK
        {
        "memory":[
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
        }

    3.module=disk:

        Status: 200 OK
        {
        "disk":[
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
        }

    4.module=net:

        Status: 200 OK
        {
        "net":[
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
        }
   
    5.module=average_load:

        Status: 200 OK
        {
        "average_load":[
            {
                "time":"2013-09-18 11:16:32",
                "w1_avg": 0.22,
                "w2_avg": 0.44,
                "w3_avg": 0.53
            },
            ...
        ]
        }
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


