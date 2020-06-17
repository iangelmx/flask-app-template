# -*- coding: utf-8 -*-
from flask import ( Flask, jsonify, send_file, request, 
                    render_template ,render_template_string, make_response, 
                    send_from_directory, redirect  )
from config.includes import *

settings = json.loads( open("./includes/settings.json", "r").read() )

SECRET_KEY = settings['secret_key']
UPLOAD_FOLDER = settings['uploads']['upload_folder']
MAX_SIZE_FILES = settings['uploads']['max_file_size_to_receive_MB'] * 1024 * 1024
PREFIX_APP = settings['prefix_webpath_app']

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_SIZE_FILES

CORS(app)

''' NO TOCAR:  '''
#Permite la comunicación entre distintos dominios
@app.after_request
def after_request(response):
  #response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,From,forceToDo,Auth')
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
  return response

@app.route(PREFIX_APP+'/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def validaOrigen(request, sitiosPermitidos):
	#Valida que se estén haciendo peticiones desde sitios de confianza
	for a in request.environ:
		pass#print(a,":",request.environ[a])
	if 'HTTP_ORIGIN' in request.environ:
		if request.environ['HTTP_ORIGIN'] in sitiosPermitidos:
			return True
	elif 'HTTP_FROM' in request.environ:
		if request.environ['HTTP_FROM'] in sitiosPermitidos:
			return True
	elif 'HTTP_REFERER' in request.environ:
		if request.environ['HTTP_REFERER'] in sitiosPermitidos:
			return True
	return False

'''
----------------------------------------------------------------------------
----------------------------------------------------------------------------
ERROR PAGES
----------------------------------------------------------------------------
----------------------------------------------------------------------------
'''

@app.errorhandler(404)
def not_found(error):
	return render_template('/ErrorPages/404.html'),404

@app.errorhandler(403)
def forbidden(error):
	return render_template('/ErrorPages/403.html'),403

@app.errorhandler(405)
def method_not_allowed(error):
	return render_template('/ErrorPages/40X.html', number_err=405, label_err="Method Not Allowed", text_error="La ruta estipulada no tolera el método solicitado."),405

@app.errorhandler(410)
def file_gone(error):
	return jsonify({'ok':'False','error': 'Gone, the file you search now have gone', 'description':'Error 410'}), 410

@app.errorhandler(500)
def intServErr(error):
	return render_template('./ErrorPages/500.html',errorInfo=error),500

@app.route(PREFIX_APP)
def hello_start():
    return jsonify(ok=True, status_code=200, description="Deployed :P")

'''
----------------------------------------------------------------------------
Fin ERROR PAGES
----------------------------------------------------------------------------
'''


'''
----------------------------------------------------------------------------
----------------------------------------------------------------------------
PDS
----------------------------------------------------------------------------
----------------------------------------------------------------------------
'''



@app.route(PREFIX_APP+'/recoverPassword/<app>/<idRowDB>', methods=['GET'])
def recoverPassword(app, idRowDB):
	bd = Bd('pdstelmexprod', hostname='localhost', username='adminNoDrop', password='Trun0k2SAg')
	apps = { '1': 'PDS - Telmex', '2':'SGS - Telmex', '3':'Club de golf Cuernavaca TMX' }
	nombres = {'1':'Desarrollo de soluciones', '2':'Sistema de Gestión Sustentable', '3':'Club de golf Cuernanaca'}

	parametros = {
		'app' : apps[app],
		'nombre' : nombres[app],
	}

	a = bd.doQuery("SELECT status, idUser, expire FROM recoverPassTemp WHERE accountToChange ='{}';".format(idRowDB))

	if len(a)>0:
		if a[0][2] >= datetime.datetime.now():
			user = bd.doQuery("SELECT field_7, field_9 FROM app_entity_1 WHERE id = {};".format(a[0][1]))
			parametros['details'] = {'username':user[0][0], 'email':user[0][1], 'expired':False}
		else:
			parametros['details']={'expired':True}
	
	if len(a) <= 0:
		parametros['details'] = None
		return render_template('./pds/recoverPassLayout.html', params=parametros)
	else:
		return render_template('./pds/recoverPassLayout.html', params=parametros)

'''
----------------------------------------------------------------------------
----------------------------------------------------------------------------
Tracking campaigns Claro video
----------------------------------------------------------------------------
----------------------------------------------------------------------------
'''

@app.route(PREFIX_APP+'/get-analytics-data', methods=['POST','GET'])
def reporte_entradas_mes_ppt():
	pass
    return jsonify( ok=True, description="Endpoint enabled" )

'''
----------------------------------------------------------------------------
----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------
----------------------------------------------------------------------------
'''
if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
