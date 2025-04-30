Generador de Perfiles
Esta herramienta nos permite generar los perfiles de los miembros del equipo para nuestra web a partir de un CSV. Es bastante útil cuando hay que actualizar muchos perfiles y no queremos hacerlo manualmente.
Lo que necesitas

Python 3.6 o más nuevo
La librería requests (podés instalarla con pip install requests)

Cómo está organizado
El código asume que estás usando esta estructura de carpetas:
rsg-argentina/
├── content/
│   └── authors/  (Acá se crean los perfiles)
└── scripts/
    └── author-seeding/
        ├── author_profile_generator.py  (Este script)
        └── authorslist.csv  (CSV con la info de los miembros)
Cómo usarlo
Uso básico
bashpython author_profile_generator.py
Con esto, el script descarga las fotos de perfil y crea los nuevos perfiles sin borrar los que ya existen.
Opciones
Tenemos dos opciones disponibles:

-noimg: Usa avatares genéricos en vez de descargar las fotos. Útil para probar rápido si todo funciona bien.
bashpython author_profile_generator.py -noimg

-dump: Borra todos los perfiles existentes antes de crear los nuevos. Útil cuando queremos hacer una limpieza general.
bashpython author_profile_generator.py -dump


También podés combinar las opciones:
bashpython author_profile_generator.py -noimg -dump
Cómo funciona la asignación de roles
El script asigna automáticamente "pesos" y grupos según el cargo que tiene cada persona:
Pesos (weight)

Peso 30: Para los cargos directivos (Presidente, Vicepresidente, Secretario, Tesorero, Asesor Científico, Asesor de Facultad)
Peso 10: Para los Asesores Académicos
Peso 0: Para todos los demás (incluyendo Voluntarios)

Esto afecta el orden en que aparecen en la web.
Grupos (user_groups)

"Authorities": Para los cargos directivos
"Academic Advisors": Para los asesores académicos
"Volunteers": Para todos los demás

Posibles problemas
Hay algunos problemas comunes que pueden surgir:

Datos incompletos:

Si falta el nombre de alguien, el script lo va a saltear
Los asesores academicos no estan incluidos en el spreadsheet por lo que el script los borrara.
Si faltan intereses, educación u otros datos, esos campos quedan vacíos


Problemas con las imágenes:

Las fotos de Google Drive a veces tienen URLs raras o estan mal formateadas (invertidas o descentradas).
Si no puede descargar una imagen, usa un avatar genérico
Si hay muchos problemas con las imágenes, usá la opción -noimg


Datos desordenados:

El script hace lo que puede para interpretar los intereses y links, pero si están mal formateados en el CSV, pueden salir mal.
A los links se les asigna un ícono según el dominio (LinkedIn, GitHub, etc.) pero puede que esten faltando algunos.
Los intereses se separan por comas, así que asegurate de que estén bien en el CSV



Mantenimiento
Si necesitás hacer cambios:

Cambios chicos: Editá directamente los archivos _index.md en la carpeta content/authors/
Cambios grandes: Actualizá el CSV y volvé a correr el script

Formato del CSV
El CSV tiene que tener estas columnas:

"Nombre/s y Apellido/s": El nombre completo
"Foto personal": URL de la foto de perfil
"E-mail": Email de contacto
"About me (en inglés)": Bio en inglés
"Lista de intereses en bioinformática (en inglés)": Intereses separados por comas
"Cargo que ocupa": Rol en la organización
"Afiliación (Laboratorio, Instituto/ Universidad) - Incluir links": Afiliaciones
"Link de Linkedin, github, twitter, ID, Google Scholar, otro": Links a redes
"Título/Carrera": Info sobre estudios