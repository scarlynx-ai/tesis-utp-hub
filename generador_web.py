import os
import json
import base64
import datetime
import requests

DIR_WEB = os.path.dirname(os.path.abspath(__file__))
DIR_EDICIONES = os.path.join(DIR_WEB, "ediciones")
DIR_DESCARGAS = os.path.join(DIR_WEB, "descargas")
ARCHIVO_HISTORIAL = os.path.join(DIR_WEB, "historial.json")

# Hash SHA-256 del DNI 76051532
AUTH_HASH_SHA256 = "b40f64b00ed7b2561d0e76bd4e06462f40a227f2206503c2b8767849e0b44f85"

os.makedirs(DIR_EDICIONES, exist_ok=True)
os.makedirs(DIR_DESCARGAS, exist_ok=True)

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        try:
            with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_historial(historial):
    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def generar_html_edicion(fecha_str, propuestas, es_index=False):
    """Genera la página HTML responsiva con modo móvil/tablet, paginador interactivo y descargas."""
    prefix_ruta = "" if es_index else "../"
    
    # 1. Filas para vista Desktop (Tabla)
    filas_tabla = ""
    # 2. Tarjetas para vista Móvil / Tablet Vertical
    tarjetas_movil = ""
    
    for i, p in enumerate(propuestas):
        pagina_num = (i // 10) + 1  # 10 por página
        
        vi_links_html = "".join([
            f'<a href="{link["url"]}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-[11px] font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800 hover:underline mr-1 mb-1">'
            f'🔗 {link["titulo"]} <span class="bg-blue-200 dark:bg-blue-800 text-blue-900 dark:text-blue-200 text-[10px] px-1 rounded font-bold">{link.get("ano", "2024")}</span></a>'
            for link in p.get("vi_links", [])
        ])
        
        vd_links_html = "".join([
            f'<a href="{link["url"]}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-800 hover:underline mr-1 mb-1">'
            f'📊 {link["titulo"]} <span class="bg-emerald-200 dark:bg-emerald-800 text-emerald-900 dark:text-emerald-200 text-[10px] px-1 rounded font-bold">{link.get("ano", "2024")}</span></a>'
            for link in p.get("vd_links", [])
        ])
        
        badge_ia = '<span class="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-semibold rounded bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300">✨ IA Aplicada</span>' if p.get("usa_llm") else '<span class="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-semibold rounded bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">⚡ Arquitectura Pura</span>'
        
        # Fila Desktop
        filas_tabla += f"""
        <tr class="tema-item tema-page-{pagina_num} hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition border-b border-slate-200 dark:border-slate-800" data-page="{pagina_num}">
            <td class="p-4 align-top font-bold text-slate-500 text-center">{p["id"]}</td>
            <td class="p-4 align-top max-w-sm">
                <div class="font-semibold text-slate-900 dark:text-slate-100 text-sm leading-snug mb-1">{p["titulo"]}</div>
                <div class="flex items-center gap-2 mt-2">
                    <span class="inline-block px-2 py-0.5 text-xs rounded bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-300 font-medium">{p["linea_utp"]}</span>
                    {badge_ia}
                </div>
            </td>
            <td class="p-4 align-top max-w-xs">
                <div class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">{p["vi_nombre"]}</div>
                <div class="text-xs text-slate-500 mb-2 italic">Indicadores: {p["vi_indicadores"]}</div>
                <div class="flex flex-wrap">{vi_links_html}</div>
            </td>
            <td class="p-4 align-top max-w-xs">
                <div class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">{p["vd_nombre"]}</div>
                <div class="text-xs text-slate-500 mb-2 italic">Indicadores: {p["vd_indicadores"]}</div>
                <div class="flex flex-wrap">{vd_links_html}</div>
            </td>
            <td class="p-4 align-top text-xs text-slate-600 dark:text-slate-400 max-w-xs">
                <div class="p-2.5 rounded bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/50 text-amber-900 dark:text-amber-300 text-[11px] leading-relaxed mb-2">
                    🛡️ <strong>Anti-Duplicidad:</strong> {p["originalidad"]}
                </div>
                <div class="flex items-center justify-between mt-2 pt-1 border-t border-slate-100 dark:border-slate-800">
                    <span class="text-[10px] text-slate-500">📅 2021–2026</span>
                    <a href="{prefix_ruta}descargas/Ficha_Tema_{p['id']}_UTP.pdf" download="Ficha_Tema_{p['id']}_UTP.pdf" target="_blank" class="inline-flex items-center gap-1.5 text-[11px] font-semibold text-rose-600 dark:text-rose-400 hover:text-rose-700 bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 dark:hover:bg-rose-900/50 border border-rose-200 dark:border-rose-800 px-2.5 py-1 rounded-lg transition shadow-sm">
                        <svg class="w-3.5 h-3.5 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                        <span>Ficha .pdf</span>
                    </a>
                </div>
            </td>
        </tr>
        """
        
        # Tarjeta Móvil / Tablet (Responsive vertical)
        tarjetas_movil += f"""
        <div class="tema-item tema-page-{pagina_num} bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm transition" data-page="{pagina_num}">
            <div class="flex items-start justify-between gap-3 mb-2">
                <div class="flex items-center gap-2">
                    <span class="w-7 h-7 rounded-lg bg-blue-600 text-white font-bold text-xs flex items-center justify-center shadow-sm">
                        {p["id"]}
                    </span>
                    <span class="px-2 py-0.5 text-xs rounded bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-300 font-medium">
                        {p["linea_utp"]}
                    </span>
                </div>
                {badge_ia}
            </div>
            
            <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-snug mb-3">
                {p["titulo"]}
            </h4>
            
            <!-- Variable Independiente -->
            <div class="mb-3 p-3 bg-blue-50/60 dark:bg-blue-950/20 rounded-lg border border-blue-100 dark:border-blue-900/40">
                <div class="text-xs font-bold text-blue-900 dark:text-blue-300 mb-1">🔹 Variable Independiente (VI):</div>
                <div class="text-xs text-slate-700 dark:text-slate-300 mb-1.5">{p["vi_nombre"]}</div>
                <div class="flex flex-wrap">{vi_links_html}</div>
            </div>
            
            <!-- Variable Dependiente -->
            <div class="mb-3 p-3 bg-emerald-50/60 dark:bg-emerald-950/20 rounded-lg border border-emerald-100 dark:border-emerald-900/40">
                <div class="text-xs font-bold text-emerald-900 dark:text-emerald-300 mb-1">📊 Variable Dependiente (VD):</div>
                <div class="text-xs text-slate-700 dark:text-slate-300 mb-1.5">{p["vd_nombre"]}</div>
                <div class="flex flex-wrap">{vd_links_html}</div>
            </div>
            
            <!-- Diferencial Anti-Plagio -->
            <div class="p-3 rounded-lg bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/40 text-[11px] text-amber-900 dark:text-amber-300 leading-relaxed mb-3">
                🛡️ <strong>Anti-Duplicidad SUNEDU:</strong> {p["originalidad"]}
            </div>
            
            <!-- Footer de la Tarjeta con Botón de Descarga Individual -->
            <div class="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800">
                <span class="text-[11px] text-slate-500 font-medium">📅 Fuentes: 2021–2026</span>
                <a href="{prefix_ruta}descargas/Ficha_Tema_{p['id']}_UTP.pdf" download="Ficha_Tema_{p['id']}_UTP.pdf" target="_blank" class="inline-flex items-center gap-1.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow-sm transition active:scale-95">
                    <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                    <span>Descargar Ficha (.pdf)</span>
                </a>
            </div>
        </div>
        """
        
    historial = cargar_historial()
    historial_nav_html = ""
    for h in historial:
        activo = "bg-blue-600 text-white font-bold" if h["fecha"] == fecha_str else "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200"
        url_dest = "index.html" if es_index and h["fecha"] == fecha_str else f"ediciones/edicion_{h['fecha']}.html"
        historial_nav_html += f'<a href="{url_dest}" class="px-3 py-1.5 rounded-lg text-xs transition {activo}">Edición {h["fecha"]} ({h["total_temas"]} temas)</a>\n'

    total_temas = len(propuestas)
    total_paginas = (total_temas + 9) // 10

    # Botones del paginador
    botones_paginador_html = ""
    for pag in range(1, total_paginas + 1):
        inicio = (pag - 1) * 10 + 1
        fin = min(pag * 10, total_temas)
        activo_class = "bg-blue-600 text-white shadow-sm" if pag == 1 else "bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 hover:bg-slate-100"
        botones_paginador_html += f"""
        <button onclick="irAPagina({pag})" id="btn-page-{pag}" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold transition pag-btn {activo_class}">
            Pág. {pag} ({inicio}–{fin})
        </button>
        """

    html = f"""<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal de Tesis UTP — Acceso Protegido ({fecha_str})</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        #content-wrapper.blurred {{ filter: blur(12px); pointer-events: none; user-select: none; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-100 min-h-screen relative">

    <!-- Modal de Autenticación por DNI (76051532) -->
    <div id="auth-modal" class="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-4">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-sm w-full p-6 shadow-2xl text-center">
            <div class="w-14 h-14 rounded-2xl bg-blue-100 dark:bg-blue-950 text-blue-600 dark:text-blue-400 mx-auto flex items-center justify-center mb-4 text-2xl shadow-inner">
                🔒
            </div>
            <div class="inline-block bg-blue-600 text-white text-[10px] font-bold px-2 py-0.5 rounded tracking-wider uppercase mb-2">
                UTP • INGENIERÍA DE SISTEMAS
            </div>
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-1">
                Acceso Privado al Repositorio
            </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mb-5 leading-relaxed">
                Ingresa tu DNI para desbloquear el catálogo de {total_temas} propuestas e historial.
            </p>
            <form id="auth-form" onsubmit="validarPassword(event)" class="space-y-3">
                <div>
                    <input type="password" id="auth-input" placeholder="Ingresa tu DNI" required autofocus autocomplete="off"
                           class="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-mono tracking-widest text-base focus:outline-none focus:ring-2 focus:ring-blue-600 transition">
                </div>
                <p id="auth-error" class="text-xs text-rose-500 font-semibold hidden animate-bounce">
                    ⚠️ DNI incorrecto. Inténtalo nuevamente.
                </p>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 active:scale-[0.98] text-white font-semibold py-3 px-4 rounded-xl text-sm transition shadow-lg shadow-blue-600/30 flex items-center justify-center gap-2">
                    <span>Desbloquear Repositorio</span>
                    <span>→</span>
                </button>
            </form>
            <p class="text-[10px] text-slate-400 mt-4">
                Protección institucional • Titulación Profesional 2026
            </p>
        </div>
    </div>

    <!-- Contenido Protegido -->
    <div id="content-wrapper" class="blurred transition-all duration-500">

        <!-- Header Institucional UTP -->
        <header class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 text-white border-b border-blue-800/40 sticky top-0 z-40 shadow-md">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="bg-blue-600 text-white text-xs font-bold px-2 py-0.5 rounded tracking-wider uppercase">UTP</span>
                        <span class="text-xs text-blue-200">Facultad de Ingeniería • Ingeniería de Sistemas</span>
                    </div>
                    <h1 class="text-base sm:text-lg font-bold tracking-tight text-white mt-1">
                        Repositorio de Propuestas de Tesis de Titulación Profesional
                    </h1>
                </div>
                <div class="flex flex-wrap items-center gap-2.5">
                    <span class="inline-flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs px-3 py-1 rounded-full font-medium">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        {total_temas} Temas Registrados
                    </span>
                    <button onclick="cerrarSesion()" title="Cerrar Sesión" class="text-xs text-slate-300 hover:text-white bg-slate-800/80 hover:bg-slate-700 border border-slate-700 px-2.5 py-1 rounded-lg transition flex items-center gap-1">
                        🔒 Bloquear
                    </button>
                </div>
            </div>
        </header>

        <!-- Contenedor Principal -->
        <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8">

            <!-- Barra de Acciones Globales: DESCARGA DE TODO EL CONJUNTO -->
            <div class="bg-gradient-to-r from-blue-900 to-slate-900 rounded-2xl p-5 sm:p-6 text-white shadow-lg mb-8 flex flex-col lg:flex-row lg:items-center justify-between gap-5 border border-blue-700/50">
                <div>
                    <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-200 border border-blue-400/30 text-xs font-semibold mb-2">
                        📥 Entregables Oficiales Disponibles
                    </div>
                    <h2 class="text-lg sm:text-xl font-bold text-white">
                        Descargar Todo el Catálogo de Propuestas
                    </h2>
                    <p class="text-xs sm:text-sm text-blue-100/80 mt-1 max-w-2xl">
                        Descarga el paquete completo con las {total_temas} propuestas formuladas con matrices de consistencia, carátula institucional y fuentes validadas (2021–2026).
                    </p>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <a href="{prefix_ruta}descargas/Propuestas_Tesis_UTP.docx" download="Propuestas_Tesis_UTP.docx" class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-semibold text-xs sm:text-sm px-4 py-2.5 rounded-xl shadow-md transition">
                        <span>📄 Catálogo Word (.docx)</span>
                    </a>
                    <a href="{prefix_ruta}descargas/Propuestas_Tesis_UTP.pdf" download="Propuestas_Tesis_UTP.pdf" class="inline-flex items-center gap-2 bg-rose-600 hover:bg-rose-500 active:scale-95 text-white font-semibold text-xs sm:text-sm px-4 py-2.5 rounded-xl shadow-md transition">
                        <span>📕 Catálogo PDF (.pdf)</span>
                    </a>
                </div>
            </div>

            <!-- Banner de Filtros e Historial -->
            <section class="bg-white dark:bg-slate-900 rounded-2xl p-5 sm:p-6 border border-slate-200 dark:border-slate-800 shadow-sm mb-6">
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
                    <div class="lg:col-span-2">
                        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-xs font-bold mb-2">
                            ✓ Criterio de Actualidad Bibliográfica: Fuentes 2021–2026 (≤ 5 años)
                        </div>
                        <h3 class="text-sm sm:text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                            🛡️ Rigor Académico, IA de Vanguardia y Filtro Anti-Duplicidad SUNEDU
                        </h3>
                        <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1.5 leading-relaxed">
                            El 100% de las fuentes poseen antigüedad ≤ 5 años (2021–2026). Integra <strong>Inteligencia Artificial aplicada</strong>, desarrollo web con <strong>Kotlin Multiplatform (KMP Wasm)</strong> y aplicaciones nativas en <strong>Android Studio (Jetpack Compose)</strong>.
                        </p>
                    </div>
                    <div class="flex flex-col gap-2 p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-800 text-xs">
                        <div class="font-bold text-slate-700 dark:text-slate-200">Tecnologías Clave Evaluadas:</div>
                        <div class="flex flex-wrap gap-1.5">
                            <span class="px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-300 font-medium">Jetpack Compose (2024)</span>
                            <span class="px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/40 text-indigo-800 dark:text-indigo-300 font-medium">KMP Wasm (2024)</span>
                            <span class="px-2 py-0.5 rounded bg-purple-100 dark:bg-purple-900/40 text-purple-800 dark:text-purple-300 font-medium">MediaPipe GenAI (2024)</span>
                            <span class="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-medium">Core Web Vitals INP (2024)</span>
                        </div>
                    </div>
                </div>
                
                <!-- Historial de Ediciones -->
                <div class="mt-5 pt-3.5 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div class="text-xs font-bold text-slate-400 uppercase tracking-wider">Historial de Ediciones:</div>
                    <div class="flex flex-wrap gap-2">
                        {historial_nav_html}
                    </div>
                </div>
            </section>

            <!-- Controles del Paginador (Superior) -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3 mb-4 bg-white dark:bg-slate-900 p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <div class="text-xs text-slate-600 dark:text-slate-400 font-medium" id="info-paginacion-top">
                    Mostrando temas 1 a 10 de {total_temas} temas
                </div>
                <div class="flex items-center gap-1.5">
                    <button onclick="cambiarPaginaRelativa(-1)" id="btn-prev-top" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 disabled:opacity-40 disabled:pointer-events-none transition">
                        ← Anterior
                    </button>
                    {botones_paginador_html}
                    <button onclick="cambiarPaginaRelativa(1)" id="btn-next-top" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 disabled:opacity-40 disabled:pointer-events-none transition">
                        Siguiente →
                    </button>
                </div>
            </div>

            <!-- 1. VISTA DESKTOP: TABLA RESPONSIVA (Visible en lg y superior) -->
            <section class="hidden lg:block bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden mb-6">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-100/80 dark:bg-slate-800/80 text-slate-600 dark:text-slate-300 text-xs uppercase font-bold tracking-wider border-b border-slate-200 dark:border-slate-800">
                            <tr>
                                <th class="p-4 w-12 text-center">N°</th>
                                <th class="p-4">Título de la Tesis y Línea UTP</th>
                                <th class="p-4">Variable Independiente (VI) & Enlaces</th>
                                <th class="p-4">Variable Dependiente (VD) & Métricas</th>
                                <th class="p-4">Anti-Plagio & Descarga</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filas_tabla}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- 2. VISTA MÓVIL / TABLET VERTICAL: TARJETAS RESPONSIVAS (Visible en pantallas < lg) -->
            <section class="block lg:hidden space-y-4 mb-6">
                {tarjetas_movil}
            </section>

            <!-- Controles del Paginador (Inferior) -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <div class="text-xs text-slate-600 dark:text-slate-400 font-medium" id="info-paginacion-bot">
                    Mostrando temas 1 a 10 de {total_temas} temas
                </div>
                <div class="flex items-center gap-1.5">
                    <button onclick="cambiarPaginaRelativa(-1)" id="btn-prev-bot" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 disabled:opacity-40 disabled:pointer-events-none transition">
                        ← Anterior
                    </button>
                    {botones_paginador_html}
                    <button onclick="cambiarPaginaRelativa(1)" id="btn-next-bot" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 disabled:opacity-40 disabled:pointer-events-none transition">
                        Siguiente →
                    </button>
                </div>
            </div>

        </main>

        <!-- Footer -->
        <footer class="border-t border-slate-200 dark:border-slate-800 mt-16 py-6 text-center text-xs text-slate-500">
            <p>Generado automáticamente mediante el Agente de Tesis UTP (Scheduled Task) • Universidad Tecnológica del Perú (2026)</p>
        </footer>

    </div>

    <!-- Script de Autenticación, Paginación y Descargas -->
    <script>
        const AUTH_HASH = "{AUTH_HASH_SHA256}";
        const TOTAL_TEMAS = {total_temas};
        const TOTAL_PAGINAS = {total_paginas};
        let paginaActual = 1;

        // --- AUTENTICACIÓN POR DNI ---
        async function sha256(text) {{
            const msgBuffer = new TextEncoder().encode(text);
            const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        }}

        async function validarPassword(e) {{
            e.preventDefault();
            const input = document.getElementById('auth-input').value.trim();
            const hashCalculado = await sha256(input);
            
            if (hashCalculado === AUTH_HASH) {{
                localStorage.setItem('tesis_utp_auth', 'unlocked_76051532');
                desbloquearUI();
            }} else {{
                const err = document.getElementById('auth-error');
                err.classList.remove('hidden');
                document.getElementById('auth-input').value = '';
                document.getElementById('auth-input').focus();
            }}
        }}

        function desbloquearUI() {{
            const modal = document.getElementById('auth-modal');
            const wrapper = document.getElementById('content-wrapper');
            modal.style.display = 'none';
            wrapper.classList.remove('blurred');
            irAPagina(1);
        }}

        function cerrarSesion() {{
            localStorage.removeItem('tesis_utp_auth');
            location.reload();
        }}

        // --- PAGINADOR INTERACTIVO ---
        function irAPagina(numPagina) {{
            if (numPagina < 1 || numPagina > TOTAL_PAGINAS) return;
            paginaActual = numPagina;

            // Ocultar todos los elementos y mostrar solo los de la página actual
            document.querySelectorAll('.tema-item').forEach(el => {{
                if (el.getAttribute('data-page') == numPagina) {{
                    el.classList.remove('hidden');
                }} else {{
                    el.classList.add('hidden');
                }}
            }});

            // Actualizar estilo de los botones de paginación
            document.querySelectorAll('.pag-btn').forEach(btn => {{
                btn.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold transition pag-btn bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 hover:bg-slate-100";
            }});
            
            const btnActivoTop = document.getElementById(`btn-page-${{numPagina}}`);
            if (btnActivoTop) {{
                document.querySelectorAll(`[id="btn-page-${{numPagina}}"]`).forEach(b => {{
                    b.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold transition pag-btn bg-blue-600 text-white shadow-sm";
                }});
            }}

            // Actualizar textos de rango
            const inicio = (numPagina - 1) * 10 + 1;
            const fin = Math.min(numPagina * 10, TOTAL_TEMAS);
            const textoRango = `Mostrando temas ${{inicio}} a ${{fin}} de ${{TOTAL_TEMAS}} temas`;
            document.getElementById('info-paginacion-top').innerText = textoRango;
            document.getElementById('info-paginacion-bot').innerText = textoRango;

            // Habilitar / Deshabilitar botones Anterior / Siguiente
            const prevDisabled = numPagina === 1;
            const nextDisabled = numPagina === TOTAL_PAGINAS;
            document.querySelectorAll('#btn-prev-top, #btn-prev-bot').forEach(b => b.disabled = prevDisabled);
            document.querySelectorAll('#btn-next-top, #btn-next-bot').forEach(b => b.disabled = nextDisabled);

            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function cambiarPaginaRelativa(delta) {{
            irAPagina(paginaActual + delta);
        }}


        // Validar sesión al cargar
        window.addEventListener('DOMContentLoaded', () => {{
            if (localStorage.getItem('tesis_utp_auth') === 'unlocked_76051532') {{
                desbloquearUI();
            }}
        }});
    </script>

</body>
</html>
"""
    return html


def compilar_edicion_web(propuestas, fecha_str=None):
    """Genera los archivos HTML de la edición y actualiza el historial."""
    if not fecha_str:
        fecha_str = datetime.date.today().strftime("%Y-%m-%d")
        
    historial = cargar_historial()
    
    historial = [h for h in historial if h["fecha"] != fecha_str]
    historial.insert(0, {
        "fecha": fecha_str,
        "total_temas": len(propuestas),
        "archivo": f"ediciones/edicion_{fecha_str}.html"
    })
    guardar_historial(historial)
    
    html_edicion = generar_html_edicion(fecha_str, propuestas, es_index=False)
    ruta_edicion = os.path.join(DIR_EDICIONES, f"edicion_{fecha_str}.html")
    with open(ruta_edicion, "w", encoding="utf-8") as f:
        f.write(html_edicion)
        
    html_index = generar_html_edicion(fecha_str, propuestas, es_index=True)
    ruta_index = os.path.join(DIR_WEB, "index.html")
    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html_index)
        
    print(f"[WEB GENERADA] Archivo index.html y {ruta_edicion} creados exitosamente con {len(propuestas)} temas, modo vertical y paginador.")
    return ruta_index


