import requests
import json
import os, sys

URL_API = "https://slack.com/api/chat.postMessage"
SLACK_USER = "Jenkins"
SLACK_IMG = "https://wiki.jenkins.io/download/attachments/2916393/logo.png?version=1&modificationDate=1302753947000&api=v2"
API_KEY = "xoxb-353771507446-yGXefV3x3yVBcUI0WhuW91pF"
AUTHORIZATION_HEADER = {"Authorization" : "Bearer " + API_KEY}
CONTENTTYPE_HEADER = {'Content-Type': 'application/json'}


class Slack:

	text = "Mensagem Default"
	attachments = None

	def __init__(self, channel=None, user=None):
		self.channel = channel
		self.user = user


	def send(self, text, attachments=None):

		"""" Valida os dados antes do envio da requisição e trata o retorno após a mesma """
		
		self.text = text
		self.attachments = attachments

		if self.channel == None:
			raise Exception("Destinatário da menssagem não foi definido!")

		try:
			response = self.make_request(self.build_data(self.channel, self.text, self.attachments))
			ok = dict(response.json())['ok']
			if ok:
				print("Mensagem Enviada Com Sucesso!")
			else:
				raise Exception("Resposta da API indica que a mensagem não foi devidamente enviada!")
		except Exception as e:
			raise Exception("Erro ao realizar requisição: " + str(e))


	def make_request(self, JSONdata):

		""" Efetivamente executa a requisição a API do Slack """

		return requests.post(
				URL_API,
				data=JSONdata,
				headers={**CONTENTTYPE_HEADER, **AUTHORIZATION_HEADER}
			)

	def build_data(self, channel, text, attachments):
		
		encoder = json.JSONEncoder()

		data = {
			'channel': channel,
			'text' : text,
			'icon_url' : SLACK_IMG,
			'username' : SLACK_USER
		}

		if self.test_attachment(attachments):
			attachdata = {
				'attachments' : [
					{
						"title": "Imagem:",
						'image_url' : attachments
					}
				]
			}
			data.update(attachdata)
		return encoder.encode(data)

	def test_attachment(self, attachments):

		""" Testa a url da imagem a ser exibida na mensagem, caso não seja encontrada nenhuma imagem será anexada"""
		
		if attachments == None:
			return False
		try:
			return requests.get(attachments).ok
		except Exception as e:
			print("Erro ao buscar a imagem para anexar a mensagem!")
			return False