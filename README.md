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
Orden de prioridad en cada llamada:
1. **MP3 subidos por papá** en el expediente del villano (se guardan solo en ese iPhone).
2. **Voces grabadas del repositorio** (`voices/*.mp3`, listadas en `voices/index.json`): una por guion.
3. **Voz del iPhone**: elige automáticamente una voz masculina para los villanos y una femenina para Hiedra. Si el iPhone no tiene voz masculina en español, instala gratis *Jorge* en Ajustes → Accesibilidad → Contenido leído → Voces → Español.

### Generar las voces grabadas
`tools/generate_voices.py` sintetiza cada línea de cada guion con la voz del personaje (`tools/voices.json`), aplica su efecto (eco helado para Mr. Frío, voz nasal para el Pingüino, voz grave y distorsionada para la cara mala de Dos Caras…), une las líneas y pasa todo por un filtro de línea telefónica.

```bash
# ElevenLabs (la mejor calidad): pon el voice_id de cada villano en tools/voices.json
ELEVENLABS_API_KEY=... python3 tools/generate_voices.py --engine eleven
# Voces neuronales de Microsoft (gratis, sin clave)
pip install edge-tts && python3 tools/generate_voices.py --engine edge
```
Requiere `node` y `ffmpeg`. `--only joker,ivy` regenera solo esos villanos; `--force` sobrescribe.

## Fotos
Cada villano trae su retrato dibujado. Si prefieres otra imagen (por ejemplo, una captura de la serie), súbela en su expediente con *Usar foto propia*. Se guarda solo en el iPhone. *Volver al retrato* la quita.

## Añadir guiones o villanos
Edita el array `VILLAINS` en `index.html`. Cada línea admite `{t, p, r}` (texto, tono, velocidad). El retrato de cada villano está en el objeto `ART` (SVG de 200×200).
