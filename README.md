webpy-mock
==========

使用webpy mock易生活缴费环境

- 查询欠费、缴费、查询缴费状态
- 后台定时修改缴费挂起状态
- 使用sqlite3存储缴费数据和预存款信息

## **如何使用?**

### **Install**
1. 安装python2.7+
2. 安装 [web.py模块](http://webpy.org/static/web.py-0.37.tar.gz)

### **Run**
1. 进入主目录
2. 命令行模式下运行：
```shell
python index.py
\# 或
python index.py 8000
```
可选参数有`port`，表示具体的端口号，示例：`python index.py 8000`，以本地`8000`端口运行web程序

## **未解决的问题**
+ 异常处理不完善
+ 日志处理未自动增加日期
