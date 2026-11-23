# Registro de revisiones de Remitee

Cada ronda del agente revisor se añade arriba: fecha, qué se observó, qué se cambió y qué queda pendiente.

## Ronda 1 · 23 nov 2026

**Qué vi.** Las pruebas pasaban (28/28), pero un usuario que volvía con sesión iniciada lanzaba un error de JavaScript (`#vph` ya no existía cuando cargaba el vídeo). El reloj de simulación (+1 día / +7 días) se veía en producción y permitía saltarse los plazos. El botón principal tenía poco contraste en oscuro (≈2,6:1) y el gris de texto también en claro (≈3,1:1). El aviso inferior tapaba el botón de Descubrir. En escritorio había un hueco de unos 100 px bajo el titular y la franja azul quedaba cortada. El selector de foto del Perfil salía nativo y en inglés.

**Qué cambié.**
- Arreglado el error al volver con sesión iniciada.
- El reloj de simulación solo aparece en modo demo o con `?sim` en la URL.
- Nuevo token `--on-accent` (blanco en claro, casi negro en oscuro) para el texto sobre el azul; `--muted` claro pasa a `#6b7186`. Ambos superan AA.
- Aviso (toast) más arriba, con esquinas de 16 px y ancho máximo; quitado el `z-index` duplicado.
- Titular de escritorio en una línea por frase (sin hueco) y franja azul a todo el ancho.
- Botón propio y bilingüe para la foto del Perfil; «Sobre Ana» pasa a «Quién es Ana» para no confundirlo con los sobres.
- Pruebas: los pasos en oscuro, escritorio e inglés ahora entran con un perfil real (antes se quedaban en la landing) y comprueban que no aparece el reloj de simulación.

**Pendiente.** Indicar de quién es el plazo bajo el anillo («plazo de Ana»); mapa del propio perfil en segunda persona; cabecera doble en escritorio; botones de cabecera de 44 px en móvil.

**Propuesta para Iyán.** Quien inicia sesión pero no terminó el tutorial vuelve a la landing; quizá debería retomar el tutorial directamente.
