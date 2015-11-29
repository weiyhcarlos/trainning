# stage1 agent 设计
## 一.主模块
业务流程处理,根据需求调用相应模块.
如果需要更改业务逻辑时,直接更改主模块逻辑调用各个模块.
目前流程
	1. 读取配置文件,加载相应模块
	2. 依次处理相关模块
	3. 处理options.

## 二.信息收集模块
通过线程池收集信息,并组装数据.

### 平均负载
	指标 含义
	w1_avg 1分钟平均负载
	w5_avg 5分钟平均负载
	w15_avg 15分钟平均负载

### cpu
	信息:
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

### mem
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

### net	
	信息:单位KB
	考虑多块网卡情形

	指标 含义
	read  网络读
	write 网络写


### disk
	信息:单位KB
	考虑多块磁盘情形

	指标 含义
	total 所有磁盘容量
	tfree  所有磁盘剩余
	tread  磁盘读
	twrite 磁盘写
	cap   单块磁盘容量
	free  单块磁盘剩余
	read  单块磁盘读
	write 单块磁盘写


## 三.信息处理模块
信息处理模块
例如存储数据库,网络传输.

## 四.接口
### 数据消息内容
	{
		#'cluster':'XXX',
		'ip':'1.1.1.1',
		'mac':'00:00:00:00:00:00',
		'hostname':'XXX',
		'cpu':
		{
			'user':0,
			'user':0,
			'nice':0,
			'system':0,
			'idle':0,
			'iowait':0,
			'irq':0,
			'softirq':0,
			'steal':0,
			'guest':0,
			'guest_nice':0,
			#暂省略cpu信息,例如个数.
		},
		'mem':
		{
			'total':100,
			'used':100,
			'abs_used':100,
			'free':100,
			'buffers':100,
			'cached':100,
			'active':100,
			'inactive':100,
			'swap_used':100,
		},
		'disk':
		{
			'total':100,
			'free':100,
            'used':100,
			'read_count':100,
			'write_count':100,
            'read_bytes':100,
            'write_bytes':100,
            'read_time':100,
            'write_time':100
			#[
			#	{
			#		'name':'sda1',
			#		'cap':1000,
			#		'free':100,
			#		'read':1,
			#		'write':1,
			#	},
			#	{
			#		'name':'sda2',
			#		'cap':1000,
			#		'free':100,
			#		'read':1,
			#		'write':1,
			#	}
			#]
		},
		'net':
		{
            'interface_name1': {
                    'bytes_sent':100,
                    'bytes_recv':100,
                    'packets_sent':100,
                    'packets_recv':100,
                    'errin':100,
                    'errout':100,
                    'dropin':100,
                    'dropout':100
                    },
            'interface_name2': {
                    ...
                    }
            ...
		}
	}

### 数据消息格式
通过json格式传输数据.

## 五.其他

### 工具类

### 时间同步
agent开启时,首先同步服务器时间,达到一致.

