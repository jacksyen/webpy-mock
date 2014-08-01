webpy-mock
==========

使用webpy mock易生活缴费环境

- 查询欠费、缴费、查询缴费状态
- 后台定时修改缴费挂起状态
- 使用sqlite3存储缴费数据和预存款信息
- 日志按天记录

## **如何使用?**

### **Install**
1. 安装python2.7+
2. 安装 [web.py模块](http://webpy.org/static/web.py-0.37.tar.gz)

### **Run**
1. 进入主目录
2. 命令行模式下运行：
```shell
python index.py
# 或
python index.py 8000
```
可选参数有`port`，表示具体的端口号，示例：`python index.py 8000`，以本地`8000`端口运行web程序

### **添加商户预存款**
在浏览器中输入`http://<host>:8000/rechange`，输入金额，在原始预存款上增加当前输入的金额

### **测试账号**
| 类型    | 直接成功   | 直接失败   | 挂起，随机转成功或失败   | 没有欠费信息   | 一直挂起   | 异常   |  挂起转成功 |
| -------| :------:  | :------:  | :------:  | :------:  | :------:  | :------:  | :------:  |
| 二次供水 | 1000001  | 1000002  | 1000003  | 1000004  | 1000005  | 1000006   | 1000008
| 重庆燃气 | 2000001  | 2000002  | 2000003  | 2000004  | 2000005  | 2000006   |
| 重庆电力 | 3000001  | 3000002  | 3000003  | 3000004  | 3000005  | 3000006   |

| 类型    | 直接成功   | 直接失败   | 挂起转失败   | 挂起转成功   | 一直挂起   |
| -------| :------:  | :------:  | :------:  | :------:  | :------:  |
| 手机充值 | 18523125117 | 15123334382 | 13811111111 | 13822222222 | 13833333333 |

## **未解决的问题**
+ 异常处理不完善
