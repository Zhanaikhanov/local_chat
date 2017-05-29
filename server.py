import http.server
import socketserver

from PIL import Image
import sys
import json
import urllib
import hashlib
from time import gmtime, strftime
import requests
from bs4 import BeautifulSoup
import random
import time

def hashgenerator(data):
	hash_1 = hashlib.sha256()
	hash_1.update(data.encode('UTF-8'))
	return hash_1.hexdigest()

def check(login, password):
	login = str(login)
	password = str(password)
	url = "http://intranet2.kbtu.kz/login.aspx"
	payload = {'uname':login, 'pwd':password}
	r = requests.Session().post(url, data = payload)
	html = r.text
	if 'welcome' in html:
		print(login,password,"true")
		return True
	else:
		print(login,password,"false")
		return False

cookies = {"cookie_data":{"name":"username","last_updated":"123123"}}

def check_cookie(data):
	if "Cookie" in data:
		cookie = data["Cookie"]
		if cookie in cookies:
			return True
	return False

def get_cookie(data):
	return data["Cookie"]	

PORT = int(sys.argv[1])
HOST = sys.argv[2]
print('on ',PORT)
two = open('123.jpeg','rb').read()
three = open('favicon.ico','rb').read()
class Handler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		global two, three
		
		if check_cookie(self.headers): 
			if self.path == '/':
				self.send_response(200)
				self.send_header("Content-type","text/html")
				self.end_headers()
				html = open('index.html').read()
				self.wfile.write(str(html).encode('ascii'))
			if self.path == '/phones.json':
				cookies[get_cookie(self.headers)]['last_updated'] = str(float(time.time()))

				fol = open('phones.json')
				json1 = fol.read()
				fol.close()
				self.send_response(200)
				self.send_header("Content-type","application/json")
				self.end_headers()
				self.wfile.write(str(json1).encode('ascii'))
			if self.path == '/123.jpeg':
				self.send_response(200)
				self.send_header("Content-type","image/jpeg")
				self.send_header("Content-Size","9018")				
				self.end_headers()
				self.wfile.write(two)
			if self.path == '/favicon.ico':
				self.send_response(200)
				self.send_header("Content-type","image/x-icon")
				self.send_header("Content-Size","258062")				
				self.end_headers()
				self.wfile.write(three)
			if self.path == '/website-design-background.jpg':
				self.send_response(200)
				self.send_header("Content-type","image/jpg")
				self.send_header("Content-Size","13049")			
				self.end_headers()
				self.wfile.write(open("website-design-background.jpg",'rb').read())

		else:	
			if self.path == "/":
				self.send_response(200)
				self.send_header("Content-type","text/html")
				self.send_header("Set-Cookie",str(hashgenerator(str(random.choice(range(10000))))))		
				self.end_headers()
				html = open('login.html').read()
				self.wfile.write(str(html).encode('ascii'))
			if self.path == '/website-design-background.jpg':
				self.send_response(200)
				self.send_header("Content-type","image/jpg")
				self.send_header("Content-Size","13049")			
				self.end_headers()
				self.wfile.write(open("website-design-background.jpg",'rb').read())
			if self.path == '/favicon.ico':	
				self.send_response(200)
				self.send_header("Content-type","image/x-icon")
				self.send_header("Content-Size","258062")				
				self.end_headers()
				self.wfile.write(three)

	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type","application/json")
		self.end_headers()
		lenth = int(self.headers['Content-Length'])
		post = self.rfile.read(lenth).decode('ascii')
		cookie_user = get_cookie(self.headers)
		current_time = float(time.time())
		user_name_1 = ''
		print(post)
		print("suka blyat 1")
		if cookie_user in cookies:
			print("suka blyat 2")	
			user_name_1 = cookies[cookie_user]["name"]
			print(user_name_1, end="----->")
			if str(post[:8]) == "comment=":
				print("suka blyat 3")	

				print("commenting")
				file = open('phones.json')
				json_data = json.loads(file.read())
				file.close()

				comment = str(post[8:])
				max_mes = len(json_data)
				if max_mes > 19:
					for i in range(1,max_mes):
						json_data[str(i)] = json_data[str(i+1)]
					
					json_data[max_mes] = {
						"name":user_name_1,
						"comment":comment,
						"id":str(random.choice(range(1000000,9999999))),
						"uploaded":str(float(time.time()))
						}
				
				else:
					print("suka blyat 4")	

					json_data[max_mes+1] = {
						"name":user_name_1,
						"comment":comment,
						"id":str(random.choice(range(1000000,9999999))),
						"uploaded":str(float(time.time()))
						}
				file = open('phones.json',"w")
				file.write(json.dumps(json_data))
				file.close()
				json2 = str.encode('{"status":"success"}')
				self.wfile.write(json2)

			elif str(post[:7]) == "update=" and post[7:12].isnumeric() and post[15:23] == "message=":
				print("suka blyat 5")	
				
				print("Editing...")
				
				message_id_for = post[7:14]
				new_message = post[23:]
				data_f = open('phones.json')
				datas = json.loads(data_f.read())
				data_f.close()
				id_Found = False
				for i in datas:
					ids = datas[str(i)]["id"]
					if message_id_for == ids and datas[str(i)]["name"] == user_name_1:
						datas[str(i)]["comment"] = new_message
						datas[str(i)]["uploaded"] = str(float(time.time()))

						id_Found = True
						data_f = open('phones.json','w')
						data_f.write(json.dumps(datas))
						data_f.close()
						break			
				if not id_Found or len(new_message)==0:
					print("suka blyat 6")	

					json2 = str.encode('{"status":"It is not yours..."}')
					self.wfile.write(json2)
				else:
					print("suka blyat 7")	
					
					json2 = str.encode('{"status":"changed"}')
					self.wfile.write(json2)

			elif post[:13] == "kill_message=" and post[13:].isnumeric():
				print("Deleting...")
				
				message_id_kill = post[13:]
				data_f = open('phones.json')
				datas = json.loads(data_f.read())
				data_f.close()
				id_Found = False
				position = ''
				if message_id_kill != "11111":
					for i in datas: 
						ids = datas[str(i)]["id"]
						if message_id_kill == ids and datas[str(i)]['name'] == user_name_1:
							position = i
							id_Found = True
							break	

					if not id_Found:
						json2 = str.encode('{"status":"It is not yours..."}')
						print(json2)
						self.wfile.write(json2)
					else:
						for i in range(int(position),len(datas)):						
							datas[str(i)] = datas[str(i+1)]
						datas.pop(str(len(datas)))
						data_f = open('phones.json','w')
						data_f.write(json.dumps(datas))
						data_f.close()
						json2 = str.encode('{"status":"success"}')
						self.wfile.write(json2)
			
				else:
					json2 = str.encode('{"status":"It is not yours..."}')
					print(json2)
					self.wfile.write(json2)
					self.send_response(200)

			elif post == "profile=get_info":
				print("suka blyat 10")	

				print('getting info...')
				about_data_base = json.loads(open("about.json").read())
				profile_data = str.encode( json.dumps(about_data_base[cookies[cookie_user]["name"]]) )
				self.wfile.write(profile_data)

			elif post == "log_out=1":
				print("suka blyat 9")	

				cookies.pop(cookie_user)
				f9 = open("about.json")
				about_data_base = json.loads(f9.read())
				f9.close()
				about_data_base[user_name_1]['last_seen'] = str(float(time.time()))
				json2 = str.encode('{"status":"success"}')
				self.wfile.write(json2)

			elif post == "che_tam=1":
				print("suka blyat 8")	

				last_updated_1 = cookies[cookie_user]['last_updated']
				file = open('phones.json')
				json_data = json.loads(file.read())
				file.close()

				opazdal = 0
				for i in json_data:
					if float(json_data[i]["uploaded"]) > float(last_updated_1):
						print("mes-->",float(json_data[i]["uploaded"]),"|last-->",float(last_updated_1))
						opazdal+=1
				opazdal_data = {"opazdal_na":opazdal}		
				json2 = str.encode(json.dumps(opazdal_data) )
				self.wfile.write(json2)
						
		
		else:
			print("suka blyat 11")	

			if post[:6] == "login=" and "&password=" in post[10:]:
				print("suka blyat 12")	
				
				name_base = open("names.json","r")
				names = json.loads(name_base.read())
				name_base.close()

				login = post[6:post.index("&password=")]
				password = post[ int(post.index("&password=") )+10:]

				if login in names:
					print("suka blyat 13")	

					if hashgenerator(password) == names[login]["password"]:
						cookies[cookie_user] = {}
						cookies[cookie_user]['name'] = login
						cookies[cookie_user]['last_updated'] = str(float(time.time()))

						json_response = str.encode('{"status":"success"}')
						self.wfile.write(json_response)
					else:
						json_response = str.encode('{"status":"Error 1"}')
						self.wfile.write(json_response)
				else:
					print("suka blyat 14")	

					if check(login,password):
						print("suka blyat 15")	

						names[login] = {}
						names[login]["password"] = hashgenerator(password)
						name_base = open("names.json","w")
						names = name_base.write(json.dumps(names))
						name_base.close()
						cookies[cookie_user]["name"] = login

						f9 = open("about.json")
						about_data_base = json.loads(f9.read())
						f9.close()
						about_data_base[login] = {}
						about_data_base[login] = {
						"login":login,
						"name":login,
						"surname":"empty",
						"date_of_birth":"empty",
						"email":"empty",
						"number":"empty",
						"github":"empty",
						"faculty":"empty",
						"course":"empty",
						"last_seen":"empty"
						}

						f9 = open("about.json",'w')
						f9.write(json.dumps(about_data_base))
						f9.close()

						profile_data = str.encode( json.dumps(about_data_base[user_name_1]) )
						self.wfile.write(profile_data)			
						json_response = str.encode('{"status":"success"}')
						self.wfile.write(json_response)

					else:
						print("suka blyat 16")	

						json_response = str.encode('{"status":"Error 2"}')
						self.wfile.write(json_response)
			else:
				print("suka blyat 15")	

				json_response = str.encode('{"status":"Error 4 please authorize"}')
				self.wfile.write(json_response)
				

try:	
	httpd = socketserver.TCPServer((HOST, PORT), Handler)
	httpd.serve_forever()
except:
	print('error')