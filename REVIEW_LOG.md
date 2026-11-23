# Registro de revisiones de Remitee

Cada ronda del agente revisor se añade arriba: fecha, qué se observó, qué se cambió y qué queda pendiente.

## Panel de administración · 23 nov 2026 (encargo de Iyán)

Nuevo panel `#admin` con resumen, personas, buzón central (código → dirección) y matches; moderación para ocultar perfiles en Descubrir; fecha de alta (`createdAt`) en los perfiles nuevos. **Reglas nuevas en `firestore.rules`: Iyán tiene que publicarlas en Firebase.** Pruebas añadidas (panel en móvil y escritorio, buzón, match, ocultar perfil).

## Ronda 2 · 23 nov 2026

**Qué vi.** Pruebas en verde (34/34). En el Perfil propio los textos salían en tercera persona («Escribe en», «Escribe desde Santander») y el mapa decía Santander mientras los datos decían Cantabria. En Cartas el anillo («19 d») no decía de quién era el plazo, y con «le toca a Ana» al lado se podía leer como plazo propio. Los botones redondos de la cabecera miden 38 px, por debajo de los 44 px táctiles recomendados. Los sobres vacíos de la valoración apenas se veían (trazo con el color de las líneas de separación).

**Qué cambié.**
- Perfil propio en segunda persona: «Escribes en», «Escribes desde Cantabria» (la misma zona que en tus datos) y mapa vacío «Todavía no has enviado cartas. Tu mapa empieza con la primera.». Los perfiles ajenos no cambian.
- Bajo el anillo de cada correspondencia en Cartas aparece «tu plazo» o «plazo de Ana» (en inglés «your time» / «Ana's time»), con recorte si el alias es largo.
- Área táctil de 44 px en los botones de cabecera (Cómo funciona, avisos, idioma, tema) sin cambiar su aspecto.
- Sobres vacíos de la valoración con trazo `--muted` semitransparente: se distinguen en claro y en oscuro.
- Pruebas: nueva comprobación de que el anillo indica de quién es el plazo (35/35).

**Pendiente.** Cabecera doble en escritorio (barra de pestañas arriba + logo y botones debajo). En el Perfil, con 0 correspondencias puede salir «1 país» porque el mapa cuenta cartas enviadas y el contador solo correspondencias con respuesta; conviene unificar el criterio. El punto de casa y el de Bilbao se solapan en el mapa (ciudades muy cercanas).

**Propuesta para Iyán.** Sigue abierta la de la ronda 1 (retomar el tutorial al iniciar sesión sin haberlo terminado). Nueva: decidir si «correspondencias» debe contar desde la primera carta enviada o solo cuando hay respuesta, para que contador y mapa digan lo mismo.

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
