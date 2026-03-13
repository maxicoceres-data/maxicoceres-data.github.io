import sqlite3
from jinja2 import Template
from pathlib import Path


def generar_web():
    
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "data" / "proyectos.db"
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #permite acceder por nombre de columna
    cursor = conn.cursor()
    proyectos = cursor.execute("SELECT * FROM proyectos").fetchall()
    conn.close()
    
    
    plantilla_html = '''
    <!doctype html>
<html lang="es">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Portfolio Maximiliano Cóceres| Analista de Datos</title>
		<link rel="icon" type="image/x-icon" href="favicon.ico" />
		<link rel="stylesheet" href="style.css" />

		<link
			rel="stylesheet"
			href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
		/>
	</head>
	<body>
		<header>
			<h1>Hola, soy <span class="highlight">Maxi</span></h1>
			<p>Especialista en Análisis de Datos</p>
			<div class="tech-icons">
				<i class="fab fa-python fa-2x" title="Python"></i>
				<i class="fas fa-database fa-2x" title="SQL"></i>
				<i class="fas fa-chart-pie fa-2x" title="PowerBI"></i>
				<i class="fab fa-github fa-2x" title="GitHub"></i>
			</div>
			<div class="cta-container">
				<a
					href="https://wa.me/634624907?text=Hola!%20Vi%20tu%20portfolio%20de%20datos%20y%20me%20gustaría%20contactarte"
					class="btn-primary"
					target="_blank"
				>
					<i class="fab fa-whatsapp"></i> Contactar por WhatsApp
				</a>

				<a
					href="assets/CV_Maximiliano_Cóceres.pdf"
					class="btn-secondary"
					download
				>
					<i class="fas fa-file-pdf"></i> Descargar CV (PDF)
				</a>
			</div>
		</header>

		<div class="container">
			<h2 style="text-align: center; font-size: 2rem">
				Mis proyectos
			</h2>

        <div class="grid">
            {% for p in lista_proyectos %}
            <div class="card">
					{% for t in p.tecnologia %}
					<span class="tag">{{t}}</span>
					{% endfor %}
					{% if p.url.endswith(".mp4") %}
					<video autoplay loop muted playsinline class="card-video">
						<source
							src="/assets/{{p.url}}"
							type="video/mp4"
						/>
						Tu navegador no soporta videos.
					</video>
					{% else %}
					<img class="card-imagen" src="/assets/{{p.url}}">
					{% endif %}
					<h3>{{p.titulo}}</h3>
					<p>
						{{p.descripcion}}
					</p>
					<a
						href="{{p.github}}"
						class="btn"
						>Ver Repositorio →</a
					>
				</div>
    {% endfor %}
        </div>
   
        </div>
        
        		<footer>
			<p>
				¿Tienes un proyecto en mente? <br /><br />
				<a href="mailto:maximiliano.g.coceres@gmail.com"
					><i class="fas fa-envelope"></i> Email</a
				>
				<a href="https://www.linkedin.com/in/maximiliano-gabriel-coceres/"
					><i class="fab fa-linkedin"></i> LinkedIn</a
				>
				<a href="https://github.com/maximilianococeres-prog"
					><i class="fab fa-github"></i> GitHub</a
				>
			</p>
		</footer>
	</body>
</html>
    
    '''
    
    
    template = Template(plantilla_html)
    html_final = template.render(lista_proyectos = proyectos)
    
    with open(BASE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html_final)
        
    print(f"🚀 Web generada con {len(proyectos)} proyectos.")
    
if __name__ == "__main__":
    generar_web()