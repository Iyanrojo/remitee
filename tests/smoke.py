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
# Usuario U1 con perfil ya creado (vuelve a la app con sesión iniciada)
ME = {
  "profiles/U1": {"alias":"Prueba","edad":"30–35","zona":"Cantabria","bio":"Me gusta escribir cartas largas.","intereses":"cine, viajes, poesía","langs":["es","en"],"g":"n","code":"MAR-6517","updatedAt":1},
  "private/U1": {"dir":"Calle Mayor 1","long":"Bio larga"},
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

def new_page(b, url, w, h, lang="es", theme="light", seed=True, logged=False, extra=None):
    ctx = b.new_context(viewport={"width":w,"height":h})
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/www.gstatic.com/**", lambda r: r.fulfill(status=200, content_type="text/javascript", body=""))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    pg.route("**/firebase-config.js", lambda r: r.fulfill(status=200, content_type="text/javascript", body=MOCK))
    init = f'localStorage.setItem("remitee-lang","{lang}");localStorage.setItem("remitee-theme","{theme}");'
    if seed: init += 'if(!localStorage.getItem("mockdb"))localStorage.setItem("mockdb",' + json.dumps(json.dumps({**SEED, **(extra or {})})) + ');'
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
        check(js(pg, "document.querySelector('#toast').getAttribute('role')") == "status" and js(pg, "!!document.querySelector('#toast .nowrap')"), "aviso anunciable y con el código de buzón sin partir")
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
        check(js(pg, "(document.querySelector('.dl.them')||{}).textContent||''").find("tiene hasta el") > 0, "tras enviar, el aviso dice hasta cuándo tiene la otra persona para responder")
        click(pg, "#back"); time.sleep(.3)
        check(js(pg, "!!document.querySelector('.item.st-sent')"), "en Cartas aparece como Enviada (verde)")
        check(js(pg, "(document.querySelector('.item.st-sent .rg-cap')||{}).textContent||''").startswith("plazo de"), "el anillo dice de quién es el plazo")
        pg.screenshot(path=str(OUT/"07-cartas.png"))
        # Persistencia
        pg.reload(); time.sleep(1); js(pg, "location.hash='#cartas'"); time.sleep(.4)
        check(js(pg, "document.querySelectorAll('.item').length") >= 1, "las correspondencias siguen tras recargar")
        # 4. Perfil
        js(pg, "location.hash='#perfil'"); time.sleep(.4)
        check(js(pg, "!!document.querySelector('#pf')"), "perfil editable")
        pg.screenshot(path=str(OUT/"08-perfil.png"), full_page=True)
        no_hscroll(pg, "perfil")
        check(js(pg, "!!document.querySelector('.vpop .verified')"), "ventana «verificado» la primera vez que entras al perfil")
        time.sleep(3.8)
        check(js(pg, "!document.querySelector('.vpop')"), "la ventana «verificado» se va sola con fundido")
        check(js(pg, "!!document.querySelector('#plusCard')"), "tarjeta de Remitee Plus en el perfil")
        check(js(pg, "getComputedStyle(document.querySelector('#plusCard .vtick')).opacity < 1"), "sin Plus, el tick de la tarjeta sale apagado")
        pg.focus("#plusCard"); pg.keyboard.press("Enter"); time.sleep(.3)
        check(js(pg, "!!document.querySelector('.plusm .vtick')"), "Remitee Plus explica el tick azul")
        check(js(pg, "document.querySelector('.plusm').contains(document.activeElement) && document.querySelector('.plusm').getAttribute('aria-modal')==='true'"), "ventana Plus: el foco entra en la ventana (aria-modal)")
        pg.screenshot(path=str(OUT/"08b-plus.png"))
        for _ in range(6): pg.keyboard.press("Tab")
        check(js(pg, "document.querySelector('.plusm').contains(document.activeElement)"), "ventana Plus: Tab no se escapa de la ventana")
        pg.keyboard.press("Escape"); time.sleep(.2)
        check(js(pg, "!document.querySelector('.overlay') && document.activeElement && document.activeElement.id==='plusCard'"), "Esc cierra la ventana y el foco vuelve a la tarjeta")
        pg.reload(); time.sleep(1.2); js(pg, "location.hash='#perfil'"); time.sleep(.4)
        check(js(pg, "!document.querySelector('.vpop')"), "la ventana «verificado» ya no sale en visitas posteriores")
        check(not errs, f"flujo completo sin errores JS {errs[:2]}")
        pg.context.close()
        # 5. Inglés + oscuro + escritorio
        for lang, theme, w, tag in (("en","dark",400,"en-oscuro-movil"),("es","light",1366,"es-escritorio"),("es","dark",1366,"es-oscuro-escritorio")):
            pg, errs = new_page(b, url, w, 860, lang=lang, theme=theme, logged=True, extra=ME)
            time.sleep(1.2); js(pg, "location.hash='#descubrir'"); time.sleep(.6)
            check(js(pg, "!document.querySelector('.land')"), f"{tag}: usuario con perfil entra directo a la app")
            check(js(pg, "!document.querySelector('.sim [data-days]')"), f"{tag}: sin reloj de simulación en producción")
            check(js(pg, "document.querySelector('#adminBtn').hidden"), f"{tag}: sin botón de administración para quien no es admin")
            if lang == "en": check("Discover" in js(pg, "document.body.innerText"), f"{tag}: interfaz en inglés")
            if w >= 820:
                hdr = js(pg, "(()=>{const t=document.querySelector('.top').getBoundingClientRect(), r=document.querySelector('.topr').getBoundingClientRect(), a=[...document.querySelectorAll('.tabs a')].pop().getBoundingClientRect(); return {top:t.bottom<=64, sep:r.left>=a.right}})()")
                check(hdr["top"] and hdr["sep"], f"{tag}: logo y botones en la misma barra que las pestañas, sin solaparse")
            no_hscroll(pg, tag)
            pg.screenshot(path=str(OUT/f"09-{tag}.png"))
            check(not errs, f"{tag}: sin errores JS {errs[:1]}")
            pg.context.close()
        # 5b. Panel de administración
        ADM_SEED = {**ME, "admins/U1": {"note":"test"}, "private/A1": {"email":"ana@x.es","dir":"Calle Luna 3\n48001 Bilbao"}, "likes/U1_A1": {"from":"U1","to":"A1"}}
        for w, tag in ((1366, "escritorio"), (400, "movil")):
            pg, errs = new_page(b, url, w, 900, logged=True, extra=ADM_SEED)
            time.sleep(1.2)
            check(js(pg, "!document.querySelector('#adminBtn').hidden"), f"admin {tag}: botón visible")
            if w == 1366:
                r = pg.evaluate("""async()=>{ let n=0; const u={sendEmailVerification:async(o)=>{ n++; if(o) throw {code:'auth/unauthorized-continue-uri'}; }}; const e=await sendVerify(u); return [e,n]; }""")
                check(r == ["", 2], f"email de verificación: si falla la URL de vuelta se reenvía sin ella {r}")
            click(pg, "#adminBtn"); time.sleep(.8)
            txt = js(pg, "document.querySelector('#view').innerText")
            check("Administración" in txt and "personas registradas" in txt, f"admin {tag}: resumen visible")
            check(js(pg, "[...document.querySelectorAll('.akpis b')].map(b=>b.textContent).join(',')").startswith("3,"), f"admin {tag}: cuenta 3 personas")
            pg.screenshot(path=str(OUT/f"11-admin-{tag}.png"), full_page=True)
            if tag == "escritorio":
                pg.set_viewport_size({"width":820,"height":860}); time.sleep(.3)
                check(js(pg, "document.querySelector('.topr').getBoundingClientRect().left >= [...document.querySelectorAll('.tabs a')].pop().getBoundingClientRect().right"), "admin 820 px: botones de cabecera sin solaparse con las pestañas")
                pg.set_viewport_size({"width":1366,"height":860}); time.sleep(.3)
            no_hscroll(pg, f"admin {tag}")
            if w == 1366:
                click(pg, "[data-at=usuarios]"); time.sleep(.3)
                check(js(pg, "document.querySelectorAll('.atable tbody tr').length") == 3, "admin: tabla con 3 personas")
                pg.screenshot(path=str(OUT/"12-admin-personas.png"))
                click(pg, "[data-at=buzon]"); time.sleep(.3)
                js(pg, "document.querySelector('#acin').value='ana-1001'; document.querySelector('#acode').requestSubmit()"); time.sleep(.3)
                check("Calle Luna 3" in js(pg, "document.querySelector('#acout').innerText"), "admin: el buzón resuelve el código a la dirección")
                pg.screenshot(path=str(OUT/"13-admin-buzon.png"))
                click(pg, "[data-at=matches]"); time.sleep(.3)
                check("Ana" in js(pg, "document.querySelector('#view').innerText") and js(pg, "document.querySelectorAll('.alist.big li').length") == 1, "admin: detecta el match Prueba–Ana")
                click(pg, "[data-at=usuarios]"); time.sleep(.3)
                click(pg, ".atable tbody tr[data-u=B2]"); time.sleep(.4)
                click(pg, "#aplus"); time.sleep(.4)
                check(js(pg, "JSON.parse(localStorage.mockdb)['profiles/B2'].plus === true"), "admin: activar Remitee Plus marca el perfil")
                check(js(pg, "!!document.querySelector('.atable tr[data-u=B2] .vtick')"), "admin: el tick azul sale en la tabla")
                click(pg, ".atable tbody tr[data-u=B2]"); time.sleep(.4)
                click(pg, "#ahide"); time.sleep(.4)
                check(js(pg, "JSON.parse(localStorage.mockdb)['profiles/B2'].hidden === true"), "admin: ocultar un perfil lo marca como oculto")
                pg.screenshot(path=str(OUT/"14-admin-oculto.png"))
            check(not errs, f"admin {tag}: sin errores JS {errs[:1]}")
            pg.context.close()
        # 5b2. Un perfil con Plus lleva tick azul en Descubrir
        pg, errs = new_page(b, url, 400, 860, logged=True, extra={**ME, "profiles/A1": {**SEED["profiles/A1"], "plus": True}, "profiles/B2": {**SEED["profiles/B2"], "hidden": True}})
        time.sleep(1.2); js(pg, "location.hash='#descubrir'"); time.sleep(.6)
        check(js(pg, "!!document.querySelector('.card .name .vtick')"), "perfil con Remitee Plus muestra el tick azul en Descubrir")
        pg.screenshot(path=str(OUT/"10b-tick-descubrir.png"))
        pg.context.close()
        # 5c. Un perfil oculto no sale en Descubrir
        pg, errs = new_page(b, url, 400, 860, logged=True, extra={**ME, "profiles/A1": {**SEED["profiles/A1"], "hidden": True}})
        time.sleep(1.2); js(pg, "location.hash='#descubrir'"); time.sleep(.5)
        check("Ana" not in js(pg, "document.querySelector('#view').innerText"), "perfil oculto no aparece en Descubrir")
        pg.context.close()
        # 6. Cómo funciona
        pg, errs = new_page(b, url, 400, 860)
        click(pg, "#how"); time.sleep(2.2)
        check(js(pg, "!!document.querySelector('.modal .flow')"), "Cómo funciona: animación visible")
        pg.screenshot(path=str(OUT/"10-como-funciona.png"))
        # Área táctil: un toque 15 px por encima de un punto de paso le sigue acertando
        click(pg, '.seg [data-t="1"]'); time.sleep(.4)
        check(js(pg, "(()=>{const d=document.querySelectorAll('.modal .dotb')[2], r=d.getBoundingClientRect(); return document.elementFromPoint(r.x+r.width/2, r.y+r.height/2-15)===d})()"), "Cómo funciona: los puntos de paso tienen área táctil amplia")
        pg.keyboard.press("Escape"); time.sleep(.2)
        check(js(pg, "!document.querySelector('.overlay')"), "Esc cierra «Cómo funciona»")
        check(not errs, f"Cómo funciona: sin errores JS {errs[:1]}")
        pg.context.close()
        # 6b. Guía «Cómo funciona» en oscuro (pendiente de la ronda 4)
        pg, errs = new_page(b, url+"#como", 400, 860, theme="dark", logged=True, extra=ME)
        time.sleep(1); close_overlays(pg); js(pg, "location.hash='#como'"); time.sleep(.5)
        check(js(pg, "!!document.querySelector('#back')"), "Cómo funciona (página) en oscuro")
        no_hscroll(pg, "Cómo funciona oscuro")
        pg.screenshot(path=str(OUT/"10c-como-oscuro.png"))
        check(not errs, f"Cómo funciona oscuro: sin errores JS {errs[:1]}")
        pg.context.close()
        b.close()
    httpd.shutdown()
    print(f"\n{'TODO BIEN' if not failures else str(len(failures)) + ' FALLOS'} · capturas en {OUT}")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    run()
