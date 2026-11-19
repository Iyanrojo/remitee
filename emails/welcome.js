// Email de bienvenida de Remitee ("¿Y ahora qué?"). Lo usa index.html y sirve para generar las vistas previas.
// HTML pensado para clientes de correo: tablas, estilos en línea y sin imágenes externas.
(function (root) {
  function welcomeEmail(lang, alias, code, siteUrl, g) {
    const en = lang === "en";
    const L = (es, e) => (en ? e : es);
    const esc = s => String(s || "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    const name = esc(alias) || L("hola", "there");
    const box = esc(code) || "LUNA-4821";
    const url = siteUrl || "https://iyanrojo.github.io/remitee/";
    const A = "#5b6cf0", INK = "#22263a", MUTED = "#6b7189", SOFT = "#eceefe", BG = "#f7f8fc", LINE = "#e6e8f0";
    const font = "font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;";
    const steps = [
      [L("Descubre perfiles", "Discover profiles"), L("Cada día puedes leer 5 perfiles. Primero los intereses y los idiomas; la foto, después del match.", "Each day you can read 5 profiles. Interests and languages first; photos after the match.")],
      [L("Haz match", "Make a match"), L("Si los dos os elegís, se abre la correspondencia. Escribe primero quien completa el match: la app te lo dirá.", "If you both choose each other, the correspondence opens. Whoever completes the match writes first: the app will tell you.")],
      [L("Escribe tu carta", "Write your letter"), L("En papel, a mano si quieres. Sin prisa: tienes 7 días para la primera carta.", "On paper, by hand if you like. No rush: you have 7 days for the first letter.")],
      [L("Doble sobre y dos sellos", "Two envelopes, two stamps"), L("Mete la carta en un sobre cerrado con solo el código de la otra persona. Ese sobre y un segundo sello van dentro de otro dirigido a nuestra oficina.", "Seal the letter in an envelope with only the other person's code. That envelope and a second stamp go inside another one addressed to our office.")],
      [L("Márcala como enviada", "Mark it as sent"), L("Haz una foto del sobre interior y pulsa «Ya he enviado la carta». Te avisaremos en cada paso del camino.", "Take a photo of the inner envelope and tap “I've sent the letter”. We'll let you know at every step.")]
    ];
    const subject = L(`${alias ? alias + ", ¿y" : "¿Y"} ahora qué? Tu primera carta en Remitee`, `${alias ? alias + ", what" : "What"} now? Your first letter on Remitee`);
    const preheader = L("Cinco pasos para enviar tu primera carta. Sin prisas.", "Five steps to send your first letter. No rush.");
    const stepRows = steps.map(([t, d], i) => `
      <tr><td style="padding:0 0 18px 0;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="44" valign="top"><div style="width:32px;height:32px;line-height:32px;border-radius:16px;background:${SOFT};color:${A};text-align:center;${font}font-weight:700;font-size:15px;">${i + 1}</div></td>
          <td valign="top" style="${font}">
            <div style="font-size:16px;font-weight:700;color:${INK};margin:4px 0 4px;">${t}</div>
            <div style="font-size:14px;line-height:21px;color:${MUTED};">${d}</div>
          </td>
        </tr></table>
      </td></tr>`).join("");
    const html = `<!doctype html><html lang="${en ? "en" : "es"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(subject)}</title></head>
<body style="margin:0;padding:0;background:${BG};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">${preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${BG};"><tr><td align="center" style="padding:32px 14px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px;">
    <tr><td style="padding:0 6px 22px;${font}">
      <span style="font-size:24px;font-weight:700;color:${INK};letter-spacing:-0.5px;">remitee<span style="color:${A};">.</span></span><br>
      <span style="font-size:12px;color:${MUTED};">${L("Mensajería a fuego lento", "Slow-cooked mail")}</span>
    </td></tr>
    <tr><td style="background:#ffffff;border-radius:22px;padding:34px 30px;${font}">
      <div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:${A};margin-bottom:10px;">${en ? "Welcome to Remitee" : ({ f: "Bienvenida a Remitee", m: "Bienvenido a Remitee" }[g] || "Te damos la bienvenida")}</div>
      <h1 style="margin:0 0 14px;font-size:30px;line-height:34px;color:${INK};font-weight:700;letter-spacing:-0.5px;">${L("¿Y ahora qué?", "What now?")}</h1>
      <p style="margin:0 0 22px;font-size:15px;line-height:23px;color:${INK};">${L(`Hola, ${name}. Ya tienes tu perfil en Remitee. Aquí las cosas van despacio, y eso es lo bonito. Estos son los pasos para enviar tu primera carta:`, `Hi ${name}. Your Remitee profile is ready. Things move slowly here, and that's the beauty of it. Here's how to send your first letter:`)}</p>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">${stepRows}</table>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 24px;"><tr><td style="background:${SOFT};border-radius:16px;padding:16px 18px;${font}">
        <div style="font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:${MUTED};margin-bottom:4px;">${L("Tu código de buzón", "Your mailbox code")}</div>
        <div style="font-family:Menlo,Consolas,monospace;font-size:20px;font-weight:700;color:${A};">${box}</div>
        <div style="font-size:13px;line-height:19px;color:${MUTED};margin-top:4px;">${L("Es lo que la gente escribirá en el sobre para ti. Tu dirección nunca se comparte.", "It's what people write on the envelope for you. Your address is never shared.")}</div>
      </td></tr></table>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-radius:999px;background:${A};">
        <a href="${url}" style="display:inline-block;padding:14px 28px;${font}font-size:15px;font-weight:700;color:#ffffff;text-decoration:none;border-radius:999px;">${L("Descubrir perfiles", "Discover profiles")}</a>
      </td></tr></table>
    </td></tr>
    <tr><td style="padding:22px 8px 0;${font}">
      <p style="margin:0 0 6px;font-size:17px;font-weight:700;color:${INK};">${L("Lo bueno tarda en llegar.", "Good things take time.")}</p>
      <p style="margin:0;font-size:12px;line-height:18px;color:${MUTED};">${L("Recibes este email porque acabas de crear tu perfil en Remitee. Solo para mayores de 25 años.", "You're receiving this email because you've just created your Remitee profile. Over 25s only.")}<br>Remitee · ${L("Apartado", "PO Box")} 123 · 39080 Santander</p>
    </td></tr>
  </table>
</td></tr></table>
</body></html>`;
    const text = [L("¿Y ahora qué?", "What now?"), "", L(`Hola, ${alias || ""}. Ya tienes tu perfil en Remitee.`, `Hi ${alias || ""}. Your Remitee profile is ready.`), "",
      ...steps.map(([t, d], i) => `${i + 1}. ${t}: ${d}`), "", `${L("Tu código de buzón", "Your mailbox code")}: ${code || ""}`, "", url, "", L("Lo bueno tarda en llegar.", "Good things take time.")].join("\n");
    return { subject, html, text };
  }
  root.welcomeEmail = welcomeEmail;
  if (typeof module !== "undefined") module.exports = welcomeEmail;
})(typeof window !== "undefined" ? window : globalThis);
