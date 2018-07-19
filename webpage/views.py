#! coding:utf-8

from django.shortcuts import render

# Create your views here.

from . import tools
import os,json
from .forms  import CheckPlanForms,CreateRepaementForms,CodisFlushForms,TimesTampForms,Base64ImageForms,ImageBase64Forms,InterfaceTestForms,ChangeMoneyForms,Params2DictForms,GetRateUUIDForms
from .createRepayByPhone import createPlanReal

import base64
import logging

logger =  logging.getLogger()

def handlePage(request):
    cfg = tools.getConfig(os.path.dirname(tools.__file__))
    # logger.info(os.path.dirname(tools.__file__)+"*****"+tools.__file__)
    # logger.info('config:'+str(cfg))
    return render(request, 'webpage/index.html', {'mainpage':cfg})


def createPlan(request):
    if request.method == 'GET':
        crforms = CreateRepaementForms()
    elif request.method == 'POST':
        crforms = CreateRepaementForms(request.POST)
        if crforms.is_valid():
            crforms_data = crforms.cleaned_data
            result = createPlanReal(crforms_data.get('env'),crforms_data.get('mobile'))        
            return render(request, 'webpage/createPlan.html', {'crforms':crforms,'result':result})
    return render(request, 'webpage/createPlan.html', {'crforms':crforms})
def checkPlan(request, repayment=tools.repayment(**cpforms_data)):
    if request.method == 'GET':
        cpforms = CheckPlanForms()
      
    elif request.method == 'POST':
        cpforms = CheckPlanForms(request.POST)  
        if cpforms.is_valid():
            cpforms_data = cpforms.cleaned_data
            result = repayment
            return render(request,'webpage/checkPlan.html',{'cpforms':cpforms,'result':result})
    return render(request, 'webpage/checkPlan.html', {'cpforms':cpforms})   


def codisFlush(request):
    if request.method == 'GET':
        cfforms = CodisFlushForms()
    elif request.method == 'POST':
        cfforms = CodisFlushForms(request.POST)
        if cfforms.is_valid():
            params_dict = {}
            cfforms_data = cfforms.cleaned_data   
#             print cfforms_data  
            cfforms_list = eval(cfforms_data.get('env'))     
            params_dict['username'] = cfforms_list[1][1]
            params_dict['password'] = cfforms_list[1][2]
            user_url = cfforms_list[1][0]
            result1 = tools.postRequest(user_url,**params_dict)
            result1 = json.loads(result1)
            params_dict = {}
            params_dict['key'] = cfforms_data.get('table')
            params_dict['maiyaSid'] = result1.get('result').get('session')
            url = cfforms_list[0]
            result2 = tools.postRequest(url,**params_dict)

            return render(request, 'webpage/codisFlush.html', {'cfforms':cfforms,'result':result2})
    return render(request, 'webpage/codisFlush.html', {'cfforms':cfforms})

def jsonFormat(request):
    return render(request,'webpage/jsonFormat.html',{})        

def timesTamp(request):
    if request.method == 'GET':
        ttforms = TimesTampForms() 


    elif request.method == 'POST':
        ttforms = TimesTampForms(request.POST)  
        if ttforms.is_valid():
            ttforms_data = ttforms.cleaned_data
            unixtime_data = ttforms_data.get("unixtime_data",None)
            bjtime_data = ttforms_data.get("bjtime_data",None)
            result1=None            
            result2=None
            if unixtime_data:
                result1 = tools.unixtime2bjtime(unixtime_data)
            if bjtime_data:
                result2 = tools.bjtime2unixtime(bjtime_data)
            return render(request,'webpage/timesTamp.html',{'ttforms':ttforms,"result2":result2,"result1":result1})
 
    return render(request, 'webpage/timesTamp.html', {'ttforms':ttforms})   

def changeMoney(request):
    if request.method == 'GET':
        cmforms = ChangeMoneyForms()
    elif request.method == 'POST':
        cmforms = ChangeMoneyForms(request.POST)
        if cmforms.is_valid():
            try:                
                cmforms_data = cmforms.cleaned_data
                orderno = cmforms_data["orderno"]
                principal = cmforms_data["principal"]
                env = eval(cmforms_data["env"])

                login_url = "http://server.maiyafenqi.com/system/auth/login.json"
                check_url = "http://server.maiyafenqi.com/order/operative/operativeList.json"
                change_url = "http://server.maiyafenqi.com/order/initOrderDataController/changeOrderInfo.json"
                xargs = {"username":env[0],"password":env[1]}  
     
                result1 = tools.postRequest(login_url,**xargs) 

                result1_json = json.loads(result1) 
                
                maiyaSid = result1_json.get("result").get("session")
                
                params_dict ={"bdid":"","pageNo":1,"pageSize":10,"username":"","orderNo":"","name":"","mobile":"","status":"","employeeId":"","createStartTime":"","createEndTime":"","shopNameLike":"","DESC":"order_begin_date","maiyaSid":""}
                
                params_dict["bdid"]= result1_json.get("result").get("user").get("id")
                params_dict["orderNo"] = orderno
                params_dict["maiyaSid"] = maiyaSid   
                
                result2 = tools.postRequest(check_url,**params_dict)
                result2_json = json.loads(result2)
                result2_result= result2_json.get("result",None)
                if result2_result:
                    result2_data = result2_result.get("data",None)
                    if result2_data and len(result2_data)== 1:
                        result2_data = result2_data[0]
                        params_dict2 = {}
                        params_dict2["uuid"] = result2_data.get("userUUID")
                        params_dict2["orderUuid"] = result2_data.get("uuid")
                        params_dict2["maiyaSid"] = maiyaSid
                        params_dict2["principal"] = principal         
                        
                        result3 = tools.postRequest(change_url,**params_dict2)          
                        return render(request, 'webpage/changeMoney.html', {'cmforms':cmforms,'result1':result1,"result2":result2,"result3":result3})
                
                return render(request, 'webpage/changeMoney.html', {'cmforms':cmforms,"result4":"订单号查询不到订单或多于1个订单！"})
            except Exception as e:
                    return render(request, 'webpage/changeMoney.html', {'cmforms':cmforms,"result4":str(e)})                  
    
    return render(request, 'webpage/changeMoney.html', {'cmforms':cmforms})  



