# Portfolio Analisis

Aplicación para administrar mi portfolio de proyectos de análisis de datos desde una interfaz en Streamlit. El proyecto permite cargar, modificar y eliminar proyectos en una base SQLite, generar una web estática con esos datos y sincronizarla con GitHub Pages.

## Qué hace este proyecto

- Gestiona proyectos desde un panel de administración hecho con Streamlit.
- Guarda los proyectos en SQLite en `data/proyectos.db`.
- Usa Google Sheets como origen de credenciales para el login.
- Genera el sitio estático del portfolio a partir de la base de datos usando Jinja2.
- Sincroniza los cambios a GitHub con GitPython.
- Guarda imágenes y videos de los proyectos dentro de `assets/`.

## Arquitectura general

El flujo principal del proyecto es este:

1. El usuario entra al panel de administración en `app.py`.
2. La app valida usuario y contraseña contra una hoja de Google Sheets.
3. Desde el panel se pueden crear, editar o eliminar proyectos en SQLite.
4. Al pulsar `Analizar Cambios`, se regenera `index.html` con los datos actuales.
5. Al pulsar `Sincronizar Portfolio`, se hace commit, pull con rebase y push al remoto de GitHub Pages.

## Stack utilizado

- Python 3.8+
- Streamlit
- SQLite
- Pandas
- Jinja2
- GitPython
- HTML + CSS para el sitio estático generado

## Estructura del repositorio

```text
portfolio_analisis/
├── app.py
├── crear_db.py
├── credenciales.json
├── encrypt_db.py
├── index.html
├── style.css
├── requirements.txt
├── pyproject.toml
├── setup.cfg
├── assets/
├── data/
│   └── proyectos.db
└── function/
    ├── data_google_sheets.py
    ├── eliminar_proyecto.py
    ├── generar_web.py
    ├── login.py
    ├── mantenimiento.py
    ├── modificar_proyecto.py
    ├── path.py
    ├── subir_portfolio.py
    └── subir_proyectos.py
```

## Archivos principales

### `app.py`

Es el punto de entrada de la aplicación. Hace estas tareas:

- Abre la base SQLite.
- Carga los proyectos en un `DataFrame`.
- Muestra el login si no hay sesión autenticada.
- Presenta tres herramientas en la barra lateral: Nuevo Proyecto, Modificar Proyecto y Eliminar Proyecto.
- Permite regenerar la web.
- Permite sincronizar el portfolio con GitHub.

### `function/subir_proyectos.py`

Inserta un nuevo proyecto en la tabla `proyectos` y copia el archivo multimedia a `assets/`.

Validaciones actuales:

- Todos los campos son obligatorios.
- La cantidad de tecnologías debe ser un entero.
- El archivo multimedia no puede superar 95 MB.
- La URL del repositorio debe empezar por `https://github.com/maxicoceres-data/`.

### `function/modificar_proyecto.py`

Actualiza una columna de un proyecto existente por ID.

### `function/eliminar_proyecto.py`

Elimina un proyecto por ID desde SQLite.

### `function/generar_web.py`

Lee todos los proyectos de la base de datos, transforma el campo `tecnologia` en etiquetas y renderiza `index.html` con una plantilla Jinja2 embebida en el propio archivo.

Comportamiento relevante:

- Si el asset termina en `.mp4`, lo inserta como video.
- Si el asset existe y no es video, lo inserta como imagen.
- Si no hay asset, muestra un bloque de respaldo.

### `function/subir_portfolio.py`

Sincroniza el repositorio local con GitHub.

Hace lo siguiente:

- Lee `GITHUB_TOKEN` desde `st.secrets`.
- Configura el remoto `origin` con autenticación por token.
- Hace `git add -A` si detecta cambios.
- Bloquea la subida si hay archivos mayores a 100 MB trackeados por Git.
- Crea un commit automático.
- Hace `pull --rebase --autostash`.
- Hace push explícito de la rama actual.

### `function/data_google_sheets.py`

Lee usuario y contraseña desde una hoja de cálculo de Google llamada `Datos portfolio` usando un service account cargado desde `st.secrets`.

### `function/login.py`

Valida las credenciales ingresadas y habilita la sesión en Streamlit.

### `function/path.py`

Centraliza la ruta absoluta a `data/proyectos.db`.

### `crear_db.py`

Crea la tabla `proyectos` si no existe.

### `encrypt_db.py`

Genera una versión cifrada de la base de datos usando Fernet y la variable de entorno `FERNET`.

### `function/mantenimiento.py`

Script auxiliar de mantenimiento por consola para modificar o eliminar proyectos directamente en SQLite. No forma parte del flujo principal de la app web.

### `credenciales.json`

