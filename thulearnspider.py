import requests
import sys
from lxml import etree

class Login(object):
    def __init__(self):
        self.login_url='http://learn.tsinghua.edu.cn/f/login'
        self.post_url='https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do'
        self.logined_url='http://learn2018.tsinghua.edu.cn/f/wlxt/index/course/student/'
        self.lesson_url='http://learn2018.tsinghua.edu.cn/b/wlxt/kc/v_wlkc_xs_xktjb_coassb/pageList'
        self.session=requests.Session()
    def login(self,username,userpass):
        headers1={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Host':'id.tsinghua.edu.cn',
            'Referer':'http://learn2018.tsinghua.edu.cn/f/login'
        }
        response = self.session.get(self.login_url, headers=headers1)
        


        post_data={
            'i_user':username,
            'i_pass':userpass,
            'atOnce':'true'
        }

        response=self.session.post(self.post_url,data=post_data,headers=headers1)
        ##print(response.status_code)
        ##print('------------------------')
        ##print(response.text)
        ##print('------------------------')
        if response.status_code==200:
            pass##print("auth successfully")
        url=self.redirect(response)
        #print(url)
        str='http://learn2018.tsinghua.edu.cn/b/j_spring_security_thauth_roaming_entry?'+url[(url.find('&')+1):]
        #print(str)


        headers2={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Host': 'learn2018.tsinghua.edu.cn',
            'Referer': url
        }
        #print(headers2)
        #print(self.session.cookies)
        response=self.session.get(str,headers=headers2)
        #print(response.status_code)
        #print(response.text)
        response=self.session.get(self.logined_url,headers=headers2)
        #print(response.status_code)
        #open('loginned.html','w',encoding='utf-8').write(response.text)
        headers3={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Host': 'learn2018.tsinghua.edu.cn',
            'Referer': 'http://learn2018.tsinghua.edu.cn/f/wlxt/index/course/student/'
        }
        post_data2={
            'aoData': '[{"name":"sEcho","value":1},{"name":"iColumns","value":5},{"name":"sColumns","value":",,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":"150"},{"name":"mDataProp_0","value":"function"},{"name":"bSortable_0","value":false},{"name":"mDataProp_1","value":"kcm"},{"name":"bSortable_1","value":true},{"name":"mDataProp_2","value":"jslx"},{"name":"bSortable_2","value":true},{"name":"mDataProp_3","value":"xnxq"},{"name":"bSortable_3","value":true},{"name":"mDataProp_4","value":"jsmc"},{"name":"bSortable_4","value":true},{"name":"iSortingCols","value":0}]'
        }
        response=self.session.post(self.lesson_url,data=post_data2,headers=headers3)
        lesson=response.json()
        open('lesson.json','w',encoding='utf-8').write(response.text)
        lesson_num=lesson['object']['iTotalRecords']
        lesson_num=int(lesson_num)
        lesson_id=[]
        for i in range(lesson_num):
            lesson_id.append(lesson['object']['aaData'][i]['wlkcid'])
        #print(lesson_id)




        

            


    def redirect(self,response):
        html=etree.HTML(response.text)
        return html.xpath('//div/a/@href')[0]




def main():
    #print("thu-crawler")
    username=input("\nusername:")
    password=input("\npassword:")
    #print("\nlogining...")
    a=Login()
    a.login(username,password)

if __name__=="__main__":
    main()
