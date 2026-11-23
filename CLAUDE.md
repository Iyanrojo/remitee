# Remitee · guía para agentes

Remitee es una app web para cartearse por correo postal con desconocidos («Mensajería a fuego lento»).
Web publicada: https://iyanrojo.github.io/remitee/ (GitHub Pages, rama `main`, se publica sola al hacer push).
Propietario: Iyán Rojo. Idioma de trabajo: español.

## Estructura

- `index.html`: toda la app (HTML + CSS + JS en un solo archivo). Es la única fuente de verdad.
- `firebase-config.js`: configuración real de Firebase (proyecto `remitee-c36cf`). **No tocar.**
- `firestore.rules`: reglas de seguridad. Si las cambias, avisa en el registro: el propietario tiene que publicarlas a mano en Firebase.
- `emails/welcome.js`: email de bienvenida «¿Y ahora qué?».
- `hero.mp4`, `favicon.svg`: recursos de la landing.
- `tests/smoke.py`: pruebas automáticas con Firebase simulado (`tests/fbmock.js`). Capturas en `tests/out/` (no se suben).
- `REVIEW_LOG.md`: registro de cada ronda de revisión.

## Convenciones del código

- Textos siempre bilingües con `L("español","English")`. Nada de texto visible sin traducir.
- Colores solo con las variables de `:root` (`--accent`, `--ink`, `--muted`, `--surface`, `--bg`, `--line`, `--ok`, `--warm`, `--bad`, `--sky`…), que se redefinen para modo oscuro. Nunca colores fijos que solo funcionen en un tema.
- Tipografías: Outfit (titulares) e Inter (texto).
- Diseño pensado primero para móvil (400 px de ancho). En escritorio (≥ 820 px) la navegación va arriba.
- Sin librerías nuevas: solo Firebase compat por CDN.
- Los perfiles de ejemplo (bots) llevan la etiqueta «Perfil de ejemplo». Los reales salen siempre antes.
- No usar fotos ni retratos de personas reales (tampoco de personajes ilustres).
- Respetar `prefers-reduced-motion` en cualquier animación.

## Reglas de producto que no se cambian sin permiso del propietario

Match mutuo por intereses e idiomas · escribe primero quien completa el match · doble sobre y dos sellos con reenvío por la oficina de Remitee · plazos (7 días la primera carta, 14 para responder) y suspensión de 3 días · 5 perfiles al día (más con Remitee Plus) · valoración de 0 a 5 sobres · solo mayores de 25 · foto, biografía extensa, galería y mapa solo tras el match · verificación del email obligatoria · eslogan «Mensajería a fuego lento».

## Cómo trabajar en cada ronda

1. `python3 tests/smoke.py` antes de tocar nada. Mira las capturas de `tests/out/` (Read sobre los PNG).
2. Revisa la web como usuario exigente y como diseñador: errores, cosas confusas, textos, jerarquía visual, espaciados, coherencia claro/oscuro, móvil/escritorio, español/inglés, accesibilidad.
3. Elige como mucho 3–5 mejoras concretas y de alto impacto. Nada de rediseños completos ni de cambiar reglas de producto.
4. Aplica los cambios en `index.html`.
5. `python3 tests/smoke.py` otra vez. **Si falla algo, arréglalo o deshaz el cambio. Nunca subas con pruebas en rojo.**
6. Añade la ronda al principio de `REVIEW_LOG.md`: fecha, qué viste, qué cambiaste y qué queda pendiente.
7. Commit en español describiendo los cambios y `git push origin main`.
