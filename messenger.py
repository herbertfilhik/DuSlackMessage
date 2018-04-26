from slack import *
import argparse
import sys

def send_messages(channel, message, attachments):
	try:
		Slack(channel).send(message, attachments)
	except Exception as e:
		print(str(e))


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	
	parser.add_argument("-c", "--channel", help="Canal SLACK a receber a mensagem!", type=str)
	parser.add_argument("-m", "--mensagem", help="Mensagem a ser enviada!", type=str)
	parser.add_argument("-a", "--attachments", help="Imagens a serem exibidas na mensagem. Obs: Informar url da imagem.", type=str)
	
	args = parser.parse_args()

	if args.mensagem == None or args.channel == None:
		parser.print_help()
		sys.exit(0)

	send_messages(args.channel, args.mensagem, args.attachments)