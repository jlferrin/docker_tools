#!/bin/python

import requests
import getopt
import sys


url_servidor = ''
url_catalogo = '/v2/_catalog'
url_tag_list = '/v2/{}/tags/list'
url_manifests_list = '/v2/{}/manifests/{}'
url_blobs_list = '/v2/{}/blobs/{}'

def usage ():
	print ('Usage:')
	print (' info_docker_registry [OPTION]... SERVER_URL')
	print ('')
	print (' SERVER_URL: http://SERVER:PORT')
	print ('')
	print ('Options:')
	print ('-h, --help		This help')
	print ('-c, --catalog 		Show the catalog images')
	print ('-i, --image=IMAGE	Information about a IMAGE')
	print ('-t, --tag=TAG 		Information about a TAG')
	print ('-a, --architecture	Show the architecture')
	print ('-b, --blob 		Information about blobs')
	print ('-y, --history 		Information about history')
#	print ('-v, --verbose 		Verbose mode')

def get_respuesta(url):
	try:
		respuesta = requests.get(url)
		if respuesta.status_code != 200:
			raise ApiError('Error: GET {} {}'.format(url,respuesta.status_code))
		json_obj = respuesta.json() 
		return json_obj
	except requests.exceptions.RequestException as err:
		print('Error: {}'.format(err))
		sys.exit(2)


def main ():
	
	try:
		options, remainder = getopt.getopt(sys.argv[1:], 'ci:t:abhy')
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)

	f_imagen = False
	f_catalogo = False
	f_tag = False
	f_blob = False
	f_history = False
        f_architecture = False

	lista_imagenes = []
	lista_tags = []

	if len(remainder) != 1:
		print('Error: URL needed\n')
		usage()
		sys.exit(2)

	if len(options) == 0:
		options.append( ('-c','') )

	url_servidor = remainder.pop()

	for opt,arg in options:
		if opt in ('-h','--help'):
			usage()
			sys.exit(2)
		elif opt in ('-c','--catalog'):
			resp_catalogo = get_respuesta(url_servidor+url_catalogo)
			f_catalogo = True
			if not f_imagen:
				lista_imagenes = resp_catalogo["repositories"]
		elif opt in ('-i','--image'):
			f_imagen = True
			lista_imagenes = [ arg ]
		elif opt in ('-v','--verbose'):
			f_verbose = True
		elif opt in ('-t','--tag'):
			f_tag = True	
			lista_tags.append( arg )
		elif opt in ('-b','--blob'):
			f_blob = True
		elif opt in ('-y','--history'):
			f_history = True
		elif opt in ('-a','--architecture'):
			f_architecture = True
		else:
			print('Error: Unknow option\n')
			usage()
			sys.exit(2)

	for imagen in lista_imagenes:
		print('Image: {} '.format(imagen))
		if not f_tag:
			resp_tag_list = get_respuesta(url_servidor+url_tag_list.format(imagen))
			lista_tags = resp_tag_list["tags"]
		for tag in lista_tags:
			print(' Tag: {}'.format(tag))
			resp_manifests_list = get_respuesta(url_servidor+url_manifests_list.format(imagen,tag))
			if f_architecture:
				print('  Arquitecture: {}'.format(resp_manifests_list["architecture"]))
			if f_blob:
				print('  fsLayers')
				for fsLayer in resp_manifests_list["fsLayers"]:
					print('   {}'.format(fsLayer))
			if f_history:
				print('  history')
				for history in resp_manifests_list["history"]:
					print('   {}'.format(history))
#			resp_blobs_list = requests.head(protocolo+servidor+':'+puerto+url_blobs_list.format(imagen,fsLayer))
#			print('   blobs list: {}'.format(resp_blobs_list.text))

if __name__ == "__main__":
    main()
