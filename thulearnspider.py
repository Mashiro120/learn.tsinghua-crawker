import requests
import sys




class Login(object):
    def __init__(self):
        self.headers={
            'Referer':'http://learn.tsinghua.edu.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3642.0 Safari/537.36',
            'Host':'learn.tsinghua.edu.cn'
        }
        self.login_url='http://learn.tsinghua.edu.cn/'
        self.post_url='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
        self.logined_url='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/mainstudent.jsp'
        self.session=requests.Session()
    def login(self,username,userpass):
        print("func:login")
        response = self.session.get(self.login_url, headers=self.headers)
        post_data={
            'userid':username,
            'userpass':userpass,
            'submit1':"%E7%99%BB%E5%BD%95"
        }
        response=self.session.post(self.post_url,data=post_data,headers=self.headers)
        print(response.status_code)
        if response.status_code==200:
            print("auth successfully")
        response=self.session.get(self.logined_url,headers=self.headers)
        print(response.status_code)
        if response.status_code==200:
            print("login successfully")
            print(response.text)


def main():
    print("main")
    a=Login()
    a.login(username,password)
if __name__=="__main__":
    main()
     
