from __future__ import unicode_literals

import os
from os import environ
import re
import sys
import youtube_dl
from bs4 import BeautifulSoup
import requests
import lxml.html

class dl:
    global session_requests
    session_requests = requests.session()
    def login(self):
        self.course_url = input("Enter Course You Want To Download :    ")

        self.email = input('Enter Your Email ? ')

        self.password = input('Enter Your Password ?')

        if self.email and self.password and self.course_url:
            try:
                print("Hang On , I Am Trying To Logging In To Your Account\n")
                if "codewithmosh" in self.course_url:
                    login_url = "https://sso.teachable.com/secure/146684/users/sign_in?flow_school_id=146684"
                login_page = session_requests.get(login_url).text
                tree = lxml.html.fromstring(login_page)
                authenticity_token = list(set(tree.xpath("/html/body/div/div/div/div/div/div/div[1]/div/form/input[2]/@value")))[0]
                print("Got Login Page & Our Authenticity Token \t",authenticity_token)
                payload = {
                    "authenticity_token": authenticity_token,
                    "commit": "Log In",
                    "user[email]": self.email,
                    "user[password]": self.password,
                    "user[school_id]": "146684",
                    "utf8": "✓"

                     }
                response = session_requests.post(login_url,data=payload)
                if "Invalid Email or password" in response.text:
                    print("Login Failed : Invalid Email & Password")
                else:
                    print("Login Succesfull")
                    self.getSectionAndLinks(self.course_url)

            except Exception as e:
                print(e)
                print("Maybe Your Internet Is Not Working\n")
                sys.exit(1)


    def getSectionAndLinks(self,url):
        self.url = url
        index = url.index('com') + 3
        self.domain = self.url[0:index]
        try:
            print("Collecting Course Information ... ")
            data = requests.get(self.url)
            soup = BeautifulSoup(data.text,'html.parser')
            courseName = input("Name Of Folder You Want To Save It In ? :   ")
            print(courseName)

            try:
                os.mkdir(courseName.replace(":","-"))
                os.chdir(courseName.replace(":","-"))
                print("Made Main Course Folder\n")
            except Exception as e:
                print(e)
                os.chdir(courseName.replace(":","-"))
            print("Getting Course Sections ... ")
            folders =[]
            c=1
            sections = soup.find_all(class_="section-title")
            for s in sections:
                section_name = s.text.replace("Available in", "").replace("days","").replace("after you enroll","").replace("day","").strip()
                folder = str(c)+"."+str(section_name.replace(":","-"))
                c+=1
                print(folder)
                try:
                    os.mkdir(folder)
                    os.chdir(folder)
                    dir_path = os.path.dirname(os.getcwd())
                    print(dir_path+"\\"+ folder + "\\")
                    folders.append(dir_path+"\\"+ folder + "\\")

                    os.chdir('../')
                except Exception as e:
                    print(e)
                    os.chdir(folder)
                    dir_path = os.path.dirname(os.getcwd())
                    print(dir_path + "\\" + folder + "\\")
                    folders.append(dir_path + "\\" + folder + "\\")


                    os.chdir('../')
                print("\nFound Section :    ",folder,"\n")
                #Let's get all the links now
            lecture_list= soup.find_all("ul",class_="section-list")
            p=0
            for secs in lecture_list:
                links =[]
                titles =[]
                z=1
                for l in secs.find_all("a", class_="item"):
                    title = str(z)+"."+" ".join(l.text.replace("Preview", "").replace("Start", "").replace("\n", "").replace(":","-").strip().split())
                    z+=1
                    link = "https://codewithmosh.com" + l.get('href')
                    print(title)
                    print(link)

                    titles.append(title)
                    links.append(link)
                print(folders[p])
                self.download_video(titles,links,folders[p])
                p+=1
                print("########################################################")

        except Exception as e:
            print(e)
            sys.exit(1)
    def download_video(self,titles,links,folders):
        handle = open('logs.txt','w')
        self.title =titles
        self.urls = links
        self.path = folders
        for i in range(0,len(self.urls)):
            try:        
                video_page = session_requests.get(self.urls[i]).text
                download_page = BeautifulSoup(video_page,'html.parser')
                try:
                    download_link = download_page.find("a",class_="download").get('href')
                    print(download_link)
                    print("Downloading With Youtube-DL\n")
                    # handle.write(download_link)
                    ydl_opts ={
                        'outtmpl': self.path+"\\"+self.title[i]+".mp4"

                    }
                     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                         ydl.download([download_link])
    
                except Exception as e:
                    print(e)
                    tempPath =  self.path+"\\"+self.title[i]+".html"
                    handle= open(tempPath,'w')
                    handle.write(video_page)
                    handle.close()

                    pass
            except Exception as e :

                print(self.urls[i])
                print(e)
               
                pass



dl  = dl()
dl.login()
