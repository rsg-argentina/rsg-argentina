# Introducción e instrucciones generales para poner/editar contenido en el sitio

## Qué es HUGO?

HUGO es un compilador para hacer páginas web estáticas a partir de archivos markdown, una serie de configs pre-establecidas, y un theme que hace todo más bonito. Para esta página estamos usando "Academic". Pueden encontrar la documentación completa de HUGO [acá](https://gohugo.io/documentation/).

## Qué es Academic?

Academic es un *theme* bastante popular que permite hacer páginas web de labos e institutos (o de personas), capturando bastante bien la escencia del mundo académico (publicacionees, charlas, etc). En este caso nos estamos yendo medio por la tangente (dado que no somos un instituto ni un lab), pero como van a ver, se adapta bastante bien. Pueden encontrar la documentación completa de Academic [acá](https://sourcethemes.com/academic/docs/)

## Cómo hago andar HUGO/Academic en mi compu?

Para hacer andar HUGO en sus compus (asumiendo que tienen algún sistema UNIX, como corresponde), van a tener que instalar Hugo-extended, clonar este repo y actualizar academic. Estos tres simples pasos serían algo como:

```Bash
	# Descargamos el deb de HUGO, versión 0.58.3 (que es la que usamos para el deploy) e instalamos
	wget https://github.com/gohugoio/hugo/releases/download/v0.58.3/hugo_extended_0.58.3_Linux-64bit.deb 	
	sudo dpkg -i hugo*_Linux-64bit.deb
	# Clonamos el repo de la web del rsg
	git clone https://github.com/rsg-argentina/rsg-argentina.git
	# Actualizamos Academic
	cd rsg-argentina
	git submodule update --init --recursive
```

> No es la única manera pero esta sé que funciona

## Cómo corro el sitio localmente?

Una vez que tenemos todo instalado, ya podemos hostear nuestra web del RSG. Para hacerlo:

```Bash
	# estando en el directorio del repo...
	hugo serve
```

Eso hará que hugo compile y les sirva el sitio en el algún puerto de su compu (`localhost:1313`, por ejemplo)


```Bash
	# Example output

					| EN  
	+------------------+----+
	Pages            | 63  
	Paginator pages  |  1  
	Non-page files   |  2  
	Static files     |  8  
	Processed images |  4  
	Aliases          |  8  
	Sitemaps         |  1  
	Cleaned          |  0  

	Total in 270 ms
	Watching for changes in /home/lioneluranl/git/rsg-argentina/{content,data,static,themes}
	Watching for config changes in /home/lioneluranl/git/rsg-argentina/config.toml, /home/lioneluranl/git/rsg-argentina/config/_default
	Environment: "development"
	Serving pages from memory
	Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
	Web Server is available at //localhost:1313/ (bind address 127.0.0.1)
	Press Ctrl+C to stop
```

Ahora pueden acceder desde el browser a esa dirección y ver el sitio a medida que lo cambian (si lo cambian)

## Los cambios que podemos/debemos hacer

HUGO/Academic permite que el desarrollo y deploy se haga en forma colaborativa, de modo que descentraliza la tarea de mantener la web actualizada. Esto es: cada cosa nueva que aportamos (una publicación, una charla, un post, una noticia, etc) puede ser actualizado por los autores de la cosa nueva en poco más de 10 mins (sin la necesidad de delegar esa tarea en alguien más que, de tener que hacer esa tarea por todos, necesitaría mucho más tiempo). 

**¿Qué cosas vamos a necesitar que cada uno agregue?**

- Su perfil 
- Sus publicaciones (relacionadas al proyecto, si las hubiera)
- Las meetings que haya organizado (o esté organizando)

Cualquier otro contenido que consideren apropiado y que sume al sitio

### ¿Cómo agrego mi perfil?

HUGO/Academic compila leyendo los usuarios de la carpeta `content/authors`. Cada usuario es una carpeta (por ejemplo `admin`) y, dentro de cada carpeta, el compilador entiende dos archivos: 
- _index.md
- avatar.[jpg|png]

El `_index.md` es un archivo markdown con información acerca del usuario, mientras que el avatar es una imagen del mismo. 

Para crear un nuevo usuario deberán generar una nueva carpeta, por ejemplo `lionel`, y dentro de ésta poner su foto (y llamarla avatar.jpg o avatar.png, según el caso), y un archivo `_index.md`. Este último admite una serie de key/values pre-configurados por academic. Por ejemplo, index de usuario dice algo como:

```T
+++
# Display name
name = "Lionel Urán Landaburu"

# Author weight -- for sort purposes
weight = 10

# Username (this should match the folder name)
authors = ["lionel"]

# Author name (this is required for people without content)
lionel = [""]

# Role/position
role = "Vice-President"

# Organizations/Affiliations
#   Separate multiple entries with a comma, using the form: `[ {name="Org1", url=""}, {name="Org2", url=""} ]`.
organizations = [ { name = "Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET)", url = "http://www.conicet.gob.ar" }, {name="Universidad de San Martín", url="http://www.unsam.edu.ar"} ]

# Short bio (displayed in user profile at end of posts)
bio = "PhD Fellow, teacher and science divulgation enthusiast."

# Enter email to display Gravatar (if Gravatar enabled in Config)
email = "lionel.u.l@iib.unsam.edu.ar"

# List (academic) interests or hobbies
interests = ["Chemogenomics, Neglected diseases, Drug Discovery"]

# Organizational groups that you belong to (for People widget)
#   Set this to `[]` or comment out if you are not using People widget.
user_groups = ["Authorities"]

# List qualifications (such as academic degrees)
[[education.courses]]
  course = "Ms in Biotechnology"
  institution = "Universidad Nacional de Quilmes"
  year = 2015


# Social/Academic Networking
# For available icons, see: https://sourcethemes.com/academic/docs/widgets/#icons
#   For an email link, use "fas" icon pack, "envelope" icon, and a link in the
#   form "mailto:your-email@example.com" or "#contact" for contact widget.

[[social]]
  icon = "envelope"
  icon_pack = "fas"
  link = "mailto:lionel.u.l@iib.unsam.edu.ar"

[[social]]
  icon = "twitter"
  icon_pack = "fab"
  link = "https://twitter.com/leitouran"

[[social]]
  icon = "google-scholar"
  icon_pack = "ai"
  link = "https://scholar.google.com/citations?user=fIjAs5UAAAAJ"

[[social]]
  icon = "linkedin"
  icon_pack = "fab"
  link = "https://www.linkedin.com/in/lionelul/"

[[social]]
  icon = "github"
  icon_pack = "fab"
  link = "https://github.com/leitouran"

[[social]]
  icon = "orcid"
  icon_pack = "ai"
  link = "https://orcid.org/0000-0002-6202-9779"

+++

# About me 

Lionel Uran Landaburu holds an MS degree in Biotechnology from the Universidad Nacional de Quilmes, Argentina. Is passionate about, and has been working on since 2011, global health problems. He has had welcoming experiences in the wet lab, but is now aiming towards Bioinformatics as a PhD fellow at IIBIO-CONICET. He is currently doing research in applied chemogenomics, using genome-wide data and chemical libraries to find novel treatments for a wide variety of neglected diseases, Chagas disease in particular.
```

Pueden usar esto como template. Hay más cosas para agregar (otras redes sociales, por ejemplo). Revisen la documentación completa de Academic si quieren agregar algo más. 

Una vez agregado esto, HUGO lo compila bien piola y ya están listos para agregar, commitear y pushear al repo. 


### ¿Cómo agrego una publicación?

El *modus operandi* es el mismo que para usuarios, con la salvedad de que esta vez agregaremos una carpeta dentro de `publications`. Pueden usar la que ya está creada como molde para las que sigan. También pueden agregar una imagen, nombrándola `featured.png` o `featured.jpg"` según el caso. 

### ¿Cómo agrego una meeting?

Igual que lo descrito arriba para publicaciones, pero esta vez creando el contenido nuevo dentro de la carpeta `talks`. También pueden usar el que ya está creado como molde. 