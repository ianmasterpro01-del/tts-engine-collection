# tts-engine-collection

**tts-engine-collection** is a lightweight graphical application developed in Python with Tkinter for text-to-speech synthesis on Linux systems (optimized for MX Linux, Debian and derivatives).

Allows you to select multiple traditional and "robotic" voice engines, adjust speed, tone and volume parameters, and export recordings directly to `.wav` format.

---

## Features

* **Support for multiple voice engines:**
  * **eSpeak-NG:** Classic Loquendo-like robotic voices with tone control, speed, volume and language variants (Latin Spanish, Spanish, female, male voices, etc.).
  * **Festival:** Classic modular synthesizer for Linux.
  * **PicoTTS (SVOX / pico2wave):** Fluid synthesized voice in multiple languages.
* **Simple interface:** Engine selector, drop-down menu of variants and sliders.
* **Audio export:** Saves the result as a `.wav` file and integrates the automatic opening of the destination carpet.
* **Automatic installer:** Script in Bash that resolves dependencies, places the executable on the system and generates the entry in the applications menu.

---

## Installation

Open a terminal and execute the following commands to clone the repository and install the application along with your voice engines:

```bash
git clone [https://github.com/ianmasterpro01-del/tts-engine-collection.git](https://github.com/ianmasterpro01-del/tts-engine-collection.git)
cd tts-engine-collection
sudo bash install.sh
