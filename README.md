# Arkham Calling

Simulador de llamadas de villanos de Gotham para el iPhone. Papá elige un villano, programa la llamada y deja el móvil a la vista. El villano "llama" a las niñas y siempre acaba igual: si hacen caso a papá, el villano pierde y huye.

Un solo archivo (`index.html`), sin dependencias ni servidor. Se instala como app en la pantalla de inicio.

## Qué hace
- **6 villanos** (Joker, Pingüino, Dos Caras, Hiedra Venenosa, Acertijo, Mr. Frío) y un modo **Sorpresa** que elige uno al azar.
- **Retratos al estilo Batman: The Animated Series**: ilustraciones vectoriales propias con cielo de color, siluetas de Gotham y focos. Cada villano tiene su color y su fondo, así se reconoce de un vistazo.
- **Llamada entrante a pantalla completa**: el retrato ocupa la pantalla, como un póster de contacto de iOS. Luego vienen la pantalla de llamada en curso con el retrato en círculo y la notificación de llamada perdida con su cara.
- **Expedientes**: ficha de cada villano con retrato grande, descripción y "lo que le da miedo". También tiene sus guiones y la opción de subir una foto o unos MP3 propios.
- Tonos, rellamada si rechazan, llamada perdida si nadie coge y salida oculta (mantén pulsada la esquina superior izquierda 1 s).

## Publicar en GitHub Pages
1. Settings → Pages → Deploy from branch → `main` / root.
2. Abre la URL en Safari del iPhone → Compartir → Añadir a pantalla de inicio.

## Uso
- Elige villano y retardo, pulsa *Preparar llamada…* y deja el móvil a la vista.
- Modo silencio desactivado y volumen alto. No bloquees el iPhone.

## Voces
Sin audios, habla la voz del sistema con un tono y una velocidad distintos para cada villano.
Para voces reales: copia un guion desde *Expedientes*, genéralo en ElevenLabs y sube el MP3 al expediente del villano.

## Fotos
Cada villano trae su retrato dibujado. Si prefieres otra imagen (por ejemplo, una captura de la serie), súbela en su expediente con *Usar foto propia*. Se guarda solo en el iPhone. *Volver al retrato* la quita.

## Añadir guiones o villanos
Edita el array `VILLAINS` en `index.html`. Cada línea admite `{t, p, r}` (texto, tono, velocidad). El retrato de cada villano está en el objeto `ART` (SVG de 200×200).
