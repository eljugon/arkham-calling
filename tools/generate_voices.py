#!/usr/bin/env python3
"""Genera los MP3 de cada guion y los deja en voices/ para que la app los use.

Uso:
  ELEVENLABS_API_KEY=... python3 tools/generate_voices.py --engine eleven
  python3 tools/generate_voices.py --engine edge        # gratis, pip install edge-tts
Opciones: --only joker,ivy   --force (regenerar aunque existan)

Cada línea del guion se sintetiza por separado (Dos Caras alterna dos voces), se le
aplica el efecto del villano (tools/voices.json), se unen con pausas cortas y al
final todo pasa por un filtro de "línea telefónica" para que suene a llamada real.
"""
import argparse, asyncio, json, os, pathlib, subprocess, sys, tempfile, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOICES_DIR = ROOT / "voices"
CFG = json.loads((ROOT / "tools" / "voices.json").read_text())
PHONE = "highpass=f=220,lowpass=f=3600,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5"
PAUSE_S = 0.45

def load_villains():
    """Saca el array VILLAINS de index.html evaluándolo con Node (son datos JS, no JSON)."""
    js = r"""
const fs=require('fs'),vm=require('vm');
const h=fs.readFileSync(process.argv[1],'utf8');
const a=h.indexOf('const VILLAINS = ['), b=h.indexOf('\n];',a);
const V=vm.runInNewContext(h.slice(a+'const VILLAINS = '.length,b+2));
process.stdout.write(JSON.stringify(V.map(v=>({id:v.id,voice:v.voice,scripts:v.scripts}))));
"""
    out = subprocess.run(["node", "-e", js, str(ROOT / "index.html")], check=True, capture_output=True, text=True).stdout
    return json.loads(out)

def is_bad(line, villain):
    # En los guiones, las líneas de la cara mala de Dos Caras llevan tono bajo (p < 0.8)
    return villain["id"] == "twoface" and isinstance(line, dict) and line.get("p", 1) < 0.8

def text_of(line):
    return line if isinstance(line, str) else line["t"]

# ---------- motores ----------
def synth_eleven(text, conf, out_path):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key: sys.exit("Falta ELEVENLABS_API_KEY")
    if not conf.get("voice_id"): sys.exit("Falta voice_id de ElevenLabs en tools/voices.json")
    body = json.dumps({
        "text": text, "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2"), "language_code": "es",
        "voice_settings": {"stability": conf.get("stability", 0.4), "similarity_boost": 0.8, "style": conf.get("style", 0.5), "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{conf['voice_id']}?output_format=mp3_44100_128",
                                 data=body, headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out_path.write_bytes(r.read())

def synth_edge(text, conf, out_path):
    import edge_tts  # pip install edge-tts
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    c = edge_tts.Communicate(text, conf["voice"], pitch=conf.get("pitch", "+0Hz"), rate=conf.get("rate", "+0%"), proxy=proxy)
    asyncio.run(c.save(str(out_path)))

SYNTH = {"eleven": synth_eleven, "edge": synth_edge}

def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)

def render_script(villain, si, engine, out_mp3):
    vc = CFG[villain["id"]]
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        parts = []
        silence = td / "pause.wav"
        ff("-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono", "-t", str(PAUSE_S), silence)
        for li, line in enumerate(villain["scripts"][si]["lines"]):
            bad = is_bad(line, villain)
            conf = vc.get(f"{engine}_bad") if bad else vc[engine]
            fx = vc.get("fx_bad" if bad else "fx", "") or "anull"
            raw = td / f"{li}.mp3"
            SYNTH[engine](text_of(line), conf, raw)
            wav = td / f"{li}.wav"
            ff("-i", raw, "-af", f"aresample=24000,{fx}", "-ac", "1", "-ar", "24000", wav)
            parts += [wav, silence]
        lst = td / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        ff("-f", "concat", "-safe", "0", "-i", lst, "-af", PHONE, "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "96k", out_mp3)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", choices=SYNTH, default="eleven")
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    only = set(filter(None, a.only.split(",")))
    VOICES_DIR.mkdir(exist_ok=True)
    index = {}
    for v in load_villains():
        for si, s in enumerate(v["scripts"]):
            out = VOICES_DIR / f"{v['id']}-{si}.mp3"
            if (not only or v["id"] in only) and (a.force or not out.exists()):
                print(f"→ {v['id']} · {s['title']}", flush=True)
                render_script(v, si, a.engine, out)
            if out.exists():
                index.setdefault(v["id"], []).append({"script": si, "title": s["title"], "file": f"voices/{out.name}"})
    (VOICES_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
    print(f"Listo: {sum(map(len, index.values()))} audios en voices/")

if __name__ == "__main__":
    main()
