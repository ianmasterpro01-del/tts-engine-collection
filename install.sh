#!/bin/bash
# Instalador automático de TTS Director y motores de voz para Debian / MX Linux

# Verificar que se ejecute con privilegios de administrador
if [ "$EUID" -ne 0 ]; then
  echo "Error: Este instalador requiere permisos de administrador."
  echo "Ejecútalo con: sudo bash install.sh"
  exit 1
fi

echo "--------------------------------------------------"
echo " 1/3. Actualizando e instalando motores de voz..."
echo "--------------------------------------------------"
apt update
apt install -y python3 python3-tk espeak-ng festival festvox-ellpc11k libttspico-utils alsa-utils xdg-utils

echo "--------------------------------------------------"
echo " 2/3. Instalando la aplicación en el sistema..."
echo "--------------------------------------------------"
# Crear carpeta de la app en /opt/
INSTALL_DIR="/opt/tts-director"
mkdir -p "$INSTALL_DIR"

# Copiar el script de Python a la carpeta del sistema
if [ -f "tts-engine-collection.py" ]; then
    cp my-tts.py "$INSTALL_DIR/tts-engine-collection.py"
else
    echo "Error: No se encontró el archivo my-tts.py en esta carpeta."
    exit 1
fi

# Crear comando ejecutable global 'tts-director'
cat << 'EOF' > /usr/local/bin/tts-director
#!/bin/bash
python3 /opt/tts-director/ tts-engine-collection.py"$@"
EOF
chmod +x /usr/local/bin/tts-director

echo "--------------------------------------------------"
echo " 3/3. Creando acceso directo en el menú..."
echo "--------------------------------------------------"
DESKTOP_FILE="/usr/share/applications/tts-director.desktop"
cat << 'EOF' > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=TTS Director
Comment=Generador de Voz Robótica y Múltiples Motores
Exec=tts-director
Icon=audio-speakers
Terminal=false
Categories=AudioVideo;Audio;Utility;
EOF
chmod +x "$DESKTOP_FILE"

echo "=================================================="
echo " ¡Instalación completada con éxito!"
echo " - Motores eSpeak, Festival y PicoTTS instalados."
echo " - Puedes iniciarlo buscando 'TTS Director' en el menú."
echo " - O escribiendo 'tts-director' en cualquier terminal."
echo "=================================================="
