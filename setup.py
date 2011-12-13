#!/usr/bin/python
# -*- coding: utf-8 -*-

from weibopy.auth import OAuthHandler
from weibopy.api import API
import webbrowser
import sys
import cPickle as pickle

class AlfredWeibo():

	consumer_key= "3099244098"
	consumer_secret ="28621138908451ae0e0feb121eecbdac"

	auth = OAuthHandler(consumer_key, consumer_secret)

	setting = {}

	def load_setting(self):
		with open ('setting.pickle','rb') as f:
			self.setting = pickle.load(f)

	def save_setting(self):
		with open ('setting.pickle','wb') as f:
			pickle.dump(self.setting,f)

	def get_pin(self):
		
		auth_url = self.auth.get_authorization_url()

		self.setting['request_token'] = self.auth.request_token.key;
		self.setting['request_token_secret'] = self.auth.request_token.secret;
		self.save_setting();

		webbrowser.open(auth_url)

	def get_access_token(self,pin):
		self.load_setting()
		self.auth.set_request_token(self.setting['request_token'],self.setting['request_token_secret'])
		access_token = self.auth.get_access_token(pin);

		self.setting['access_token'] = access_token.key;
		self.setting['access_token_secret'] = access_token.secret;

		self.save_setting()

	def update_weibo(self,message):
		self.load_setting()
		self.auth.set_request_token(self.setting['request_token'],self.setting['request_token_secret'])
		self.auth.set_access_token(self.setting['access_token'],self.setting['access_token_secret'])

		api = API(self.auth)

		is_updated = api.update_status(message)

		if(is_updated):
			print '你又在微博上跟大家说了一句话'


def main():
    argv = sys.argv[1:][0]
    parm = argv.split(" ")

    alfredWeibo = AlfredWeibo();

    if(parm[0] == "setup"):
    	alfredWeibo.get_pin();
    if(parm[0] == "pin"):
    	alfredWeibo.get_access_token(parm[1])
    else:
    	alfredWeibo.update_weibo(argv)


if __name__ == "__main__":
    main()