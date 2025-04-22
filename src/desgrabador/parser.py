import whisper
from pathlib import Path
from typing import Dict, List

def transcribe_audio(
    audio_path: Path,
    model_size: str = 'base',
    language: str = 'es',
    temperature: float = 0.0,
    device: str = 'cpu'
) -> Dict:
    """
    Transcribe con Whisper, soporta modelo, idioma, temperatura y device.
    """
    model = whisper.load_model(model_size).to(device)
    result = model.transcribe(
        str(audio_path), language=language, temperature=[temperature]
    )
    return result


def save_as_txt(transcript: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(transcript, encoding='utf-8')


def save_as_srt(segments: List[Dict], output_path: Path) -> None:
    def fmt(ts: float) -> str:
        h = int(ts//3600)
        m = int((ts%3600)//60)
        s = int(ts%60)
        ms = int((ts-int(ts))*1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n{fmt(seg['start'])} --> {fmt(seg['end'])}\n{seg['text'].strip()}\n\n")