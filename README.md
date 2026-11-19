# Remitee

*Mensajería a fuego lento.*

Prototipo de una app para poner en contacto a desconocidos que quieren escribirse cartas en papel. Una especie de "Tinder epistolar": la app sirve para encontrarse y la relación ocurre por correo postal.

> Estado: prototipo provisional. Todo funciona en el navegador con datos de ejemplo; no hay servidor ni base de datos.

## Idea

- **Perfiles escritos.** Alias, texto de presentación e intereses. Sin teléfono ni email. Foto opcional, solo después del match.
- **Match mutuo.** La correspondencia se abre solo si las dos personas se eligen. Límite de 3 correspondencias abiertas a la vez.
- **Código de buzón.** Cada persona tiene un código (por ejemplo `LUNA-4821`). Las cartas se envían a una dirección central de la plataforma indicando ese código.
- **Reenvío.** El buzón central resuelve el código y reenvía la carta, en un sobre nuevo, al domicilio real, que solo conoce la plataforma.
- **Revelado mutuo.** Las direcciones solo se muestran cuando ambas personas aceptan.

## Reglas

- **Plazos.** Tras el match hay 7 días para enviar la primera carta y marcarla en la app. Cada carta recibida da 14 días para responder.
- **Penalización.** Quien no cumple su plazo cierra la correspondencia y su cuenta queda suspendida 3 días, sin poder hacer nuevos matches.
- **Edad mínima.** Solo mayores de 25 años.
- **Registro obligatorio.** Para entrar hay que registrarse con Google (en el prototipo, simulado) y crear el perfil.
- **Perfiles diarios.** Se pueden ver 5 perfiles al día. Para ver más hay que suscribirse a Remitee Plus.
- **Tras el match.** Se desbloquean la foto, si la persona la comparte, y la biografía extensa.

- **Quién escribe primero.** Quien completa el match, es decir, quien dice que sí en segundo lugar.
- **Doble sobre y dos sellos.** La carta va en un sobre interior cerrado con solo el código del destinatario. Ese sobre y un segundo sello van dentro de un sobre exterior dirigido a Remitee. En la oficina se abre solo el exterior y el segundo sello se usa para reenviar el interior, intacto.
- **Seguimiento.** Al enviar se sube una foto del sobre interior. Cada carta pasa por cuatro fases visibles para los dos: enviada, en la oficina, reenviada y entregada.
- **Coste.** La app es gratis; cada persona pone sus dos sellos. Remitee Plus es opcional.
- **Historial.** Cada perfil muestra cuántas correspondencias ha tenido y si responde a tiempo. Quien acaba de llegar aparece como recién llegado, recién llegada o nueva en Remitee.

- **Nunca contesta.** Quien ha perdido 2 o más matches por no responder lo muestra en su perfil.
- **Avisos.** Cada cambio de fase de una carta se notifica por email y en la app a las dos personas (por ejemplo: «Tu carta está en nuestra oficina. Se la enviaremos a Lince»). Los canales se eligen en el perfil.

- **Valoraciones.** Quien recibe una carta la valora de 0 a 5 cartas. Cada perfil muestra la media y el número de valoraciones.
- **Idiomas.** Español e inglés, con un botón ES/EN en la cabecera. Por defecto se usa el idioma del navegador.

## Qué se puede probar

| Vista | Qué enseña |
|---|---|
| Descubrir | Perfiles sin foto, elegir o pasar, match y vista previa del sobre con el código |
| Mis correspondencias | Estado de cada carta (escrita → buzón central → reenviada → entregada) y revelado de direcciones |
| Buzón central | El lado de la plataforma: introducir un código y ver a quién corresponde |
| Mi perfil | Campos del perfil y dirección privada |
| Cómo funciona | Recorrido completo de una carta |

## Uso

Para el vídeo de la landing, sube un archivo `hero.mp4` a la raíz del repositorio (junto a `index.html`). Se reproduce solo, en bucle y sin sonido; mientras no exista, se ve un hueco reservado.

Abre `index.html` en el navegador. No necesita instalación.

Para publicarlo con GitHub Pages: *Settings → Pages → Deploy from a branch → `main` / root*.

## Activar el login con Google (Firebase)

Mientras `firebase-config.js` esté vacío, la web funciona en modo prototipo: el login se simula y el perfil se guarda solo en el navegador.

1. Crea un proyecto en [Firebase](https://console.firebase.google.com) (el plan gratuito basta).
2. **Authentication → Sign-in method:** activa **Google**.
3. **Authentication → Settings → Authorized domains:** añade el dominio donde se publica la web (por ejemplo `tuusuario.github.io` o `remitee.netlify.app`).
4. **Firestore Database:** créala en modo producción, en una región europea (por ejemplo `europe-southwest1`, Madrid).
5. **Firestore → Reglas:** pega el contenido de `firestore.rules` y publica.
6. **Configuración del proyecto → Tus apps → App web:** copia el bloque `firebaseConfig` en `firebase-config.js`.

Qué se guarda:

- `profiles/{uid}`: alias, edad, zona, profesión, biografías, intereses, género, código de buzón. Lo leen las personas registradas.
- `private/{uid}`: email, dirección postal y preferencias de avisos. Solo lo lee su dueño.

Pendiente: mostrar en Descubrir los perfiles reales, matches entre usuarios, fotos (Firebase Storage) y envío real de emails.

## Pendiente de decidir

- Coste del reenvío (sello, sobre, gestión) y modelo de negocio: suscripción o pago por carta.
- Dirección central real: apartado de correos o servicio de buzón virtual.
- Qué hacer con cartas sin código válido o con contenido inapropiado.
- Verificación de identidad y moderación de perfiles.
- Protección de datos (RGPD) para las direcciones postales.
