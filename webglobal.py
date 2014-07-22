# -*- coding:utf-8 -*-

class Global:

    GLOBAL_ACCOUNT = [
        # 水费
        {
            # 直接成功
            '1000001': {'userCode': '1000001', 'username': u'东家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区88号', 'memo': '缴费成功', 'money': 120.00, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
            # 直接失败
            '1000002': {'userCode': '1000002', 'username': u'李嘉家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费失败', 'money': 20.00, 'status': 'FAIL', 'applyResultCode': '0000106'},
            # 挂起随机转成功or失败
            '1000003': {'userCode': '1000002', 'username': u'李嘉家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费处理中', 'money': 10.90, 'status': 'HANGUP', 'applyResultCode': '0000107'},
            # 没有欠费信息
            '1000004': {'userCode': '1000004', 'username': u'周博', 'success': 'true', 'queryResultCode': '0000121'},
            # 一直挂起
            '1000005': {'userCode': '1000005', 'username': u'郑中', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费处理中', 'money': 10.90, 'status': 'HANGUP', 'applyResultCode': '0000107', 'isHangup': True},
            # 异常
            '1000006': {'userCode': '1000006', 'username': u'阿訇', 'success': 'false', 'queryResultCode': '0000205'}
         },
        # 气费
        {
            # 直接成功
            '2000001': {'userCode': '2000001', 'username': u'么么', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区门店8号', 'memo': '缴费成功', 'money': 312.88, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
            # 直接失败
            '2000002': {'userCode': '2000002', 'username': u'刘尼', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区洋河北路10号', 'memo': '缴费失败', 'money': 39.09, 'status': 'FAIL', 'applyResultCode': '0000106'},
            # 挂起随机转成功or失败
            '2000003': {'userCode': '2000003', 'username': u'哈格', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市九龙坡区12号', 'memo': '缴费处理中', 'money': 19.10, 'status': 'HANGUP', 'applyResultCode': '0000107'},
            # 没有欠费信息
            '2000004': {'userCode': '2000004', 'username': u'张尼', 'success': 'true', 'queryResultCode': '0000121'},
            # 一直挂起
            '2000005': {'userCode': '2000005', 'username': u'郑中', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费处理中', 'money': 10.90, 'status': 'HANGUP', 'applyResultCode': '0000107', 'isHangup': True},
            # 异常
            '2000006': {'userCode': '2000006', 'username': u'阿訇', 'success': 'false', 'queryResultCode': '0000205'}
         },
        # 电费
        {
            # 直接成功
            '3000001': {'userCode': '3000001', 'username': u'占方式', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区11号', 'memo': '缴费成功', 'money': 81.20, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
            # 直接失败
            '3000002': {'userCode': '3000002', 'username': u'张三丰', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区健康路121号', 'memo': '缴费失败', 'money': 9.02, 'status': 'FAIL', 'applyResultCode': '0000106'},
            # 挂起随机转成功or失败
            '3000003': {'userCode': '3000003', 'username': u'杨富', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区龙组路89号', 'memo': '缴费处理中', 'money': 190.90, 'status': 'HANGUP', 'applyResultCode': '0000107'},
            # 没有欠费信息
            '3000004': {'userCode': '3000004', 'username': u'王博', 'success': 'true', 'queryResultCode': '0000121'},
            # 一直挂起
            '3000005': {'userCode': '3000005', 'username': u'郑中', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费处理中', 'money': 10.90, 'status': 'HANGUP', 'applyResultCode': '0000107', 'isHangup': True},
            # 异常
            '3000006': {'userCode': '3000006', 'username': u'阿訇', 'success': 'false', 'queryResultCode': '0000205'}
         },
        # 手机充值
        {
            # 直接成功
            '18523125117': {'userCode': '18523125117', 'status': 'SUCCESS', 'applyResultCode': '0000000'},
            # 直接失败
            '15123334382': {'userCode': '15123334382', 'status': 'FAIL', 'applyResultCode': '0000106'},
            # 挂起转失败
            '13811111111': {'userCode': '13811111111', 'status': 'HANGUP', 'applyResultCode': '0000107', 'rechangeStatus': 'FAIL'},
            # 挂起转成功
            '13822222222': {'userCode': '13822222222', 'status': 'HANGUP', 'applyResultCode': '0000107', 'rechangeStatus': 'SUCCESS'},
            # 一直挂起
            '13833333333': {'userCode': '13833333333', 'status': 'HANGUP', 'applyResultCode': '0000107', 'isHangup': True}
            }
        ]
    

    # 商户key
    GLOBAL_MERCHANTS = {'lencee': '9a7520152a7a97cfc76c82454463a83c'}

    '''sqlite3 数据表名称'''
    # 缴费表
    GLOBAL_TABLE_PAYMENT = 'easylife_payment_order'
    # 预存款表
    GLOBAL_TABLE_BALANCE = 'easylife_merchant_balance'

    # 结果码
    GLOBAL_RESP_CODE = {
        '0000000': u'执行成功',
        '0000100': u'参数不合法',
        '0000101': u'可用余额小于缴费金额',
        '0000102': u'当前机构不可用或当前用户无此机构使用权限',
        '0000103': u'订单创建失败',
        '0000104': u'担保交易创建失败',
        '0000105': u'缴费过程中校验失败',
        '0000106': u'缴费失败',
        '0000107': u'缴费处理中',
        '0000108': u'缴费部分失败',
        '0000109': u'缴费前的处理失败',
        '0000110': u'数据未找到',
        '0000111': u'外部订单号已存在',
        '0000120': u'缴费用户不存在',
        '0000121': u'没有欠费信息',
        '0000122': u'缴费用户账户状态不正常',
        '0000123': u'没有抄表或缴费账单未生成',
        '0000124': u'用户上月未交费',
        '0000125': u'卡或表故障',
        '0000126': u'超过限定金额',
        '0000127': u'撤销缴费出错',
        '0000128': u'路由失败',
        '0000129': u'支付金额不能小于欠费金额',
        '0000130': u'支付金额必须等于欠费金额',
        '0000131': u'不在缴费时间段',
        '0000132': u'业务前置条件不满足',
        '0000133': u'返销处理中',
        '0000134': u'业务状态异常',
        '0000201': u'缴费系统远端执行异常',
        '0000202': u'缴费系统参数异常',
        '0000204': u'缴费系统远端返回系统级异常',
        '0000205': u'缴费系统远端返回未知异常',
        '0000300': u'账户金额冻结失败',
        '0000302': u'退款失败',
        '0000303': u'分润退款失败',
        '0000400': u'未知异常',
        '0000401': u'数据库访问异常',
        '0000402': u'交易系统网络异常',
        '0000403': u'缴费系统网络异常',
    }

    def __init__(self):
        pass
