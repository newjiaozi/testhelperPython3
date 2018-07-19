#coding:utf-8
'''
Created on 2017��2��17��

@author: ldl
'''


import os,json,time,logging
import requests
from urllib.parse import parse_qsl



logger =  logging.getLogger()

def getConfig(BASE_DIR):
    cfg_path = os.path.join(os.path.join(BASE_DIR,'webpage.cfg'))
    logger.info('PATH:'+cfg_path)
    cfg_dict = {}
    try:        
        cfg = open(cfg_path,'r')
        cfg_data = cfg.readlines()
        for i in cfg_data:
            # logger.info("i"+i)
            if i.startswith("#"):
                continue
            elif i:
                tmp = i.split()
                cfg_dict[tmp[0]]=tmp[1]
            else:
                continue
        return cfg_dict
    except Exception as e:
        logger.exception(e)
        return None
        
def moneyper(money,qs,lv):
    mq = money/qs + (money*lv/100)/12
    return '每期： %.2f   总额： %.2f ，每期利息为：%.2f' % (mq,mq*qs,(money*lv/100)/12)


def JY_moneyper(money,qs,lv,kt):
    lx = money*(lv/100)/12
    bj = money/qs[1]
    qs_all = qs[0]+qs[1]
    baoli_res = baoli(kt, lv, qs_all,money)
    sum_money = qs[0]*lx+qs[1]*(bj+lx)
    return '前%s期： %.2f ，后%s期： %.2f，总额为 %.2f' % (qs[0],lx,qs[1],bj+lx,sum_money) + baoli_res


# kt砍头息，lv客户利率，qs分期期数,ts商户贴息,bl保理服务费
def baoli(kt,lv,qs,money):
    ts =(kt-0.6)*12/qs  #商户贴息的年化率：(商户的砍头息-保理的服务费点数)*12/分期期数
    xjtxll = 11.88 - lv - ts  #消金账户的贴息利率=11.88-借款人的年化率-商户贴息的年化率（保理账户中）
    ts_money = 0
    bl = 0
    if (lv+ts) < 11.88:
        if kt > 0.6:
            bl = money*0.6/100 
            ts_money = (money*ts/1200)*qs   
        elif kt == 0.6:
            bl = money*0.6/100 
            ts_money = 0                   
        else:
            bl = money*kt/100
            ts_money = 0
    else:
        if lv > 11.88 and kt != 0:
            bl = money*kt/100
            ts_money = 0
        elif lv == 11.88 and kt != 0:
            bl = money*kt/100
            ts_money = 0
            
        elif lv < 11.88 and kt != 0:
            ts_money = money*kt/100-(money*lv/1200*qs+money*kt/100 -money*11.88/1200*qs) 
            bl = ((money*lv/100)/12)*qs + money*kt/100 - ((money*11.88/100)/12)*qs
        else:
            bl =0 
            ts_money = 0
    return " ,保理服务费为：%.2f，商户贴息费用为：%.2f，打款金额为：%.2f，消金账户的贴息利率:%.2f,商户贴息的年化率:%.2f" % (bl,ts_money,money-bl-ts_money,xjtxll,ts)


def repayment(**xargs):
    count = xargs.get('count')
    money = xargs.get('money')
    lv = xargs.get('lv')
    kt = xargs.get('kt')
    if count.isdigit():
        return moneyper(money,eval(count),lv) + baoli(kt, lv, eval(count), money)
    else:
        return JY_moneyper(money,eval(count),lv,kt)

def postRequest(url,**xargs):
    resp = requests.post(url, data = xargs)
    if resp.ok:
        resp_json = resp.json()
        return json.dumps(resp_json,indent=4,ensure_ascii=False)
#         return resp_json
    else:
        return resp.text


def getRequest(url):
    resp = requests.get(url)
    if resp.ok:
        resp_json = resp.json()
        return json.dumps(resp_json,indent=4,ensure_ascii=False)
#         return resp_json
    else:
        return resp.text


def dict2JsonStr(dict_data):
    if isinstance(dict_data, dict):
        return json.dumps(dict_data,indent=4,ensure_ascii=False)
    return None


def unixtime2bjtime(unixtime_data):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(unixtime_data))

def bjtime2unixtime(bjtime_data):
    return time.mktime(bjtime_data.timetuple())


def parseqs2Dict(qs): 
    return dict(parse_qsl(qs,keep_blank_values=1))
         

if __name__ == '__main__':
    pass