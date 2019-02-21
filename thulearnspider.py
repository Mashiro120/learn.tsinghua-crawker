import requests
import sys
from lxml import etree
import os
import re
class spider(object):
    def __init__(self,username,userpass):
        self.login_url='http://learn.tsinghua.edu.cn/f/login'
        self.post_url='https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do'
        self.logined_url='http://learn2018.tsinghua.edu.cn/f/wlxt/index/course/student/'
        self.lesson_url='http://learn2018.tsinghua.edu.cn/b/wlxt/kc/v_wlkc_xs_xktjb_coassb/pageList'
        self.username=username
        self.userpass=userpass
        self.session=requests.Session()
    def login(self):
        headers1={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Host':'id.tsinghua.edu.cn',
            'Referer':'http://learn2018.tsinghua.edu.cn/f/login'
        }
        response = self.session.get(self.login_url, headers=headers1)
        


        post_data={
            'i_user':self.username,
            'i_pass':self.userpass,
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
        strxxx='http://learn2018.tsinghua.edu.cn/b/j_spring_security_thauth_roaming_entry?'+url[(url.find('&')+1):]
        #print(strxxx)


        headers2={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Host': 'learn2018.tsinghua.edu.cn',
            'Referer': url
        }
        #print(headers2)
        #print(self.session.cookies)
        response=self.session.get(strxxx,headers=headers2)
        #print(response.status_code)
        #print(response.text)
        response=self.session.get(self.logined_url,headers=headers2)
        #print(response.status_code)
        #open('loginned.html','w',encoding='utf-8').write(response.text)
        
    def downloader(self):
        self.login()
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
        lesson_name=[]
        
        for i in range(lesson_num):
            lesson_id.append(lesson['object']['aaData'][i]['wlkcid'])
            lesson_name.append(lesson['object']['aaData'][i]['kcm'])
    
        for i in range(lesson_id):
            self.lesson_downloader(lesson_id[i],lesson_name[i])
        
        #print(lesson_name)
        #self.lesson_downloader(lesson_id[67],lesson_name[67])

    def lesson_downloader(self,lesson,lesson_name):
        # print(lesson)
        oripath=os.getcwd()
        download_path=oripath+'\\'+lesson_name
        if lesson_name not in os.listdir():
            os.makedirs(download_path)
        headers3={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Host': 'learn2018.tsinghua.edu.cn',
            'Referer': 'http://learn2018.tsinghua.edu.cn/f/wlxt/index/course/student/'
        }
        strxxx='http://learn2018.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjflb/student/pageList?wlkcid='+lesson+'&sfgk=0'
        response=self.session.get(strxxx,headers=headers3)
        tabs=response.json()
        tabs_id=[]
        #cnt=1
        for tab in tabs['object']['rows']:
            tabs_id.append(tab['id'])
            if tab['bt'] not in os.listdir(download_path+'\\'):
                os.makedirs(download_path+'\\'+tab['bt'])
        for tab_id in tabs_id:
            strxxx='http://learn2018.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/kjxxb/'+lesson+'/'+tab_id
            response=self.session.get(strxxx,headers=headers3)
            file_list=response.json()['object']
            #open(str(cnt)+'.json','w',encoding='utf-8').write(response.text)
            #cnt+=1
            for file_id in file_list:
                links='http://learn2018.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid='+file_id[7]
                print(file_id[1])
                response=self.session.get(links,headers=headers3)
                filename=re.findall('"(.*)"',response.headers['Content-Disposition'])
                with open(download_path+'\\'+tab['bt']+'\\'+filename,'wb') as f:
                    f.write(response.content) 


    def redirect(self,response):
        html=etree.HTML(response.text)
        return html.xpath('//div/a/@href')[0]




def main():
    #print("thu-crawler")
    username=input("\nusername:")
    password=input("\npassword:")
    #print("\nlogining...")
    a=spider(username,password)
    a.downloader()

if __name__=="__main__":
    main()
