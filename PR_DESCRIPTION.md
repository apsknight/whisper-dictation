# Add Configurable SageMaker Inference Support

## Overview
This PR adds configurable support for AWS SageMaker inference endpoints alongside the existing local Whisper model, allowing users to choose between local and cloud-based speech-to-text processing.

## Features Added

### 🔧 Configuration Options
- New `WHISPER_INFERENCE_MODE` environment variable (`local` or `sagemaker`)
- `SAGEMAKER_ENDPOINT_NAME` configuration for custom endpoint names
- Backward compatible - defaults to `local` mode if not configured

### 🚀 SageMaker Integration
- New `SageMakerClient` module for endpoint communication
- Automatic endpoint health checking and connection testing
- Base64 audio encoding for SageMaker inference
- Error handling and fallback mechanisms

### 🎯 Seamless Mode Switching
- Runtime detection of inference mode from environment variables
- Status indicators show current mode (Local/SageMaker)
- Unified transcription interface regardless of backend
- Preserves all existing features (text enhancement, microphone selection, etc.)

## Usage

### Local Mode (Default)
```bash
# .env file
WHISPER_INFERENCE_MODE=local
```

### SageMaker Mode
```bash
# .env file
WHISPER_INFERENCE_MODE=sagemaker
SAGEMAKER_ENDPOINT_NAME=your-whisper-endpoint
AWS_REGION=us-west-2
```

## Benefits

- **Flexibility**: Choose between local processing or cloud inference
- **Scalability**: Leverage SageMaker for better performance/accuracy
- **Cost Control**: Use local mode for development, SageMaker for production
- **Zero Breaking Changes**: Existing users continue with local mode seamlessly

## Implementation Details

- Maintains the same audio recording and processing pipeline
- SageMaker client handles base64 encoding and JSON communication
- Error handling ensures graceful fallback and clear status messages
- Logging indicates which inference mode is active

## Testing

- ✅ Code compiles without syntax errors
- ✅ Backward compatibility maintained
- ✅ Configuration parsing works correctly
- ✅ Both inference paths implemented

This enhancement makes the application more versatile for different deployment scenarios while maintaining the simplicity and reliability of the existing codebase.
