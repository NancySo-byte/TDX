from pytdx.hq import TdxHq_API
api = TdxHq_API(heartbeat=False)
api = api.connect( '124.71.187.72',7709)
#返回代码
def all_stock():
    stock = []
    c = api.get_security_list(1, 21000)
    d = api.get_security_list(1, 22000)
    e = api.get_security_list(1, 23000)
    for i in c:
        if i['code'][0:3] == '600' or i['code'][0:3] == '601' or i['code'][0:3] == '603' or i['code'][0:3] == '605':
            stock.append(i['code'])
    for i in d:
        if i['code'][0:3] == '600' or i['code'][0:3] == '601' or i['code'][0:3] == '603' or i['code'][0:3] == '605':
            stock.append(i['code'])
    for i in e:
        if i['code'][0:3] == '600' or i['code'][0:3] == '601' or i['code'][0:3] == '603' or i['code'][0:3] == '605':
            stock.append(i['code'])
    a = api.get_security_list(0, 0)
    b = api.get_security_list(0, 1000)
    for g in a:
        if g['code'][0:3] == '000' or g['code'][0:3] == '001' or g['code'][0:3] == '002':
            stock.append(g['code'])
    for h in b:
        if h['code'][0:3] == '000' or h['code'][0:3] == '001' or h['code'][0:3] == '002':
            stock.append(h['code'])
    return stock

#确定9点25位置
def nine_25_station(maker,stock_code,time):
    if stock_code[0:3] == '000' or stock_code[0:3] == '001' or stock_code[0:3] == '002':
        maker = 0
    else:
        maker = 1
    # 先判断是否在这个区间中
    left_data = 3000
    right_data = 5000
    if len(api.get_history_transaction_data(maker, stock_code, left_data, 1, time)) == 0:
        # print('{}是3000之内'.format(stock_code))
        left_data = 100
    elif len(api.get_history_transaction_data(maker, stock_code, right_data, 1, time)) != 0:
        # print('{}是5000之外'.format(stock_code))
        right_data = 10000
    a =True
    while a:
        if len(api.get_history_transaction_data(maker, stock_code, left_data, 1, time)) == 1 and len(api.get_history_transaction_data(maker, stock_code, left_data + 1, 1, time))== 0:
            # print('{}在09：25的位置是{}'.format(stock_code,left_data))
            a = False
        if len(api.get_history_transaction_data(maker, stock_code, left_data, 1, time)) == 1 and len(api.get_history_transaction_data(maker, stock_code, right_data, 1, time)) == 0:
            if len(api.get_history_transaction_data(maker, stock_code,int((left_data + right_data)/2), 1, time)) == 0:
                right_data = int((left_data + right_data)/2)
            else:
                left_data = int((left_data + right_data)/2)
    return left_data
#找到9点35时的位置并判断没有负数
def nine_35_station(makers,stock_code,time):
    if stock_code[0:3] == '000' or stock_code[0:3] == '001' or stock_code[0:3] == '002':
        makers = 0
    else:
        makers = 1
    a = nine_25_station(makers,stock_code,time)
    b = True
    while b:
        if api.get_history_transaction_data(makers,stock_code,a,1,time)[0]['time'] != '09:35':
            a = a - 1
        else:
            # print('{}在09：35位置是{}'.format(stock_code,a))
            b = False
    return a
#获取股票前一天的收盘价来计算股票的涨幅。
def list_day(stock_code):
    if stock_code[0:3] == '000' or stock_code[0:3] == '001' or stock_code[0:3] == '002':
        maker = 0
    else:
        maker = 1
    a = api.get_security_bars(4,maker, stock_code, 1, 1)[0]['close']
    return a

# 提取时间，提取昨天的收盘价格
def time_closes(makers,i):
    time_close = {}
    # 提取日K线
    day_k = api.get_security_bars(9, makers, i, 0, 800)
    for t in day_k:
        year = str(t['datetime'][0:4])
        month = str(t['datetime'][5:7])
        day = str(t['datetime'][8:10])
        time = year + month + day
        close = t['close']
        time_close[time] = close
    return time_close
print(time_closes(1,'600000'))


# 主程序（无修改）
def main():
    for i in all_stock():
        if i[0:3] == '000' or i[0:3] == '001' or i[0:3] == '002':
            makers = 0
        else:
            makers = 1
        # a = api.get_history_transaction_data(makers, i, nine_35_station(0, i, time),nine_25_station(0, i, time) - nine_35_station(0, i, time), time)
        # b = 0
        # for y in a:
        #     # print((y['price']-close)/close*100)
        #     if (y['price'] - close) / close * 100 <= 80:
        #         if b <= y['price']:
        #             b = y['price']
        #         else:
        #             print(i)
        #             print('下降排除')
        #             break
        #     else:
        #         print('选择这个')


if __name__ == '__main__':
    main()