Existe en el repositorio local, pero el flujo activo del proyecto lee las credenciales de Google Sheets desde `st.secrets`. Si mantienes este archivo, conviene tratarlo como material sensible y no depender de él como mecanismo principal.

## Base de datos

La tabla principal es `proyectos` y su esquema actual es:

```sql
CREATE TABLE IF NOT EXISTS proyectos(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		titulo TEXT,
		tecnologia TEXT,
		descripcion TEXT,
		url TEXT,
		github TEXT
)
```

### Significado de las columnas

- `id`: identificador autoincremental.
- `titulo`: nombre visible del proyecto.
- `tecnologia`: lista de tecnologías separadas por comas.
- `descripcion`: texto descriptivo del proyecto.
- `url`: nombre del archivo multimedia guardado en `assets/`.
- `github`: enlace al repositorio del proyecto.

## Assets y salida web

### `assets/`

Contiene los recursos estáticos del portfolio, por ejemplo:

- imágenes de proyectos
- videos de demostración
- PDF del CV
- logos y otros recursos visuales

### `index.html`

Es la salida generada del portfolio público. El archivo actual se regenera desde la base de datos al ejecutar la acción `Analizar Cambios` o llamando a `generar_web()`.

### `style.css`

Define la estética de la página pública: hero principal, tarjetas de proyectos, etiquetas de tecnología, botones de contacto y pie de página.

## Requisitos para ejecutar el proyecto

- Python 3.8 o superior
- Un entorno virtual recomendado
- Acceso a una hoja de Google Sheets con las credenciales de login
- Un token de GitHub con permisos para subir al repositorio del portfolio
- Dependencias de Python instaladas

## Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repo>
cd portfolio_analisis
```

### 2. Crear y activar un entorno virtual

En Windows con PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Además de lo que ya esté en `requirements.txt`, el código actual usa estas librerías:

- `streamlit`
- `pandas`
- `jinja2`
- `gitpython`

Si tu entorno no las tiene instaladas, agrégalas manualmente:

```bash
pip install streamlit pandas jinja2 gitpython
```

## Configuración de secretos

El proyecto usa `st.secrets`, por lo que necesitas un archivo `.streamlit/secrets.toml` con al menos estas claves:

```toml
GITHUB_TOKEN = "tu_token_de_github"

[GOOGLE_SHEETS]
type = "service_account"
project_id = "tu_project_id"
private_key_id = "tu_private_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "tu_service_account@proyecto.iam.gserviceaccount.com"
client_id = "tu_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

## Ejecución local

Para levantar el panel de administración:

```bash
streamlit run app.py
```

## Flujo de uso dentro de la app

### Login

- La pantalla inicial pide usuario y contraseña.
- Los datos válidos se leen desde Google Sheets.

### Nuevo Proyecto

Permite cargar:

- título
- cantidad de tecnologías
- tecnologías separadas por coma
- descripción
- imagen o video (`png` o `mp4`)
- URL del repositorio GitHub

### Modificar Proyecto

- Muestra el contenido de la base en un `DataFrame`.
- Permite elegir la columna a modificar.
- Actualiza el registro por ID.

### Eliminar Proyecto

- Muestra el contenido actual de la tabla.
- Elimina un proyecto por ID tras confirmación.

### Analizar Cambios

- Regenera `index.html` a partir de la base SQLite.

### Sincronizar Portfolio

- Sincroniza el repositorio con GitHub usando el token configurado.

## Scripts auxiliares

### Crear base de datos

```bash
python crear_db.py
```

### Generar la web de forma directa

```bash
python function/generar_web.py
```

### Cifrar la base de datos

En Git Bash:

```bash
export FERNET="tu_clave_fernet"
python encrypt_db.py
```

En Windows PowerShell:

```powershell
$env:FERNET="tu_clave_fernet"
python encrypt_db.py
```

## Consideraciones actuales del proyecto

- `requirements.txt` hoy no refleja todas las librerías que usa el código.
- El login depende de la disponibilidad de Google Sheets y de las credenciales del service account.
- La sincronización con GitHub depende de que el remoto y el token tengan permisos válidos.
- El límite práctico de subida de assets está controlado para evitar archivos incompatibles con GitHub.
- La web pública se genera desde una plantilla inline dentro de `function/generar_web.py`, no desde un archivo separado de plantilla.

## Posibles mejoras futuras

- Consolidar todas las dependencias en `requirements.txt` o `pyproject.toml`.
- Separar la plantilla HTML de `generar_web.py` a un archivo dedicado.
- Añadir validaciones más estrictas sobre extensiones, nombres de archivo y columnas editables.
- Incorporar tests para la lógica de base de datos y generación de HTML.
- Añadir una migración o bootstrap más limpio para la base de datos inicial.

## Autor

Maximiliano Cóceres
