import http.server
import socketserver
import os
import sys
import json
import requests
from urllib import parse
import random


def get_bonus_malus(iin):
	print(iin)
	r = requests
	t = r.get('https://promarket.kz/ru/insurance/auto/angular2getClientByIin?iin={}'.format(iin))
	class_ogpo = t.text
	return class_ogpo

def calcul(dat):
	r = dat.split("&")
	t = []
	for i in r:
		if i[:13] == 'dannye[users]':
			i = 'ogpo_person'+i[13:];
			t.append(i)
		elif i[:17] == 'dannye[vehiciles]':
			i = 'ogpo_tc'+i[17:];
			t.append(i)

	t = '&'.join(t)

	a = requests.Session()
	headers = {
	     "Host":"strahoffka.kz",
	     "Content-Type":"application/x-www-form-urlencoded"}
	b = a.post('http://strahoffka.kz/order/step1/', headers = headers, data = t)

	j = json.loads(b.text)

	return j['data']['price']





PORT = int(sys.argv[1])
HOST = sys.argv[2]
print('on ',PORT)
class Handler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):	
		print(self.path)
		if self.path == '/':
			self.send_response(200)
			self.send_header("Content-type","text/html")
			self.end_headers()
			html = open('index.html').read()
			self.wfile.write(str(html).encode('utf8'))
		if self.path == '/driving2.jpg':
			self.send_response(200)
			self.send_header("Content-type","image/jpeg")
			self.send_header("Content-Size","31644")				
			self.end_headers()
			self.wfile.write(open('driving2.jpg','rb').read())
	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type","application/json")
		self.end_headers()
		lenth = int(self.headers['Content-Length'])
		post = self.rfile.read(lenth)
		post = parse.unquote(post.decode())
		print(post)
		if post[:4] == 'iin=':
			json2 = {}
			json2['status'] = 'success'
			json2['bonus_malus'] = get_bonus_malus(post[4:])
			profile_data = str.encode( json.dumps(json2) )
			self.wfile.write(profile_data)
		elif "dannye[users]" in post:
			json2 = {}
			json2['status'] = 'success'
			json2['price'] = calcul(post)
			price = str.encode( json.dumps(json2) )
			self.wfile.write(price)

try:	
	httpd = socketserver.TCPServer((HOST, PORT), Handler)
	httpd.serve_forever()
except:
	print('level')