### 目录结构

* agent-server 监控web后台
* agent-ui 监控web前端
* agent-worker 监控数据接口
* agent 监控数据收集
* docs 文档

## 项目结构

* code: 代码目录
* conf: 配置文件
* misc: 环境配置文件、一些依赖等
* tests: 测试代码
* scripts: 脚本，启停控制等


### 镜像构建

    docker build -t $USER/$NAME .
