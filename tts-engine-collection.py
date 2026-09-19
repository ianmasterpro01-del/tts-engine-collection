import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog, ttk


def cambiar_motor(event=None):
  motor = combo_motor.get()
  if motor == "espeak-ng":
    combo_voz["values"] = [
        "es",
        "es-419",
        "es-es",
        "es+m3",
        "es+f3",
        "es+croak",
        "es+whisper",
        "en-us",
    ]
    combo_voz.set("es-419")
    slider_vel.config(state="normal")
    slider_tono.config(state="normal")
  elif motor == "festival":
    combo_voz["values"] = ["spanish", "default"]
    combo_voz.set("spanish")
    slider_vel.config(state="disabled")
    slider_tono.config(state="disabled")
  elif motor == "pico2wave (SVOX)":
    combo_voz["values"] = ["es-ES", "es-MX", "en-US", "de-DE", "fr-FR"]
    combo_voz.set("es-ES")
    slider_vel.config(state="disabled")
    slider_tono.config(state="disabled")


def hablar():
  texto = caja.get("1.0", tk.END).strip()
  if not texto:
    return

  motor = combo_motor.get()
  voz = combo_voz.get()
  vel = str(slider_vel.get())
  tono = str(slider_tono.get())
  vol = str(slider_vol.get())

  if motor == "espeak-ng":
    subprocess.Popen(
        ["espeak-ng", "-v", voz, "-s", vel, "-p", tono, "-a", vol, texto]
    )
  elif motor == "festival":
    subprocess.Popen(f'echo "{texto}" | festival --tts', shell=True)
  elif motor == "pico2wave (SVOX)":
    temp_wav = os.path.join(tempfile.gettempdir(), "temp_tts.wav")
    subprocess.run(["pico2wave", "-l", voz, "-w", temp_wav, texto])
    subprocess.Popen(["aplay", temp_wav])


def guardar():
  texto = caja.get("1.0", tk.END).strip()
  if not texto:
    status.config(text="Escribe algún texto antes de guardar.", fg="red")
    return

  ruta_archivo = filedialog.asksaveasfilename(
      defaultextension=".wav",
      filetypes=[("Archivo WAV", "*.wav"), ("Todos los archivos", "*.*")],
      title="Selecciona dónde guardar el audio",
  )

  if ruta_archivo:
    motor = combo_motor.get()
    voz = combo_voz.get()
    vel = str(slider_vel.get())
    tono = str(slider_tono.get())
    vol = str(slider_vol.get())

    if motor == "espeak-ng":
      subprocess.run([
          "espeak-ng",
          "-v",
          voz,
          "-s",
          vel,
          "-p",
          tono,
          "-a",
          vol,
          texto,
          "-w",
          ruta_archivo,
      ])
    elif motor == "festival":
      subprocess.run(
          f'echo "{texto}" | text2wave -o "{ruta_archivo}"', shell=True
      )
    elif motor == "pico2wave (SVOX)":
      subprocess.run(["pico2wave", "-l", voz, "-w", ruta_archivo, texto])

    status.config(text="¡Guardado con éxito!", fg="green")

    carpeta_destino = os.path.dirname(ruta_archivo)
    subprocess.Popen(["xdg-open", carpeta_destino])


# Ventana principal
app = tk.Tk()
app.title("TTS Director para Linux")
app.geometry("460x580")

# Caja de texto
tk.Label(app, text="Escribe tu texto aquí:", font=("Arial", 10, "bold")).pack(
    anchor="w", padx=15, pady=(10, 2)
)
caja = tk.Text(app, height=8, font=("Arial", 10))
caja.pack(fill="x", padx=15, pady=5)

# Panel de Controles
frame_controles = tk.Frame(app)
frame_controles.pack(fill="x", padx=15, pady=5)

# Selector de Motor de Voz
tk.Label(
    frame_controles, text="Motor de Voz:", font=("Arial", 9, "bold")
).grid(row=0, column=0, sticky="w", pady=5)
combo_motor = ttk.Combobox(
    frame_controles,
    values=["espeak-ng", "festival", "pico2wave (SVOX)"],
    state="readonly",
    width=18,
)
combo_motor.set("espeak-ng")
combo_motor.grid(row=0, column=1, sticky="e", pady=5)
combo_motor.bind("<<ComboboxSelected>>", cambiar_motor)

# Selector de Voz / Idioma
tk.Label(frame_controles, text="Voz / Variante:").grid(
    row=1, column=0, sticky="w", pady=5
)
combo_voz = ttk.Combobox(frame_controles, state="readonly", width=18)
combo_voz.grid(row=1, column=1, sticky="e", pady=5)

# Sliders
tk.Label(frame_controles, text="Velocidad:").grid(
    row=2, column=0, sticky="w", pady=5
)
slider_vel = tk.Scale(
    frame_controles, from_=80, to=300, orient="horizontal", length=200
)
slider_vel.set(160)
slider_vel.grid(row=2, column=1, pady=5)

tk.Label(frame_controles, text="Tono (Pitch):").grid(
    row=3, column=0, sticky="w", pady=5
)
slider_tono = tk.Scale(
    frame_controles, from_=0, to=99, orient="horizontal", length=200
)
slider_tono.set(50)
slider_tono.grid(row=3, column=1, pady=5)

tk.Label(frame_controles, text="Volumen:").grid(
    row=4, column=0, sticky="w", pady=5
)
slider_vol = tk.Scale(
    frame_controles, from_=0, to=200, orient="horizontal", length=200
)
slider_vol.set(100)
slider_vol.grid(row=4, column=1, pady=5)

# Inicializar opciones según el motor por defecto
cambiar_motor()

# Botones
btn_hablar = tk.Button(
    app,
    text="🔊 Reproducir",
    command=hablar,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold"),
    height=2,
)
btn_hablar.pack(fill="x", padx=15, pady=(15, 5))

btn_guardar = tk.Button(
    app,
    text="💾 Exportar a Audio (.wav)",
    command=guardar,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
)
btn_guardar.pack(fill="x", padx=15, pady=5)

status = tk.Label(app, text="", fg="green")
status.pack(pady=5)

app.mainloop()
