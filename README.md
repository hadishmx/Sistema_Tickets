la instalacion del proyecto consiste en dos partes, backend y frontend.

prerequisitos:

tener instalado xampp (opcional).

tener instalado node.js y path incluido.


  Backend:

1.- Desde Terminal dirigirse a la carpeta backend y ejecutar el codigo.
	
 	pip install -r requirements.txt

2.-(opcional) en la carpeta backend/backend/settings.py ajustar conexion con mysql segun sus preferencias.

	DATABASES = {  
	    'default': {  
	        'ENGINE': '',  
	        'NAME': '',  
	        'USER': '',  
	        'PASSWORD': '',  
	        'HOST': '',  
	        'PORT': '',  
	    }  
	}
 
 !!! en caso de no utilizar el codigo, eliminar el codigo dentro del archivo. !!!

3.- Crear super usuario.

	py manage.py createsuperuser

4.- Iniciar servidor local.

	py manage.py runserver

  Frontend:

1.- Desde 2da terminal dirigirse a fronend e installar los paquetes.

	npm install
 
descargará e instalará los paquete requeridos al igual que el requirements.txt

2.-Iniciar el servidor local.

	npm run dev


Proyecto esta sujeto a cambios en cuanto instalacion.
 


