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
		

	def connect(self):
		url = self.settings.items['systems'][self.system]['rest_url']
		credentials = self.user + ':' + self.password
		auth = base64.b64encode(credentials.encode()).decode()

		aut.connection(
			url=url, 
			auth=auth,                  # base64 userid:password 
			noproxy=True,               # defalut False 
			sslverify=False,            # default True
			cert='/path/to/certfile',   # default None
			timeout=60                  # default 3600  
		)

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
