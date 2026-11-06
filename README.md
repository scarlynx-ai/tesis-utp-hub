# Portal de Propuestas de Tesis — UTP

Repositorio y plataforma de evaluación de propuestas de investigación para la Titulación Profesional en Ingeniería de Sistemas (Universidad Tecnológica del Perú).

Permite la revisión estructurada, filtrado por líneas de investigación y exportación de 20 propuestas de tesis con control de acceso institucional.

---

## Características

- **Catálogo de Propuestas**: 20 temas de investigación orientados a Inteligencia Artificial, Visión Computacional, IoT, Seguridad y Desarrollo Multiplataforma.
- **Acceso Restringido**: Pantalla de autenticación por DNI para salvaguardar la autoría y los derechos intelectuales del proyecto.
- **Exportación Automatizada**: Scripts de generación en Python para compilar resúmenes ejecutivos en formatos PDF y Microsoft Word (`.docx`).
- **Historial de Versiones**: Seguimiento cronológico de modificaciones y entregables según el calendario académico institucional.

---

## Estructura del Repositorio

```text
tesis_web_utp/
├── index.html            # Portal web interactivo con catálogo y buscador dinámico
├── generador_web.py      # Script para compilar y actualizar la base de datos de propuestas
├── historial.json        # Registro de revisiones y cambios por fecha
└── descargas/            # Documentos PDF y DOCX listos para revisión docente
```

---

## Ejecución Local

Para visualizar el portal en local:

```bash
# Iniciar servidor estático ligero
python -m http.server 3000
```

Visita `http://localhost:3000` en tu navegador.

---

## Autor

Desarrollado por **Scarlynx** para el proceso de Titulación Profesional UTP.
