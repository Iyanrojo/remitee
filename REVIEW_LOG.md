# Registro de revisiones de Remitee

Cada ronda del agente revisor se añade arriba: fecha, qué se observó, qué se cambió y qué queda pendiente.

## Ronda 6 · 25 nov 2026

**Qué vi.** Pruebas en verde (77/77). En la pantalla de acceso no había forma de ver la contraseña al escribirla (en móvil es fácil equivocarse y el alta exige 8 caracteres). Los errores del formulario («Escribe un email válido», «La contraseña necesita…») solo salían en un aviso flotante: el campo no se marcaba, el foco se quedaba en el botón y un lector de pantalla no sabía qué campo fallaba. Las pestañas «Crear cuenta / Ya tengo cuenta» tenían `role="tab"` pero no indicaban cuál estaba activa. Al hacer match, detrás de la ventana «¡Es mutuo!» aparecía además el aviso flotante «Match con Ana.», que repetía lo mismo. Seguía pendiente desde la ronda 3 que el arco del mapa hacia una ciudad desplazada (Bilbao junto a Santander) apuntaba a su posición real y no a su punto.

**Qué cambié.**
- Contraseña: botón «Mostrar / Ocultar» dentro del campo (área táctil de 44 px, `aria-pressed` y nombre accesible bilingüe).
- Formulario de acceso: si un dato no vale, ese campo se marca con borde `--bad`, `aria-invalid` y recibe el foco; la marca se quita al corregirlo. También en «He olvidado mi contraseña» sin email.
- Pestañas del acceso con `aria-selected`.
- Match: el aviso se sigue guardando en Avisos (campana) pero ya no sale flotando detrás de la ventana del match (`notify(…, quiet)`).
- Mapa: punto y arco usan la misma posición, así que el arco llega al punto separado.
- Pruebas: pestaña activa anunciada, mostrar/ocultar contraseña y su área táctil, campo con error marcado y enfocado, marca que se quita al corregir, match sin aviso duplicado pero guardado en Avisos y arcos que terminan en su punto (86/86).

**Pendiente.** El alias de la vista previa de la ventana Plus («Prueba ✓») se podría quitar en pantallas muy bajas. Revisar con lector de pantalla real (VoiceOver/TalkBack) el anuncio de las ventanas. En escritorio la imagen del hero de la landing se ve muy lavada en la captura (parece el póster del vídeo con velo claro); comprobar en la web real si es intencionado.

**Propuesta para Iyán.** Siguen abiertas: retomar el tutorial al iniciar sesión sin haberlo terminado (ronda 1); decidir si «correspondencias» cuenta desde la primera carta enviada o solo con respuesta (ronda 2); y un botón «Quiero Plus» que avise a administración mientras no haya pagos (ronda 5). Esta última pesa más ahora: al agotar los 5 perfiles del día, «Suscribirme a Remitee Plus» abre una ventana que solo tiene «Cerrar».

## Ronda 5 · 24 nov 2026

**Qué vi.** Pruebas en verde (67/67). En el Perfil, la tarjeta «Hazte Remitee Plus» mostraba el tick azul a todo color aunque no tengas Plus: parecía que ya estaba activo. Ninguna ventana (Plus, Avisos, Match, Enviar carta, Cómo funciona, ficha de administración) se cerraba con Esc, el foco se quedaba detrás de la ventana y con Tab se salía a la página; solo dos tenían `role="dialog"`. Varios controles táctiles se quedaban muy por debajo de 44 px: «← Anterior» en Descubrir (24 px de alto), «← Volver»/«← Cartas» (27 px), «Anterior/Siguiente» de la animación del sobre (30 px) y los puntos de paso (8 × 8 px). Faltaba la captura de «Cómo funciona» en oscuro (pendiente de la ronda 4): revisada, se ve bien.

**Qué cambié.**
- Tarjeta de Remitee Plus: sin suscripción, el tick sale apagado en gris y con una flecha «›», así se lee como invitación; con Plus sigue en azul.
- Ventanas: al abrirse reciben el foco, se marcan con `role="dialog"`, `aria-modal` y el título como nombre; Tab y Mayús+Tab no salen de la ventana; Esc la cierra usando su propio botón (Cerrar, Más tarde, Cancelar, Entendido) y el foco vuelve al botón que la abrió. El tutorial de alta no se cierra con Esc y la foto ampliada mantiene su propio Esc.
- Áreas táctiles ampliadas con un pseudoelemento invisible (sin mover el diseño) en «Anterior», «Volver», los botones de la animación y los puntos de paso.
- Pruebas: tick apagado sin Plus, foco dentro de la ventana, Tab atrapado, Esc cierra y devuelve el foco, Esc en «Cómo funciona», área táctil de los puntos y captura `10c-como-oscuro.png` (77/77). Quitado del repositorio `tests/__pycache__` y añadido a `.gitignore`.

**Pendiente.** El arco del mapa hacia una ciudad desplazada sigue apuntando a su posición real. El alias de la vista previa de la ventana Plus («Prueba ✓») se podría quitar en pantallas muy bajas. Revisar con lector de pantalla real (VoiceOver/TalkBack) el anuncio de las ventanas.

**Propuesta para Iyán.** Siguen abiertas: retomar el tutorial al iniciar sesión sin haberlo terminado (ronda 1) y decidir si «correspondencias» cuenta desde la primera carta enviada o solo con respuesta (ronda 2). Nueva: en la web real la ventana de Remitee Plus no tiene ningún botón para pedirlo (solo «Cerrar»); hasta que haya pagos, ¿añadimos un «Quiero Plus» que avise a administración por email?

## Remitee Plus con tick azul · 24 nov 2026 (encargo de Iyán)

El aviso «Email verificado / Identidad verificada con Google» del Perfil sale solo la primera vez que se entra tras verificar (se guarda `vSeen`). Remitee Plus pasa a ser una suscripción mensual con perfiles ilimitados y tick azul junto al alias (Descubrir, Cartas, correspondencia, Perfil y panel de administración); tarjeta en el Perfil y ventana explicativa. Sin pagos todavía: en la web real lo activa administración desde la ficha de cada persona; en el prototipo se simula. **Reglas nuevas: el dueño no puede ponerse `plus` ni quitarse `hidden`; hay que publicarlas en Firebase.**

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
