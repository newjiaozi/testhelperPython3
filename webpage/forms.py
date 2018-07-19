#coding:utf-8
'''
Created on 2017年2月20日

@author: ldl
'''


from django import forms
import datetime,time

class CheckPlanForms(forms.Form):    
    count_choices = (
                    (3,'3期',),
                    (6,'6期'),
                    (9,'9期'),
                    (12,'12期'),
                    (18,'18期'),
                    (24,'24期'),
                    (36,'36期'),
                    ([6,6],'6+6期'),
                    ([6,12],'6+12期'),
                    ([6,18],'6+18期'),
                    ([9,15],'9+15期'),
                    ([12,24],'12+24期'),                    
                    )
    count = forms.ChoiceField(choices = count_choices,label='借款期数')
    money =  forms.FloatField(label='借款金额',min_value=1)
    kt = forms.FloatField(label='砍头息')
    lv = forms.FloatField(label='年化利率')



class CreateRepaementForms(forms.Form):
    env_choice = (
                  ('stb','stb环境'),
                  ('sit','sit环境'))
    
    env = forms.ChoiceField(choices= env_choice,label = '环境') 
    mobile = forms.IntegerField(max_value=18999999999,min_value=1,label = '手机号')




class CodisFlushForms(forms.Form):
    env_choice = (
                  (['http://192.168.3.204:8080/system/redis/table.json',['http://192.168.3.204:8080/system/auth/login.json','ldl_admin','111111']],'stb环境'),
                  (['http://server.sit.maiyafenqi.com/system/redis/table.json',['http://server.sit.maiyafenqi.com/system/auth/login.json','ldl_admin','111111']],'sit环境'),
                  (['http://server.pre.maiyafenqi.com/system/redis/table.html',['http://server.pre.maiyafenqi.com/system/auth/login.json','cuidongzhu','cdz-2256836']],'pre环境'),
                  (['http://server.maiyafenqi.com/system/redis/table.json',['http://server.maiyafenqi.com/system/auth/login.json','cuidongzhu','cdz-2256836']],'prd环境'),)
    
    table_choice = (
                    ('ORD_ORDER','ORD_ORDER'),
                    ('ORD_ORDER_PART','ORD_ORDER_PART'),
                    ('ORD_USER','ORD_USER'),
                    ('ORD_USER_ACCOUNT','ORD_USER_ACCOUNT'),
                    ('ORD_USER_DETAIL','ORD_USER_DETAIL'),
                    ('ORD_USER_HONOR','ORD_USER_HONOR'),
                    ('ORD_AUTH_STATUS','ORD_AUTH_STATUS'),
                    ('ORD_WITHDRAW_BALANCE','ORD_WITHDRAW_BALANCE'),
                    )

    
    env = forms.ChoiceField(choices=env_choice,label='环境')
    table = forms.ChoiceField(choices=table_choice,label='表名')
    


class TimesTampForms(forms.Form):
    unixtime_data = forms.IntegerField(label='unixtime转北京时间',required=False,initial=time.mktime(datetime.datetime.today().timetuple()))
    bjtime_data = forms.DateTimeField(label='北京时间转unixtime',required=False,initial=datetime.datetime.today(),input_formats=["%Y-%m-%d %H:%M:%S"])



class Base64ImageForms(forms.Form):
    image_file = forms.FileField(label='图片') 
    
    
    
class ImageBase64Forms(forms.Form):
    base64_text = forms.CharField(widget=forms.Textarea,label="base64数据")
    
    
class InterfaceTestForms(forms.Form):
    
    method_choice = (("POST","POST"),
                     ("GET","GET"))    
    url = forms.URLField(label='请求地址') 
    method = forms.ChoiceField(choices=method_choice,label="请求方法")
    counts = forms.IntegerField(label="请求次数",min_value=1,initial=1)
    data = forms.CharField(widget = forms.Textarea,label="请求数据",required=False)
 
 
class ChangeMoneyForms(forms.Form):
    env_choice =((['cuidongzhu','cdz-2256836'],"prd环境"),)
    env = forms.ChoiceField(label="环境",choices=env_choice)
    orderno = forms.CharField(label='订单编号')
    principal = forms.IntegerField(label="金额",min_value=1,max_value=1000)
   
class Params2DictForms(forms.Form):
    params = forms.CharField(widget=forms.Textarea,label="参数")  
    
    
    
class GetRateUUIDForms(forms.Form):
    env_choice = (([['http://192.168.3.204:8080/system/auth/login.json','admin','qwe123'],"http://server.stb.maiyafenqi.com/a/shop/rateTable/getShopRateHeaderList.json"],"stb环境"),
                  ([['http://server.sit.maiyafenqi.com/system/auth/login.json','admin','qwe123'],"http://server.sit.maiyafenqi.com/shop/rateTable/getShopRateHeaderList.json"],"sit环境"),
                  ([['http://server.pre.maiyafenqi.com/system/auth/login.json','cuidongzhu','cdz-2256836'],"http://server.pre.maiyafenqi.com/shop/rateTable/getShopRateHeaderList.json"],"pre环境"),
                  ([['http://server.maiyafenqi.com/system/auth/login.json','cuidongzhu','cdz-2256836'],"http://server.maiyafenqi.com/shop/rateTable/getShopRateHeaderList.json"],"prd环境"),)  
    
    env = forms.ChoiceField(label="环境",choices=env_choice)
    shopid = forms.IntegerField(label="商户ID")   