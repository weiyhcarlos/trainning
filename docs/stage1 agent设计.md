# stage1 agent设计
## 主模块
业务流程处理,根据需求调用相应模块.
如果需要更改业务逻辑时,直接更改主模块逻辑调用各个模块.
目前流程
	1. 检测程序是否存在.是执行3,否执行2.  
	2. 查询/更改/调试,执行相应的流程并结束.  
	3. 读取配置文件  
	4. 根据参数修改设置   
	5. 调整时间同步   
	6. 加载收集模块,实例化  
	7. 启动查询模块,准备接收查询/更改设置等.  
	8. 收集信息  
	9. 数据处理  
	10. 数据是否处理成功,是执行11,否则执行12  
	11. 存储本地,设定标记
  
[流程图](https://www.processon.com/view/565d1019e4b010dc0fb4a43e)


## 模块

### 1.工具类

#### 1.1解析配置文件
读取本地配置文件加载到全局变量中
code:utils目录下config.py

#### 1.2命令行参数解析
解析命令行参数,并加载到环境变量中.
抽象出来.设定一个基类.每增加一个新的参数,直接增加对应的子类处理即可.
code:utils目录下args_par.py

##### 1.3修改参数
修改全局变量
code:与1.2相同

##### 1.4查询
与查询线程通信,返回对应结果
code:与1.2相同

#### 1.5时间同步
检测ntp服务是否开启
code:utils目录下syn_time.py


### 2.信息收集模块

[信息收集类图](https://www.processon.com/view/link/566ad86be4b0add117b77c60)

收集模块主要结构:

    Collector类
        __init__方法 
            参数: ["cpu","memory",...]
        
        set_module方法 
            参数:["cpu","memory",...]
            返回:
                成功则返回{"status":0, "ret":""}
                失败则返回{"status":1, "ret":error_message}
        
        **collect_info方法** (主收集方法)
            参数:
                无
            返回: 
                成功则返回{"status":0, "ret":收集信息dict}
                失败则返回{"status":1,"ret":error_message}
    
    
    BaseCollect基类: 实现collect函数
        MemoryCollector类
        CpuCollector类
        DiskCollector类
        NetCollector类
        AverageLoadCollector类


### 3.信息处理模块
[处理模块类图](https://www.processon.com/view/link/566ad838e4b0add117b77aac)

处理模块主要结构:
    
    Handler类:
        __init__方法
            参数:{
                "method":方法名,           
                "config":配置dict(包括本地文件存储位置以及连接参数)
            }
        
        set_handler方法
            参数:{
                "method":方法名,           
                "config":配置dict(包括本地文件存储位置以及连接参数)
            }
            返回:
                成功则返回{"status":0, "ret":收集信息dict}
                失败则返回{"status":1,"ret":error_message}            
        
        **handle_data方法** (主处理方法)
            参数(以dict方式存入):
                {
                "modules":["cpu","memory","average_load",
                            "net","disk"],
                "data":收集得到的机器信息
                }
            返回:
                成功则返回:{"status":0,"ret":""}
                失败则返回:{"status":1, "ret":相应错误信息}
 
    BaseHandler类:
        PrintHandler类 #调试用
        MongodbHandler类
        TcpHandler类 #TODO


## 接口
### 指标
#### 平均负载
	指标 含义
	w1_avg 1分钟平均负载
	w5_avg 5分钟平均负载
	w15_avg 15分钟平均负载

#### cpu
	信息:单位百分比(%)
	指标 含义
	user 用户态
	nice 低优先级用户态
	system 内核态
	idle 空闲
	iowait 等待IO
	irq 硬中断服务	
	softirq 软中断服务
	steal 虚拟化相关
	guest 虚拟化相关
	guest_nice 虚拟化相关

#### mem
	信息:单位MB
	指标 含义
	total 总内存
	used 已使用内存
	abs_used used - buffers - cached
	free 空闲内存
	buffers 磁盘缓冲
	cached 磁盘缓存
	active 活跃内存，不大可能被挪用
	inactive 不活跃内存，很可能被挪用
	swap_used 已使用 swap

#### net	
	信息:单位KB/s
	考虑多块网卡情形

	指标 含义
    t_sent_rate 总发送速率
    t_recv_rate 总接收速率
	sent_rate  单个网卡发送速率
	recv_rate 单个网卡接收速率


#### disk
	信息:
	考虑多块磁盘情形

	指标 含义
    t_cap 所有磁盘容量 GB
    t_used 所有磁盘使用 GB
	t_free  所有磁盘剩余 GB
	t_read_rate  磁盘读 MB/s
	t_write_rate 磁盘写 MB/s
	cap   单块磁盘容量 GB
    used  单块磁盘使用 GB
	free  单块磁盘剩余 GB
	read_rate  单块磁盘读 MB/s
	write_rate 单块磁盘写 MB/s


### 数据消息内容
	{
		"cluster":"XXX",
		"ip":"1.1.1.1",
		"mac":"00:00:00:00:00:00",
		"hostname":"XXX",
		"time":"2015-12-09 11:16:32",
		"cpu":
		{
			"user":0,
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
			//暂省略cpu信息,例如个数.
		},
		"mem":
		{
			"total":100,
			"used":100,
			"abs_used":100,
			"free":100,
			"buffers":100,
			"cached":100,
			"active":100,
			"inactive":100,
			"swap_used":100,
		},
		"disk":
		{
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
					"disk_name":"sda2",
					"cap":1000,
					"free":100,
					"read_rate":1,
					"write_rate":1,
				}
			]
		},
		"net":
        {
            "t_sent_rate":100,
            "t_recv_rate":100,
            "per_net_info":[
                {
                    "net_name":"eth0",
                    "sent_rate":100,
                    "recv_rate":100,
                },
                {
                    ...
                }
                ...
            ]
	}

### 数据消息格式
通过json格式传输数据.



