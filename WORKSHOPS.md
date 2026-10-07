# Guía rápida para mantener workshops

Este archivo existe para que cualquiera pueda actualizar la página de workshops sin saber Hugo.

## Qué se edita

La lista de trayectos y cursos vive en `data/workshops.yaml`.

Cada curso vive dentro de `content/workshops/<curso>/`.

Si el curso va a tener varias ediciones, la carpeta del curso usa `_index.md`.

Si el curso tiene una sola edición, puede seguir usando `index.md` como antes.

Cada edición vive dentro del mismo curso, en `content/workshops/<curso>/<edicion>/index.md`.

## Cómo agregar un curso nuevo

1. Creá la carpeta del curso en `content/workshops/`, por ejemplo `content/workshops/mi_curso/`.
2. Si el curso va a tener ediciones, usá `content/workshops/mi_curso/_index.md`. Si no, usá `index.md`.
3. Poné el contenido del curso como ya se hace hoy.
4. Agregá el slug del curso en el trayecto correcto dentro de `data/workshops.yaml`.
5. Si querés que aparezca con imagen, agregá `featured.png` o `img.png` dentro de la carpeta del curso.

## Cómo agregar una nueva edición

1. Creá una carpeta dentro del curso, por ejemplo `content/workshops/introduccion_a_bash/2026/index.md`.
2. Copiá el contenido de una edición anterior o escribí el nuevo contenido.
3. En el front matter, asegurate de tener:
   - `course: "introduccion_a_bash"`
   - `layout: workshop_edition`
   - `year: 2026`
   - `title: "..."` con el nombre visible de la edición
4. Agregá esa edición dentro del bloque `editions` del curso correspondiente en `data/workshops.yaml`.
5. Dejá las ediciones ordenadas como quieras verlas en la web. La primera de la lista es la que se usa como entrada principal del curso.

## Cómo mover un curso de trayecto

1. Abrí `data/workshops.yaml`.
2. Buscá el curso en la lista del trayecto actual.
3. Cortalo y pegalo en el trayecto nuevo.

## Cómo dejar un curso en Otros

Si borrás el curso de `data/workshops.yaml`, la página lo va a mostrar en **Otros** automáticamente.

## Cómo cambiar el nombre de un trayecto

Editá el campo `title` del trayecto en `data/workshops.yaml`.

## Reglas simples

- El `slug` del curso es el nombre de la carpeta.
- El orden de los trayectos se controla moviendo los bloques en `data/workshops.yaml`.
- El orden de las ediciones se controla ordenando la lista `editions` dentro de cada curso en `data/workshops.yaml`.
- La página principal de workshops muestra cada curso una sola vez.
- Si un curso tiene ediciones, el click de la card va a la primera edición de su lista.
- Las ediciones no aparecen como cards separadas en la vista principal.

## Si algo no aparece

- Revisá que la carpeta exista en `content/workshops/`.
- Revisá que el slug esté escrito igual en `data/workshops.yaml`.
- Si el curso no está asignado, va a salir en **Otros**.
