"""Pruebas automáticas de Remitee.

Uso:  python3 tests/smoke.py            (desde la raíz del repositorio)
Abre la web en Chromium con un Firebase simulado, recorre los flujos principales
en móvil y escritorio, en español e inglés, claro y oscuro, y guarda capturas en tests/out/.
Termina con código 1 si algo falla (errores de JavaScript, elementos que faltan, desbordes).
"""
import http.server, json, os, socketserver, sys, threading, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "out"; OUT.mkdir(parents=True, exist_ok=True)
MOCK = (ROOT / "tests" / "fbmock.js").read_text(encoding="utf-8")
SEED = {
  "profiles/A1": {"alias":"Ana","edad":"30–35","zona":"Bilbao","prof":"Arquitecta","bio":"Escribo de noche y leo de día.","intereses":"cine, viajes, poesía","langs":["es","en"],"g":"f","code":"ANA-1001","updatedAt":300},
  "profiles/B2": {"alias":"Bruno","edad":"35–40","zona":"Sevilla","prof":"Músico","bio":"Toco el piano en un bar.","intereses":"música, mar, jazz","langs":["es"],"g":"m","code":"BRU-2002","updatedAt":200},
  "likes/A1_U1": {"from":"A1","to":"U1"},
}
failures = []
def check(cond, msg):
    print(("  ok  " if cond else "  FALLO ") + msg)
    if not cond: failures.append(msg)

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
def serve():
    os.chdir(ROOT)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/"

def new_page(b, url, w, h, lang="es", theme="light", seed=True, logged=False):
    ctx = b.new_context(viewport={"width":w,"height":h})
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/www.gstatic.com/**", lambda r: r.fulfill(status=200, content_type="text/javascript", body=""))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    pg.route("**/firebase-config.js", lambda r: r.fulfill(status=200, content_type="text/javascript", body=MOCK))
    init = f'localStorage.setItem("remitee-lang","{lang}");localStorage.setItem("remitee-theme","{theme}");'
    if seed: init += 'if(!localStorage.getItem("mockdb"))localStorage.setItem("mockdb",' + json.dumps(json.dumps(SEED)) + ');'
    if logged: init += 'localStorage.setItem("mockauth","1");'
    pg.add_init_script(init)
    pg.goto(url); time.sleep(.8)
    return pg, errs

def js(pg, code): return pg.evaluate(code)
def click(pg, sel):
    ok = js(pg, f"(()=>{{const e=document.querySelector({sel!r}); if(!e) return false; e.click(); return true;}})()"); time.sleep(.25); return ok
def close_overlays(pg): js(pg, "document.querySelectorAll('.overlay,.lightbox').forEach(o=>o.remove())")
def no_hscroll(pg, name): check(js(pg, "document.documentElement.scrollWidth <= innerWidth + 1"), f"{name}: sin scroll horizontal")

