# AI Hand Gesture Volume Controller

A real-time, AI-powered Windows application that lets users control system volume, mute/unmute audio, and play/pause media using hand gestures through a webcam.

## Features

- Real-time hand tracking with MediaPipe
- 21 hand landmark detection and visualization
- Touch-free Windows system volume control
- Fist gesture for mute/unmute
- Open palm gesture for media play/pause
- Exponential smoothing for stable volume changes
- Gesture confirmation and cooldown system
- Live volume percentage, FPS, and gesture status
- Premium dark-themed dashboard

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- PyInstaller

## How It Works

1. OpenCV captures live webcam frames.
2. MediaPipe detects 21 hand landmarks.
3. Finger joint angles identify hand gestures.
4. Thumb-to-index distance determines the target volume.
5. Pycaw updates the Windows system audio.
6. Windows media key events control compatible media players.

## Gesture Controls

| Gesture | Action |
|---|---|
| Thumb and Index Distance (Index Extended) | Increase / Decrease Volume |
| Closed Fist (Hold 1 Second) | Mute / Unmute |
| Open Palm (Hold 1 Second) | Play / Pause Media |
| C Key | Enable Gesture Control |
| P Key | Pause Gesture Control |
| Q Key | Exit Application |

## Installation

**Requirements:** Windows 10/11, Python 3.11, a webcam, and an audio output device.

Clone the repository:

```bash
git clone https://github.com/Paradoxai77/Volume-Controller.git
cd Volume-Controller
```

Create and activate a virtual environment:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Download the MediaPipe Hand Landmarker model:

```powershell
New-Item -ItemType Directory -Force models
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -OutFile "models\hand_landmarker.task"
```

Run the application:

```powershell
python main.py
```

## Windows Executable

The application can also be packaged with PyInstaller. If a Windows release is available, download the ZIP from the GitHub Releases section, extract the complete folder, and run `GestureStudio.exe`.

## Project Structure

```text
AI-Hand-Gesture-Volume-Controller/
├── main.py
├── models/
│   └── hand_landmarker.task
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitations

- Currently supports Windows system audio.
- Requires a functioning webcam and suitable lighting.
- Finger-angle recognition may vary with hand orientation.
- Media play/pause depends on the receiving application.

## Future Improvements

- Automatic gesture calibration
- More advanced gesture recognition
- Customizable gesture mappings
- Improved UI and background operation
- Cross-platform support

## Author

**Paradoxai77**

GitHub: https://github.com/Paradoxai77

## License

No license has been specified yet.