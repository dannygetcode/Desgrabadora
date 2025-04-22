import subprocess
from pathlib import Path
from typing import Union

def download_media(source: str, output_dir: Path) -> Path:
    """
    Descarga la mejor pista de audio desde una URL (YouTube, Drive...) o procesa
    un archivo local (video/audio), y genera un WAV para transcripción.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    wav_path = output_dir / "media.wav"

    # Si es URL...
    if source.startswith("http"):  # simplificado, usa urllib.parse si deseas
        from yt_dlp import YoutubeDL
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(output_dir / 'media.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'quiet': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([source])
        if not wav_path.exists():
            raise FileNotFoundError(f"No se generó {wav_path}")
        return wav_path

    # Ruta local...
    src_path = Path(source)
    if not src_path.exists():
        raise FileNotFoundError(f"Fuente no encontrada: {source}")

    # Convertir o copiar según extensión
    ext = src_path.suffix.lower()
    if ext == '.wav':
        return src_path
    if ext in ['.mp3', '.m4a', '.flac', '.ogg'] + ['.mp4', '.mkv', '.mov', '.avi', '.webm']:
        cmd = [
            'ffmpeg', '-y', '-i', str(src_path),
            '-ac', '1', '-ar', '16000',  # mono, 16kHz
            str(wav_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return wav_path

    raise ValueError(f"Formato no soportado: {ext}")


def normalize_audio(input_wav: Path, output_wav: Path) -> Path:
    """
    Normaliza volumen al máximo usando loudnorm.
    """
    cmd = [
        'ffmpeg', '-y', '-i', str(input_wav),
        '-af', 'loudnorm', str(output_wav)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_wav


def mejorar_audio(input_wav: Path, output_mp3: Path) -> Path:
    """
    Aplica filtros de FFmpeg para limpieza de ruido y compresión.
    Devuelve MP3.
    """
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg', '-y', '-i', str(input_wav),
        '-af', 'highpass=f=200,lowpass=f=3000,afftdn,acompressor',
        str(output_mp3)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_mp3


def aislar_voz(input_wav: Path, output_wav: Path) -> Path:
    """
    Separa la pista vocal con Demucs en MP3.
    """
    subprocess.run([
        'demucs', str(input_wav),
        '--two-stems=vocals', '-n', 'htdemucs', '--out_format', 'mp3'
    ], check=True)
    sep_dir = Path('separated') / 'htdemucs' / input_wav.stem
    vocals_mp3 = sep_dir / 'vocals.mp3'
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    vocals_mp3.replace(output_wav)
    return output_wav