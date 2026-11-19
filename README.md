# Remitee

Prototipo de una app para poner en contacto a desconocidos que quieren escribirse cartas en papel. Una especie de "Tinder epistolar": la app sirve para encontrarse y la relación ocurre por correo postal.

> Estado: prototipo provisional. Todo funciona en el navegador con datos de ejemplo; no hay servidor ni base de datos.

## Idea

- **Perfiles escritos.** Alias, texto de presentación e intereses. Sin teléfono ni email. Foto opcional, solo después del match.
- **Match mutuo.** La correspondencia se abre solo si las dos personas se eligen. Límite de 3 correspondencias abiertas a la vez.
- **Código de buzón.** Cada persona tiene un código (por ejemplo `LUNA-4821`). Las cartas se envían a una dirección central de la plataforma indicando ese código.
- **Reenvío.** El buzón central resuelve el código y reenvía la carta, en un sobre nuevo, al domicilio real, que solo conoce la plataforma.
- **Revelado mutuo.** Las direcciones solo se muestran cuando ambas personas aceptan.

## Qué se puede probar

| Vista | Qué enseña |
|---|---|
| Descubrir | Perfiles sin foto, elegir o pasar, match y vista previa del sobre con el código |
| Mis correspondencias | Estado de cada carta (escrita → buzón central → reenviada → entregada) y revelado de direcciones |
| Buzón central | El lado de la plataforma: introducir un código y ver a quién corresponde |
| Mi perfil | Campos del perfil y dirección privada |
| Cómo funciona | Recorrido completo de una carta |

## Uso

Abre `index.html` en el navegador. No necesita instalación.

Para publicarlo con GitHub Pages: *Settings → Pages → Deploy from a branch → `main` / root*.

## Pendiente de decidir

- Coste del reenvío (sello, sobre, gestión) y modelo de negocio: suscripción o pago por carta.
- Dirección central real: apartado de correos o servicio de buzón virtual.
- Qué hacer con cartas sin código válido o con contenido inapropiado.
- Verificación de identidad y moderación de perfiles.
- Protección de datos (RGPD) para las direcciones postales.
