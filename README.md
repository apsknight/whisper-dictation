# Whisper Dictation

A macOS application that converts speech to text using OpenAI's Whisper model running locally. Press the Globe/Function key to start recording, press it again to stop recording, transcribe, and paste text at your current cursor position.

## Features

- System tray (menu bar) application that runs in the background
- Global hotkey (Globe/Function key) to trigger dictation
- Transcribes speech to text using OpenAI's Whisper model locally
- Automatically pastes transcribed text at your cursor position
- Visual feedback with menu bar icon status

## Setup and Installation

### Development Setup

1. Install Python dependencies:
```
pip install -r requirements.txt
```

2. Install PortAudio (required for PyAudio):
```
brew install portaudio
```

3. Run the application in development mode:
```
python src/main.py
```

### Building the macOS App

To build a standalone macOS application:

1. Install all dependencies:
```
pip install -r requirements.txt
```

2. Build the app:
```
python setup.py py2app
```

3. The app will be created in the `dist` folder. You can then move it to your Applications folder.

## Usage

1. Launch the Whisper Dictation app. You'll see a microphone icon (🎙️) in your menu bar.
2. Press the Globe key or Function key on your keyboard to start recording.
3. Speak clearly into your microphone.
4. Press the Globe/Function key again to stop recording.
5. The app will transcribe your speech and automatically paste it at your current cursor position.

You can also interact with the app through the menu bar icon:
- Click "Start/Stop Listening" to toggle recording
- Access Settings for configuration options
- Click "Quit" to exit the application

## Permissions

The app requires the following permissions:
- Microphone access (to record your speech)
- Accessibility access (to simulate keyboard presses for pasting)

## Requirements

- macOS 10.14 or later
- Microphone