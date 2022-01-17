import base64
import automic_rest as aut
from . settings import Settings

class Automic():
	def __init__(self, system=None, client=None, user=None, password=None):
		self.settings = Settings()
		self.user = self.settings.items['user']
		self.password = self.settings.items['password']
		self.client = client
		self.system = system.lower()
		self.sslverify = self.settings.items['systems'][self.system]['rest_sslverify']
		self.sslcert = self.settings.items['systems'][self.system]['rest_sslcert']
		self.noproxy = self.settings.items['systems'][self.system]['rest_noproxy']
		
	def isBase64(self, s):
		try:
			base64.b64encode(base64.b64decode(s)) == s
			return True
		except Exception:
			return False

	def connect(self):
		try:
			url = self.settings.items['systems'][self.system]['rest_url']
			if self.isBase64(self.password):
				password = base64.b64decode(self.password).decode("utf-8")
			else:
				password = self.password
			
			credentials = self.user + ':' + password
			auth = base64.b64encode(credentials.encode()).decode()
			
			aut.connection(
				url=url, 
				auth=auth,                  # base64 userid:password 
				noproxy=self.noproxy,       # defalut False 
				sslverify=self.sslverify,   # default True
				cert=self.sslcert,   		# default None
				timeout=60                  # default 3600  
			)
			return True
		except:
			return False

	def list_executions(self):
		try:
			return aut.listExecutions(client_id=self.client).response['data']
		except:
			return None

	def list_agents(self):
		try:
			return aut.listAgents(client_id=self.client).response['data']
		except:
			return None

	def health_check(self):
		try:
			return aut.healthCheck(client_id=self.client).response
		except:
			return None