def run():
    httpd, url = serve()
    with sync_playwright() as p:
        b = p.chromium.launch()
        # 1. Landing en móvil y escritorio
        for w,h,tag in ((400,860,"movil"),(1366,860,"escritorio")):
            pg, errs = new_page(b, url, w, h)
            check(js(pg, "!!document.querySelector('.hero-title')"), f"landing {tag}: titular visible")
            no_hscroll(pg, f"landing {tag}")
            pg.screenshot(path=str(OUT/f"01-landing-{tag}.png"), full_page=(tag=="movil"))
            check(not errs, f"landing {tag}: sin errores JS {errs[:1]}")
            pg.context.close()
        # 2. Registro completo con Google (simulado) + tutorial
        pg, errs = new_page(b, url, 400, 860)
        click(pg, "#start"); check(js(pg, "!!document.querySelector('#g')"), "pantalla de acceso")
        pg.screenshot(path=str(OUT/"02-acceso.png"))
        click(pg, "#g"); time.sleep(.6)
        check(js(pg, "!!document.querySelector('.overlay.wiz')"), "tutorial de alta abierto")
        pg.fill("#w-a","Prueba"); pg.check("#w-25"); pg.fill("#w-z","Cantabria"); click(pg, "#wn")
        click(pg, "#wsk")
        pg.fill("#w-b","Me gusta escribir cartas largas."); pg.fill("#w-i","cine, viajes, poesía"); click(pg, "#wn")
        pg.fill("#w-l","Biografía extensa de prueba."); click(pg, "#wn")
        pg.fill("#w-d","Calle Mayor 1, 39001 Santander"); click(pg, "#wn")
        click(pg, "#wn"); time.sleep(.8)
        check(js(pg, "location.hash") == "#descubrir", "tras el alta se llega a Descubrir")
        db = json.loads(js(pg, "localStorage.getItem('mockdb')"))
        check("profiles/U1" in db and "private/U1" in db, "perfil guardado en Firestore (simulado)")
        # 3. Descubrir: perfiles reales primero
        time.sleep(.6); first = js(pg, "document.querySelector('.card .name')?.textContent")
        check(first in ("Ana","Bruno"), f"Descubrir muestra primero un perfil real (salió: {first})")
        check(js(pg, "!document.querySelector('.card .exbadge')"), "el perfil real no lleva etiqueta de ejemplo")
        pg.screenshot(path=str(OUT/"03-descubrir.png"))
        click(pg, "#more summary"); time.sleep(.3); pg.screenshot(path=str(OUT/"04-perfil-completo.png"), full_page=True)
        # Like a Ana (ya le había elegido) -> match
        for _ in range(3):
            if js(pg, "document.querySelector('.card .name')?.textContent") == "Ana": break
            click(pg, "#no")
        click(pg, "#yes"); time.sleep(.8)
        check(js(pg, "!!document.querySelector('.overlay.mt')"), "match mutuo con un perfil real")
        pg.screenshot(path=str(OUT/"05-match.png"))
        click(pg, ".overlay.mt #go"); time.sleep(.5)
        check(js(pg, "!!document.querySelector('.chead')"), "ventana de correspondencia abierta")
        click(pg, "#sent"); click(pg, "#s-ex"); click(pg, "#s-ok"); time.sleep(.4)
        check(js(pg, "document.querySelectorAll('.lcard').length") >= 1, "carta marcada como enviada")
        pg.screenshot(path=str(OUT/"06-correspondencia.png"), full_page=True)
        click(pg, "#back"); time.sleep(.3)
        check(js(pg, "!!document.querySelector('.item.st-sent')"), "en Cartas aparece como Enviada (verde)")
        pg.screenshot(path=str(OUT/"07-cartas.png"))
        # Persistencia
        pg.reload(); time.sleep(1); js(pg, "location.hash='#cartas'"); time.sleep(.4)
        check(js(pg, "document.querySelectorAll('.item').length") >= 1, "las correspondencias siguen tras recargar")
        # 4. Perfil
        js(pg, "location.hash='#perfil'"); time.sleep(.4)
        check(js(pg, "!!document.querySelector('#pf')"), "perfil editable")
        pg.screenshot(path=str(OUT/"08-perfil.png"), full_page=True)
        no_hscroll(pg, "perfil")
        check(not errs, f"flujo completo sin errores JS {errs[:2]}")
        pg.context.close()
        # 5. Inglés + oscuro + escritorio
        for lang, theme, w, tag in (("en","dark",400,"en-oscuro-movil"),("es","light",1366,"es-escritorio"),("es","dark",1366,"es-oscuro-escritorio")):
            pg, errs = new_page(b, url, w, 860, lang=lang, theme=theme, logged=True)
            time.sleep(.6); js(pg, "location.hash='#descubrir'"); time.sleep(.5)
            if lang == "en": check("Discover" in js(pg, "document.body.innerText"), f"{tag}: interfaz en inglés")
            no_hscroll(pg, tag)
            pg.screenshot(path=str(OUT/f"09-{tag}.png"))
            check(not errs, f"{tag}: sin errores JS {errs[:1]}")
            pg.context.close()
        # 6. Cómo funciona
        pg, errs = new_page(b, url, 400, 860)
        click(pg, "#how"); time.sleep(2.2)
        check(js(pg, "!!document.querySelector('.modal .flow')"), "Cómo funciona: animación visible")
        pg.screenshot(path=str(OUT/"10-como-funciona.png"))
        pg.context.close()
        b.close()
    httpd.shutdown()
    print(f"\n{'TODO BIEN' if not failures else str(len(failures)) + ' FALLOS'} · capturas en {OUT}")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    run()
