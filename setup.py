from setuptools import setup, find_packages

setup(
    name="desgrabador",
    version="0.1.0",
    description="Herramienta CLI para transcripción de audio/video",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "yt-dlp",
        "openai-whisper",
    ],
    entry_points={
        "console_scripts": [
            "desgrabador=desgrabador.cli:main",
        ],
    },
)
