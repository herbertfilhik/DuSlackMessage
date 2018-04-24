import requests
import json

URL_API = "https://slack.com/api/chat.postMessage"
SLACK_USER = "Jenkins"
SLACK_IMG = "https://wiki.jenkins.io/download/attachments/2916393/logo.png?version=1&modificationDate=1302753947000&api=v2"#"http://afonsof.com/jenkins-material-theme/images/logo.svg"
API_KEY = "xoxp-97000916645-331284306803-349504845671-0d1d9254a459abbee61374e02cce82cd"
AUTHORIZATION_HEADER = {"Authorization" : "Bearer " + API_KEY}


class Slack:

	text = "Mensagem Default"
	attachments = None

	def __init__(self, channel=None, user=None):
		self.channel = channel
		self.user = user


	def send(self, text, attachments=None):
		self.text = text
		self.attachments = attachments

		if self.channel == None:
			raise Exception("Destinatário da menssagem não foi definido!")

		try:
			response = self.make_request(self.channel, self.text, self.attachments)
			ok = dict(response.json())['ok']
			if ok:
				print("Mensagem Enviada Com Sucesso!")
			else:
				raise Exception("Resposta da API indica que a mensagem não foi devidamente enviada!")
		except Exception as e:
			raise Exception("Erro ao realizar requisição: " + str(e))



	def make_request(self, channel, text, attachments):
		return requests.post(
				URL_API,
				data=json.dumps({'channel': channel, 'text' : text, 'icon_url' : SLACK_IMG, 'username' : SLACK_USER}),
				headers={'Content-Type': 'application/json', **AUTHORIZATION_HEADER}
			)