#coding=utf-8




import requests
import mysql.connector
import json



##查询用户bo_id非0的所有bo_id
sql = 'select ORD_USER.nonobank_userid,ORD_ORDER.bo_id from ORD_ORDER,ORD_USER \
    where ORD_USER.id = ORD_ORDER.create_user and ORD_USER.mobile = "%s" \
    and ORD_USER.disabled =0 and ORD_ORDER.bo_id !=0 and ORD_ORDER.status =7' 


## 已经在ORD_ORDER_PART中的数据，不需要再执行生成任务计划，已经有了分期详情
sql_1 = 'select distinct ORD_ORDER_PART.bo_id from ORD_ORDER_PART,ORD_USER where \
        ORD_ORDER_PART.nonobank_userid = ORD_USER.nonobank_userid \
        and ORD_USER.mobile = "%s"' 




## stb
config = {"stb":{'host':'10.3.1.10',
        'user':'root',
        'password':'0708',
        'port':3306 ,#默认即为3306
        'database':'finance_order',
        'charset':'utf8'#默认即为utf8
        },"stb_host_addr":"192.168.3.54:8080","sit":{'host':'192.168.4.13',
        'user':'maiya_app',
        'password':'AosimisigsxHziv/6vwjYFhM3Q',
        'port':3308 ,#默认即为3308
        'database':'finance_order',
        'charset':'utf8'#默认即为utf8
        },"sit_host_addr":"192.168.4.11:8080"}


## 获取用户下的所有bo_id和nonobank_userid
def getSessionBoid(platform,phone):
##    print u"操作平台为：%s" % platform
    try:
        cnn=mysql.connector.connect(**config.get(platform))
        cursor = cnn.cursor()
        cursor.execute(sql % phone)        
        res = cursor.fetchall()
        cursor.execute(sql_1 % phone)
        res_1 = cursor.fetchall()
        return res,res_1
    except mysql.connector.Error as e:
        print(('connect fails!{}'.format(e)))
        return
    finally:
        cursor.close()
        cnn.close()   

def createPlanReal(platform,phone):
##    print u"操作平台为：%s" % platform
    result = ''
    boid_yes,boid_no = getSessionBoid(platform,phone)
    result += "可能需要操作的数据有：%s \n" % boid_yes
    boid_list_dont_handle = []
    if boid_no:
        for i in boid_no:
            boid_list_dont_handle.append(i[0])
#     result +=  u"不需要操作的数据有：%s \n" % boid_list_dont_handle
        
    count = 0    
    if boid_yes:
        for querydata in boid_yes:                
            userId = querydata[0]
            boid = querydata[1]
            if boid in boid_list_dont_handle:
                continue
            resp = requests.post("http://%s/nono-csmFin/csmFin/loginByUserId" % config.get(platform+"_host_addr"),headers={'Content-Type': 'application/x-www-form-urlencoded'},data={'userId':userId},timeout=60)
            sessionid = resp.json().get('data').get('sessionId')
#             print type(boid),type(userId),type(sessionid)
            result1 = "获取nonosession的msg为："+resp.json().get('msg')+"USERID="+userId+"SESSIONID="+sessionid
            result += result1
            request = {"sessionId":sessionid,"userId":userId,"boid":boid}
            resp = requests.post("http://%s/nono-csmFin/csmFin/executeXJTimingtask"  % config.get(platform+"_host_addr"),data={'request':json.dumps(request)})
            result2 = "执行任务计划响应结果为：--####--"+resp.text
            result += result2
            count += 1
        
        return result + '实际共执行%s 次' % count 
    else:
        return "出现错误,未查询到可以操作的数据！"






