# Registro de revisiones de Remitee

Cada ronda del agente revisor se añade arriba: fecha, qué se observó, qué se cambió y qué queda pendiente.

## Ronda 4 · 24 nov 2026

**Qué vi.** Pruebas en verde (57/57). Tras enviar una carta, la ventana de correspondencia decía «Le toca a Ana» junto a «Tu plazo queda en pausa…», mientras el anillo mostraba el plazo de Ana: dos plazos distintos en la misma caja y ninguna fecha. El aviso «Perfil creado. Tu código de buzón es ROCA-8450» partía el código en dos líneas y desaparecía a los 3 s, poco para apuntar un dato importante; además el aviso no se anunciaba a lectores de pantalla. Los selectores (Edad, Cómo quieres que te presentemos) y los desplegables «Quién es Ana» no tenían anillo de foco con teclado. En «Cómo funciona» los personajes de la otra persona seguían con pastel y texto fijos (pendiente de la ronda 3).

**Qué cambié.**
- Correspondencia, carta enviada y aún en camino: «Tu carta va camino de nuestra oficina y tu plazo queda en pausa hasta que llegue. Ana tiene hasta el 13 dic para responder.» (coincide con el anillo).
- Avisos (toast): `role="status"` para lectores de pantalla, los códigos de buzón no se parten y la duración crece con la longitud del texto (de 3,2 a 7 s).
- Anillo de foco también en `select`, `summary` y elementos con `tabindex`.
- «Cómo funciona»: la figura de la otra persona usa `--tint1` y `--on-tint`, y la inicial propia `--on-accent`, así que se adaptan al modo oscuro.
- Pruebas: aviso anunciable con el código sin partir y aviso de plazo con fecha tras enviar (59/59).

**Pendiente.** El arco del mapa hacia una ciudad desplazada sigue apuntando a su posición real. Los intereses los escribe cada persona y salen en su idioma también con la app en inglés (es contenido de usuario; no se traduce). No hay captura de «Cómo funciona» en oscuro en las pruebas: convendría añadirla.

**Propuesta para Iyán.** Siguen abiertas: retomar el tutorial al iniciar sesión sin haberlo terminado (ronda 1) y decidir si «correspondencias» cuenta desde la primera carta enviada o solo con respuesta (en el Perfil sale «0 correspondencias · 1 país»).

## Email de verificación · 24 nov 2026 (aviso de Iyán: «no les llega el email»)

El envío fallaba en silencio: si Firebase rechazaba la URL de vuelta (dominio no autorizado) o el límite de envíos, no se avisaba a nadie. Ahora, si la URL falla, se reenvía sin ella; la pantalla «Revisa tu email» avisa si no se pudo enviar, indica el remitente (noreply@remitee-c36cf.firebaseapp.com) y sugiere mirar en spam. Pendiente en la consola de Firebase: comprobar dominios autorizados y personalizar la plantilla del email.

## Ronda 3 · 23 nov 2026

**Qué vi.** Pruebas en verde (53/53). En escritorio seguía la cabecera doble: barra de pestañas arriba y, debajo, otra fila con el logo y los botones, que empujaba el contenido unos 90 px. En modo oscuro los avatares sin foto (círculos pastel con candado o inicial) eran manchas casi blancas que deslumbraban sobre el fondo oscuro. En el Perfil, cuando una carta iba a una ciudad muy cercana a la tuya (Santander–Bilbao), su punto quedaba tapado por el de casa. En Cartas la segunda línea repetía la etiqueta («Enviada · le toca a Ana» / «Tu carta · enviada») sin aportar nada.

**Qué cambié.**
- Escritorio: una sola barra fija arriba con el logo a la izquierda, las pestañas en el centro y los botones a la derecha. Entre 820 y 1079 px «Cómo funciona» pasa a «?» y las pestañas se centran en el hueco libre para no solaparse (también con el botón de administración).
- Avatares sin foto con fondos en variables (`--tint1`…`--tint5`, `--on-tint`): pastel en claro y tonos apagados con inicial clara en oscuro.
- Mapa de cartas: si una ciudad cae casi encima de casa, su punto se separa unos píxeles para que se vean los dos.
- Cartas: la línea de una carta tuya enviada incluye la fecha de su fase («Tu carta · enviada · 23 nov»).
- Pruebas: la cabecera de escritorio está en una sola barra y los botones no se solapan con las pestañas, también a 820 px con administración (56/56).

**Pendiente.** El arco del mapa hacia una ciudad desplazada sigue apuntando a su posición real (es casi invisible, pero se podría unificar). En el Perfil, con 0 correspondencias puede salir «1 país» (pendiente de la decisión de abajo). Los fondos pastel de las animaciones de «Cómo funciona» (`.fl-them`, `.pp-them`) siguen fijos; revisar en oscuro.

**Propuesta para Iyán.** Siguen abiertas: retomar el tutorial al iniciar sesión sin haberlo terminado (ronda 1) y decidir si «correspondencias» cuenta desde la primera carta enviada o solo con respuesta, para que contador y mapa coincidan (ronda 2).

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
