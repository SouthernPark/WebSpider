import requests
from bs4 import BeautifulSoup



class Login(object):
    def __init__(self, course_web, path):
        self.headers = {
            'Referer': 'http://ice.xjtlu.edu.cn/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Host': 'ice.xjtlu.edu.cn'
        }
        self.login_url = 'http://ice.xjtlu.edu.cn/'
        self.post_url = 'https://ice.xjtlu.edu.cn/login/index.php'
        self.course_web = course_web
        self.path = path
        self.session = requests.Session()

    #this function is used to get the hidden logintoken code on ice
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = BeautifulSoup(response.text, "html.parser")
        attrbutes = {"type": "hidden", "name": "logintoken"}
        logintoken = selector.find(name="input", attrs= attrbutes)  # from here find logintoken
        token = logintoken["value"]
        return token

    def login(self, name, password):
        post_data = {
            'anchor':'',
            'logintoken': self.token(),
            'username': name,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print("log into ice")

            pdf_web, pdf_name = self.get_pdf_website()  #get the pdf web and name of CSE101
            self.download_pdf(pdf_web, pdf_name)


    def get_pdf_website(self):
        response = self.session.get(self.course_web, headers=self.headers)
        if response.status_code == 200:

            print("redirected to " + self.course_web)
            soup = BeautifulSoup(response.text, "html.parser")
            soup_pdf = soup.select(".activityinstance a")
            pdf_soup = []  #this is the the websites that is real pdf soup
            pdf_web = []   #this contains the real pdf websites
            pdf_name = []   # this contains the pdf names
            for pdf in soup_pdf:
                download = pdf["onclick"][13:-17]
                if "resource" in download:
                    pdf_soup.append(pdf)
            for i in pdf_soup:

                pdf_name.append(i.find(name = "span", class_ = "instancename").text)
                pdf_web.append(i["onclick"][13:-17])
        return pdf_web, pdf_name

    def download_pdf(self,pdf_web ,pdf_name):
        for i in range(len(pdf_web)):
            response = self.session.get(pdf_web[i], headers=self.headers)
            path = self.path + pdf_name[i] + ".pdf"
            f = open(path, "wb")
            f.write(response.content)
            f.close()
        print("download finished")

course_web = "https://ice.xjtlu.edu.cn/course/view.php?id=153"
path = "/home/sherlocky/下载/CSE107/"
login = Login(course_web,path)
login.login("Qiangqiang.liu17", "uEAjvHmc")