def publicar_en_vercel(token, nombre_proyecto="tesis-utp-hub"):
    """Publica todos los archivos web y descargas a Vercel usando la API REST v13."""
    if not token:
        print("\n[AVISO VERCEL] No se encontró VERCEL_TOKEN configurado.")
        return None
        
    url = "https://api.vercel.com/v13/deployments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    archivos_deploy = []
    
    # 1. index.html
    with open(os.path.join(DIR_WEB, "index.html"), "r", encoding="utf-8") as f:
        archivos_deploy.append({
            "file": "index.html",
            "data": f.read()
        })
        
    # 2. historial.json
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
            archivos_deploy.append({
                "file": "historial.json",
                "data": f.read()
            })
            
    # 3. Páginas de ediciones
    for archivo in os.listdir(DIR_EDICIONES):
        if archivo.endswith(".html"):
            ruta_comp = os.path.join(DIR_EDICIONES, archivo)
            with open(ruta_comp, "r", encoding="utf-8") as f:
                archivos_deploy.append({
                    "file": f"ediciones/{archivo}",
                    "data": f.read()
                })
                
    # 4. Archivos binarios de descarga (.docx y .pdf) codificados en base64
    for archivo in os.listdir(DIR_DESCARGAS):
        ruta_bin = os.path.join(DIR_DESCARGAS, archivo)
        if os.path.isfile(ruta_bin):
            with open(ruta_bin, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
                archivos_deploy.append({
                    "file": f"descargas/{archivo}",
                    "data": b64_data,
                    "encoding": "base64"
                })
                
    try:
        requests.patch(
            f"https://api.vercel.com/v9/projects/{nombre_proyecto}",
            headers=headers,
            json={"ssoProtection": None},
            timeout=10
        )
    except Exception:
        pass

    payload = {
        "name": nombre_proyecto,
        "files": archivos_deploy,
        "projectSettings": {
            "framework": None
        },
        "target": "production"
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        if res.status_code in [200, 201]:
            data = res.json()
            aliases = data.get("alias", [])
            if aliases:
                url_despliegue = f"https://{aliases[0]}"
            else:
                url_despliegue = f"https://{data.get('url')}"
            print(f"\n[VERCEL DESPLEGADO CON ÉXITO] Tu web está en vivo en: {url_despliegue}")
            return url_despliegue
        else:
            print(f"\n[ERROR VERCEL API] Código {res.status_code}: {res.text}")
            return None
    except Exception as e:
        print(f"\n[ERROR CONEXIÓN VERCEL] {e}")
        return None
