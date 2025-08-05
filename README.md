# Whisper Dictation

**Note: This application is for macOS only.**

A macOS application that converts speech to text using OpenAI's Whisper Large V3 Turbo model deployed on Amazon SageMaker. Press the Globe/Function key to start recording, press it again to stop recording, transcribe, and paste text at your current cursor position.

## Features

- System tray (menu bar) application that runs in the background
- Global hotkey (Globe/Function key) to trigger dictation
- Transcribes speech to text using OpenAI's Whisper Large V3 Turbo model on Amazon SageMaker
- Automatically pastes transcribed text at your cursor position
- Visual feedback with menu bar icon status
- High-quality transcription with powerful cloud-based inference

## Setup and Installation

### Prerequisites

1. **AWS Account**: You need an AWS account with appropriate permissions for SageMaker and Bedrock.
2. **AWS CLI**: Install and configure AWS CLI with your credentials:
   ```bash
   aws configure
   ```

### Step 1: Deploy Whisper Large V3 Turbo on SageMaker

1. **Access Amazon Bedrock Model Catalog**:
   - Go to the [AWS Console](https://console.aws.amazon.com/)
   - Navigate to **Amazon Bedrock** service
   - Click on **Model catalog** in the left sidebar

2. **Find Whisper Large V3 Turbo**:
   - Search for "Whisper Large V3 Turbo" in the model catalog
   - Select the model from the search results

3. **Deploy to SageMaker Endpoint**:
   - Click **"Deploy to SageMaker endpoint"**
   - Configure the deployment:
     - **Endpoint name**: `whisper-inference` (or your preferred name)
     - **Instance type**: `ml.g5.2xlarge` (recommended for optimal performance)
     - **Instance count**: `1`
   - Click **"Deploy"** and wait for the endpoint to be in "InService" status (this may take 5-10 minutes)

4. **Note your endpoint details**:
   - Endpoint name: e.g., `whisper-inference`
   - Region: Note the AWS region where you deployed (e.g., `us-west-2`)

### Step 2: Configure the Application

1. **Create configuration file**:
   ```bash
   cp src/config.env.example config.env
   ```

2. **Edit `config.env`** with your endpoint details:
   ```bash
   # Whisper Dictation Configuration
   WHISPER_ENDPOINT_NAME=your-endpoint-name
   AWS_REGION=your-aws-region
   
   # Optional: AWS Profile (if not using default)
   # AWS_PROFILE=your-profile-name
   ```

   **Alternative**: You can also set these as environment variables:
   ```bash
   export WHISPER_ENDPOINT_NAME=your-endpoint-name
   export AWS_REGION=your-aws-region
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PortAudio** (required for PyAudio):
   ```bash
   brew install portaudio
   ```

### Step 3: AWS Permissions

Ensure your AWS credentials have the following permissions:
- `sagemaker:InvokeEndpoint` for your Whisper endpoint
- Access to the specific SageMaker endpoint ARN

You can test your endpoint access with:
```bash
aws sagemaker list-endpoints --region your-aws-region
```

### Development Setup

Run the application in development mode:
```bash
python src/main.py
```

### Running the Script in the Background

To run the script in the background:

1. Install all dependencies:
```
pip install -r requirements.txt
```

2. Run the script in the background:
```
nohup ./run.sh >/dev/null 2>&1 & disown
```

3. The script will continue running in the background. You can then use the app as described in the Usage section.

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
- Microphone access (to record your speech).  
  Go to System Preferences → Security & Privacy → Privacy → Microphone and add your Terminal or the app.
- Accessibility access (to simulate keyboard presses for pasting).  
  Go to System Preferences → Security & Privacy → Privacy → Accessibility and add your Terminal or the app.

## Requirements

- macOS 10.14 or later
- Microphone

## Troubleshooting

### Configuration Issues

1. **Check your endpoint configuration**:
   ```bash
   # Verify your endpoint exists and is in service
   aws sagemaker describe-endpoint --endpoint-name your-endpoint-name --region your-aws-region
   ```

2. **Test AWS credentials**:
   ```bash
   aws sts get-caller-identity
   ```

3. **Debug configuration loading**:
   The app will print the endpoint name and region it's using when it starts. Check the console output.

### General Issues

If something goes wrong or you need to stop the background process, you can kill it by running one of the following commands in your Terminal:

1. List the running process(es):
```
ps aux | grep 'src/main.py'
```
2. Kill the process by its PID:
```
kill -9 <PID>
```

### Common Error Messages

- **"SageMaker client not initialized"**: Check your AWS credentials and region configuration
- **"ModelError when calling InvokeEndpoint"**: Verify your endpoint name and that it's in "InService" status
- **"AccessDenied"**: Ensure your AWS credentials have `sagemaker:InvokeEndpoint` permissions
