import pew
from main import menugen
import network
import time

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)
pew.init()
screen = pew.Pix()

class Menu:
	def __init__(self):
		self.selected = 0

	def update(self):
		pass

	def action(self, s):
		stack.pop()

class StaAp(Menu):
	entries = ['Sta', 'AP']

	def action(self, s):
		if s == 0:
			stack.append(Sta())
		elif s == 1:
			stack.append(Ap())

class Sta(Menu):
	def __init__(self):
		Menu.__init__(self)
		self.active = True
		self.entries = ['', 'connect', 'ifconfig', 'scan']

	def update(self):
		self.active = sta.active()
		self.entries[0] = '+active+' if self.active else '-active-'

	def action(self, s):
		if s == 0:
			self.active = not self.active
			sta.active(self.active)
		elif s == 1:
			stack.append(Connect())
		elif s == 2:
			stack.append(Ifconfig(sta))
		elif s == 3:
			stack.append(Scan())

class Ifconfig(Menu):
	def __init__(self, interface):
		Menu.__init__(self)
		self.interface = interface

	def update(self):
		self.entries = [a + b for a, b in zip(('IP:', 'NM:', 'GW:', 'NS:'), self.interface.ifconfig())]

def _connect(ssid, password):
	try:
		sta.disconnect()
		while sta.isconnected():
			time.sleep(0.1)
		sta.connect(ssid, password)
		for i in range(8):
			screen.pixel(i, 7, 3)
			if sta.isconnected():
				screen.box(1, 0, 7, 8, 1)
				break
			status = sta.status()
			if status != network.STAT_CONNECTING:
				screen.box(2, 0, 7, i, 1)
				pew.show(screen)
				time.sleep(1)
				stack.pop()
				stack.append(Message({network.STAT_WRONG_PASSWORD: 'wrong password', network.STAT_NO_AP_FOUND: 'no AP found', network.STAT_CONNECT_FAIL: 'connection failed'}.get(status, str(status))))
				return
			pew.show(screen)
			time.sleep(2)
		else:
			screen.box(2, 0, 7, 8, 1)
		pew.show(screen)
		time.sleep(1)
		stack.pop()
	except OSError as e:
		stack.append(Message('Error: ' + str(e)))

class Connect(Menu):
	def __init__(self):
		Menu.__init__(self)

	def update(self):
		try:
			with open('networks', 'r') as f:
				self.networks = [l.rstrip('\r\n').split('\t') for l in f]
		except OSError:
			self.networks = [['<not found>', '']]
		self.entries = [n[0] for n in self.networks]

	def action(self, s):
		_connect(*self.networks[s])

class Scan(Menu):
	def update(self):
		try:
			self.results = sta.scan()
			if self.results:
				self.entries = ['{} ({}, {})'.format(str(r[0], 'utf-8'), r[3], {0: 'open', 1: 'WEP', 2: 'WPA-PSK', 3: 'WPA2-PSK', 4: 'WPA/WPA2-PSK'}.get(r[4], '?')) for r in self.results]
			else:
				self.entries = ['--no networks found--']
				self.results = None
		except OSError as e:
			self.entries = ['Error: ' + str(e)]
			self.results = None

	def action(self, s):
		if self.results is None:
			stack.pop()
		elif not 1 <= self.results[s][4] <= 4:
			_connect(str(self.results[s][0], 'utf-8'), None)

class Ap(Menu):
	def update(self):
		self.active = ap.active()
		if self.active:
			name = ap.config('essid')
			self.entries = ['+active+', 'name:' + name, 'ifconfig']
		else:
			self.entries = ['-active-']

	def action(self, s):
		if s == 0:
			self.active = not self.active
			ap.active(self.active)
			if self.active:
				import ubinascii
				essid = b"MicroPython-%s" % ubinascii.hexlify(ap.config("mac")[-3:])
				password = b"micropythoN"
				for i in range(8):
					screen.pixel(i, 7, 3)
					pew.show(screen)
					i += 1
					time.sleep(0.1)
					if ap.active():
						break
				ap.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=password, hidden=False)
				stack.append(Message('pass:{:s}\nname:{:s}'.format(password, essid)))
		elif s == 2:
			stack.append(Ifconfig(ap))

class Message(Menu):
	def __init__(self, msg):
		Menu.__init__(self)
		self.entries = msg.split('\n')

stack = [StaAp()]
while len(stack) != 0:
	menu = stack[-1]
	menu.update()
	for selected in menugen(screen, menu.entries, menu.selected):
		if pew.keys() & pew.K_X:
			stack.pop()
			break
		pew.show(screen)
		pew.tick(1/24)
	else:
		time.sleep(0.1)
		menu.selected = selected
		menu.action(selected)
