#!/usr/bin/python
# -*- coding: utf-8 -*-

from weibopy.auth import OAuthHandler
from weibopy.api import API
import webbrowser
import sys
import os
import cPickle as pickle

class AlfredWeibo():

    consumer_key= "3099244098"
    consumer_secret ="28621138908451ae0e0feb121eecbdac"

    auth = OAuthHandler(consumer_key, consumer_secret)

    setting = {}
    weibos = []

    def load_setting(self):
        with open ('setting.pickle','rb') as f:
            self.setting = pickle.load(f)

    def save_setting(self):
        with open ('setting.pickle','wb') as f:
            pickle.dump(self.setting,f)

    def save_weibo(self):
        with open ('savedWeibo.pickle','wb') as f:
            pickle.dump(self.weibos,f)

    def get_pin(self):
        
        auth_url = self.auth.get_authorization_url()

        request_token = self.auth.request_token.key
        request_token_secret = self.auth.request_token.secret

        if (request_token != None and request_token.count > 0):
            print "wb pin <浏览器里的pin>"
            self.setting['request_token'] = request_token
            self.setting['request_token_secret'] = request_token_secret
            self.save_setting()
            webbrowser.open(auth_url)
        else:
            print '出错啦，等下在搞吧～～'


    def get_access_token(self,pin):
        self.load_setting()
        self.auth.set_request_token(self.setting['request_token'],
                self.setting['request_token_secret'])
        access_token = self.auth.get_access_token(pin);

        if (access_token.key != None and access_token.secret != None
        and access_token.key.count >0 and access_token.secret.count >0):
            self.setting['access_token'] = access_token.key;
            self.setting['access_token_secret'] = access_token.secret;
            self.save_setting()
            print '好了，搞定了！可以发微博啦～～～～'
        else:
            print "出错啦，等下在搞吧～～"

    def update_weibo(self,message):
        self.load_setting()
        self.auth.set_request_token(self.setting['request_token'],
                self.setting['request_token_secret'])
        self.auth.set_access_token(self.setting['access_token'],
                self.setting['access_token_secret'])

        api = API(self.auth)

        is_updated = api.update_status(message)

        if(is_updated):
            print '你又在微博上跟大家说了一句话~~'

    def save(self,message):
        self.weibos.append(message)
        self.save_weibo()
        print "要记得发出去哦～～～"

    def nowplaying(self,message):
        showString = os.popen("osascript track_info.scpt").readline()

        if (showString != ""):


            if  message != "":
                showString = showString[0:-1] + '>>>' + message

            self.update_weibo(showString)
        else:
            showString = "亲，你的耳朵里没有声音哦，你是不是弄错了阿！"

        print showString

def main():
    argv = sys.argv[1:][0]
    parm = argv.split(" ")

    alfredWeibo = AlfredWeibo()

    if(parm[0] == "setup"):
        alfredWeibo.get_pin()
    elif(parm[0] == "pin"):
        alfredWeibo.get_access_token(parm[1])
    elif(parm[0] == "reset"):
        alfredWeibo.reset()
    elif(parm[0] == "np"):
        message = argv[2:]
        alfredWeibo.nowplaying(message)
    elif( parm[0] == 'nowplaying' ):
        message = argv[10:]
        alfredWeibo.nowplaying(message)
    else:
        alfredWeibo.update_weibo(argv)


if __name__ == "__main__":
    main()
