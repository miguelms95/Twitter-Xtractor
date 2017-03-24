# -*- coding: utf-8 -*-
''' Developed by Miguel Martinez Serrano www.miguelms.es'''
import requests
import StringIO
from BeautifulSoup import BeautifulSoup

DESCARGAR_FOTOS = 0    # 1 para descargar las fotos # 0 para no descargarlas

def intro():
    cadena = '*** Bienvenido a Twitter XTRACTOR ***\n'
    cadena +='Introduce una URL de perfil de twitter o un nombre de usuario.\n'
    cadena +='Formatos de ejemplo: @miguelms_es, miguelms_es,  http://twitter.com/miguelms_es\n'
    return cadena

def extraerImagenPerfil(url_usuario):
    page = requests.get(url_usuario)
    if(page.status_code == 200):

        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        #print html
        url_img_perfil = html.find('img',{'class':'ProfileAvatar-image '}).get('src')
        print 'Foto de perfil: ' + extraerRutaImagenAltaCalidad(url_img_perfil)
    else:
        print '### ERROR: ' + str(page.status_code) + ' página no encontada'

def extraerImagenPortada(url_usuario):
    page = requests.get(url_usuario)
    if(page.status_code == 200):
        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        #print html
        url_img_perfil = html.find('div',{'class':'ProfileCanopy-headerBg'}).find('img').get('src')
        print 'Foto de portada: ' + url_img_perfil
    else:
        print '### ERROR: '+str(page.status_code)+' página no encontada'

def extraerRutaImagenAltaCalidad(url):
    urlImagen = url.split('_')
    formatoImg = urlImagen[2]
    formatoImg = formatoImg.split('.')
    formatoImg = formatoImg[1] # aqui tengo 'jpg' o 'png'
    urlFinal = urlImagen[0] + '_' + urlImagen[1]+'.'+formatoImg
    return urlFinal

def limpiar_url(url):
    url = url.replace(" ","")
    if ('http' or 'https') not in url:
        while(url[0]=='@'):
            url = url[1:]
        if(checkTwitterURL(url)<0):
            return -1
        url = 'https://twitter.com/'+url
    else:
        if (checkTwitterURL(url) < 0):
            return -2
    return url

def checkTwitterURL(url):
    if ('twitter.com') not in url:  # en este caso ha introducido un usuario directamente
        return 1
    else:
        if (len(url) < 12):  # como minimo introduce twitter.com/
            print 'introduce un nombre de usuario tras la url de twitter. Ejemplo: twitter.com/google'
            return -2
        return 1 # todo correcto

def extraerFotos(url):
    url = limpiar_url(url)
    if(url <0):
        print '## ERROR en la URL introducida ##'
    else:
        print getInfoPerfil(url)
        srcPerfil = extraerImagenPerfil(url)
        srcPortada =extraerImagenPortada(url)
        if(DESCARGAR_FOTOS):
            descargarImagen(srcPerfil)
            descargarImagen(srcPortada)

def descargarImagen(src):
    print 'Descargando'

def getInfoPerfil(url):
    cadena = ''
    page = requests.get(url)
    if (page.status_code == 200):
        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        nombreUsuario = html.find('h1', {'class': 'ProfileHeaderCard-name'}).find('a').contents[0]
        shortUser = html.find('b', {'class': 'u-linkComplex-target'}).string
        descriptionUser = html.find('p', {'class': 'ProfileHeaderCard-bio u-dir'}).string
        fechaRegistro = html.find('span', {'class': 'ProfileHeaderCard-joinDateText js-tooltip u-dir'}).string
        lugar = html.find('span', {'class': 'ProfileHeaderCard-locationText u-dir'}).string
        cadena += '=== ' +nombreUsuario +' (@'+shortUser+') ===\n'
        cadena += descriptionUser+'\n'
        cadena += fechaRegistro+'\n'
        cadena += lugar.replace(' ','').replace('\n','')+'\n'   # las fechas tienen muchos espacios y un salto de linea O_o

        return cadena
print intro()

# extraerFotos('http://twitter.com/miguelms_es')
while 1:
    data_user = raw_input('Obtener info de perfil -> ')
    extraerFotos(data_user)