def base64Image(request):
    if request.method == 'GET':
        biforms = Base64ImageForms()
    elif request.method == 'POST':
        biforms = Base64ImageForms(request.POST,request.FILES)

        if biforms.is_valid():            
            biforms_data = biforms.cleaned_data
            myfile = biforms_data.get('image_file')

            if myfile.size > 512000:
#                 result1 =u"文件大于500K，不能转换"
                result1 = base64.b64encode(myfile.read())
            else:                
                result1 = base64.b64encode(myfile.read())
            return render(request, 'webpage/base64Image.html', {'biforms':biforms,'result1':result1})
    return render(request, 'webpage/base64Image.html', {'biforms':biforms})


def imageBase64(request):
    if request.method == 'GET':
        ibforms = ImageBase64Forms()
    elif request.method == 'POST':
        ibforms = ImageBase64Forms(request.POST)
        result = False
        if ibforms.is_valid(): 
            ibforms_data = ibforms.cleaned_data           
            base64_text = ibforms_data.get("base64_text",None)
            image_data = base64.b64decode(base64_text)
            tmp1_png = os.path.join(os.path.dirname(__file__),"static/webpage","tmp.png")
            # logger.info(tmp1_png)
            tmp1 = open(tmp1_png,"wb")
            tmp1.write(image_data) 
            tmp1.close()
            result = True                        
            return render(request, 'webpage/imageBase64.html', {'ibforms':ibforms,'result':result})
    return render(request, 'webpage/imageBase64.html', {'ibforms':ibforms})


def interfaceTest(request):
    if request.method == 'GET':
        itforms = InterfaceTestForms()      
    elif request.method == 'POST':
        
        itforms = InterfaceTestForms(request.POST)  
        if itforms.is_valid():
            itforms_data = itforms.cleaned_data

            method = itforms_data['method']
            counts = itforms_data['counts']
            all_result = {}
            if method == "POST":
                data = tools.parseqs2Dict(itforms_data['data'])
                for i in range(0,counts): 
                    result = tools.postRequest(itforms_data['url'],**data)
                    all_result["%s" % (i+1)] = result
            elif method == "GET":                
                for i in range(0,counts):                    
                    result = tools.getRequest(itforms_data['url'])
                    all_result["%s" % (i+1)] = result
          
            return render(request,'webpage/interfaceTest.html',{'itforms':itforms,'result':result,"all_result":all_result})
    return render(request, 'webpage/interfaceTest.html', {'itforms':itforms})   



def params2Dict(request):
    if request.method == 'GET':
        pdforms = Params2DictForms()     
    elif request.method == 'POST':
        pdforms = Params2DictForms(request.POST)  
        if pdforms.is_valid():
            pdforms_data = pdforms.cleaned_data
#             print pdforms_data
            result = tools.parseqs2Dict(pdforms_data['params'])            
            result = json.dumps(result,indent=4,ensure_ascii=False)
            return render(request,'webpage/params2Dict.html',{'pdforms':pdforms,'result':result})
    return render(request, 'webpage/params2Dict.html', {'pdforms':pdforms})   



def getRateUuid(request):
    if request.method == 'GET':
        grforms = GetRateUUIDForms()      
    elif request.method == 'POST':
        grforms = GetRateUUIDForms(request.POST)  
        if grforms.is_valid():
            try:
                grforms_data = grforms.cleaned_data
                env = eval(grforms_data["env"])
                shopId = grforms_data["shopid"]
                
                login_url = env[0][0]
                username = env[0][1]
                password = env[0][2]
                rate_url = env[1]
                
                xargs = {"username":username,"password":password}
                result1 = tools.postRequest(login_url,**xargs) 
                result1_json = json.loads(result1)            
                maiyaSid = result1_json.get("result").get("session")          
                
                param_dict = {"shopId":"","maiyaSid":""}
                param_dict["shopId"] = shopId
                param_dict["maiyaSid"] = maiyaSid
                result = tools.postRequest(rate_url,**param_dict)
                result2 = None
            except Exception as e:
                result2 = str(e)
                result = None
            return render(request,'webpage/getRateUuid.html',{'grforms':grforms,'result':result,"result2":result2})
    return render(request, 'webpage/getRateUuid.html', {'grforms':grforms})   




def changeAuthentication(request):
    pass