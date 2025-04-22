import argparse
from pathlib import Path
from .downloader import (
    download_media, normalize_audio,
    mejorar_audio, aislar_voz
)
from .parser import transcribe_audio, save_as_txt, save_as_srt


def main():
    p = argparse.ArgumentParser(prog='desgrabador')
    p.add_argument('-s','--source', required=True, help='URL o ruta local')
    p.add_argument('-m','--model', choices=['tiny','base','small','medium','large'], default='base')
    p.add_argument('-o','--output-dir', default='outputs')
    p.add_argument('--no-txt', action='store_true')
    p.add_argument('--no-srt', action='store_true')
    p.add_argument('--temperature', type=float, default=0.0)
    p.add_argument('--language', default='es')
    p.add_argument('--device', choices=['cpu','cuda'], default='cpu')
    args = p.parse_args()

    out = Path(args.output_dir)
    out.mkdir(exist_ok=True)
    print(f"🔍 Procesando: {args.source}")

    wav = download_media(args.source, out)
    norm = out / 'media_normalized.wav'
    normalize_audio(wav, norm)
    wav = norm
    print(f"🎤 Normalizado: {wav}")

    if input("¿Aislar voz? (s/n): ").strip().lower()=='s':
        iso = out / 'media_vocals.mp3'
        wav = aislar_voz(wav, iso)
        print(f"🗣 Voces: {wav}")

    if input("¿Mejorar audio? (s/n): ").strip().lower()=='s':
        imp = out / 'media_improved.mp3'
        mejorar_audio(wav, imp)
        wav = imp
        print(f"🎧 Mejorado: {wav}")

    print(f"🤖 Transcribiendo ({args.model})…")
    res = transcribe_audio(
        wav, model_size=args.model,
        language=args.language,
        temperature=args.temperature,
        device=args.device
    )

    if not args.no_txt:
        txt = out / 'transcripcion.txt'
        save_as_txt(res['text'], txt)
        print(f"✅ TXT: {txt}")
    if not args.no_srt:
        srt = out / 'transcripcion.srt'
        save_as_srt(res['segments'], srt)
        print(f"✅ SRT: {srt}")

if __name__=='__main__':
    main()