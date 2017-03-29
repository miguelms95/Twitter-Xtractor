# -*- coding: utf-8 -*-
''' Developed by Miguel Martinez Serrano www.miguelms.es'''
import requests
import urllib
import os
from BeautifulSoup import BeautifulSoup

DESCARGAR_FOTOS = 1     # 1 para descargar las fotos # 0 para no descargarlas
DIR = 'export_imgs'     #Directorio para guardar imagenes exportadas
aliasUser = ''

def intro():
    cadena = '*** Bienvenido a Twitter XTRACTOR *** '
    cadena +='Desarrollado por @miguelms_es *** www.miguelms.es\n\n'
    cadena +='Introduce una URL de perfil de twitter o un nombre de usuario.\n'
    cadena +='Formatos de ejemplo: @miguelms_es, miguelms_es,  http://twitter.com/miguelms_es\n'
    return cadena

def extraerImagenPerfil(url_usuario):
    page = requests.get(url_usuario)
    if(page.status_code == 200):    # check conexion
        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        url_img_perfil = html.find('img',{'class':'ProfileAvatar-image '}).get('src')
        print 'Foto de perfil: ' + extraerRutaImagenAltaCalidad(url_img_perfil)
        return extraerRutaImagenAltaCalidad(url_img_perfil)
    else:
        print '### ERROR: ' + str(page.status_code) + ' página no encontada'

def extraerImagenPortada(url_usuario):
    page = requests.get(url_usuario)
    if(page.status_code == 200):
        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        #print html
        url_imagenPortada = html.find('div',{'class':'ProfileCanopy-headerBg'}).find('img').get('src')
        if(url_imagenPortada != None):
            print 'Foto de portada: ' + url_imagenPortada+'\n'
            return url_imagenPortada
        return None
    else:
        print '### ERROR: '+str(page.status_code)+' página no encontada'

def extraerRutaImagenAltaCalidad(url):
    # https://pbs.twimg.com/profile_images/839721704163155970/LI_TRk1z_400x400.jpg
    urlImagen = url.split('/')
    #print urlImagen
    formatoImg = urlImagen[5]
    #print formatoImg
    formatoImg = formatoImg.split('.')
    formatoImg = formatoImg[1] # aqui tengo 'jpg' o 'png'
    urlFinal = urlImagen[0] + '//' + urlImagen[2]+'/' + urlImagen[3]+'/' + urlImagen[4]+'/'+splitPartImgenSrc(urlImagen[5])+'.'+formatoImg
    return urlFinal

def splitPartImgenSrc(url):
    url = url.split('x')
    tamFoto = len(url[1].split('.')[0])
    tamFoto +=1 # para eliminar tambien la "_" de la ruta de la imagen
    return url[0][:-tamFoto]


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
    if ('twitter.com') not in url:  # En este caso ha introducido el nombre de un usuario
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
        srcPortada = extraerImagenPortada(url)

        if(DESCARGAR_FOTOS):
            if(srcPerfil != None):
                descargarImagen(srcPerfil,'perfil')
            else:
                print 'No tiene foto de perfil\n'
            if(srcPortada != None):
                descargarImagen(srcPortada,'portada')
            else:
                print 'No tiene foto de portada\n'

def descargarImagen(src,cad):
    resource = urllib.urlopen(src)
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    output = open(DIR+'/'+aliasUser+'_'+cad+'.jpg', 'wb')
    output.write(resource.read())
    output.close()
    print 'Descargando foto de ' + cad

# PENDIENTE
def getFormato(src):
    src = src.split('.')
    return src[3]

def getInfoPerfil(url):
    cadena = ''
    page = requests.get(url)
    if (page.status_code == 200):
        html = BeautifulSoup(page.content.decode('utf-8', 'ignore'))
        nombreUsuario = html.find('h1', {'class': 'ProfileHeaderCard-name'}).find('a').contents[0]
        shortUser = html.find('b', {'class': 'u-linkComplex-target'}).string
        global aliasUser
        aliasUser = shortUser
        descriptionUser = html.find('p', {'class': 'ProfileHeaderCard-bio u-dir'}).string
        if(descriptionUser == None):
            descriptionUser = ''
        fechaRegistro = html.find('span', {'class': 'ProfileHeaderCard-joinDateText js-tooltip u-dir'}).string
        lugar = html.find('span', {'class': 'ProfileHeaderCard-locationText u-dir'}).string
        cadena += '=== ' +nombreUsuario +' (@'+shortUser+') ===\n'
        cadena += descriptionUser+'\n'
        cadena += fechaRegistro+'\n'
        cadena += lugar.replace(' ','').replace('\n','')+'\n'   # las fechas tienen muchos espacios y un salto de linea O_o

        return cadena
print intro()

#extraerFotos('http://twitter.com/google')

while 1:
    data_user = raw_input('Obtener info de perfil -> ')
    if(data_user=="exit"):
        exit(0)
    extraerFotos(data_user)

