#!/usr/bin/env python3
import boto3
import json
import base64
import os
from dotenv import load_dotenv
from logger_config import setup_logging

# Load environment variables
load_dotenv()
logger = setup_logging()

class SageMakerClient:
    def __init__(self):
        """Initialize SageMaker runtime client"""
        self.region_name = os.getenv('AWS_REGION', 'us-west-2')
        self.endpoint_name = os.getenv('SAGEMAKER_ENDPOINT_NAME', 'whisper-inference')
        
        # Initialize boto3 client for SageMaker Runtime
        try:
            self.client = boto3.client(
                'sagemaker-runtime',
                region_name=self.region_name,
            )
            logger.info(f"SageMaker client initialized with endpoint: {self.endpoint_name}")
        except Exception as e:
            logger.error(f"Error initializing SageMaker client: {e}")
            self.client = None
    
    def transcribe_audio(self, audio_file_path):
        """
        Send audio file to SageMaker endpoint for transcription.
        Returns the transcribed text.
        """
        if not self.client:
            raise Exception("SageMaker client not initialized")
        
        try:
            # Read the audio file and encode it as base64
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Prepare the request payload
            payload = {
                "audio": audio_base64,
                "task": "transcribe"
            }
            
            # Invoke the SageMaker endpoint
            response = self.client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            # Parse the response
            response_body = response['Body'].read().decode('utf-8')
            result = json.loads(response_body)
            
            # Extract the transcribed text
            if 'text' in result:
                transcribed_text = result['text'].strip()
                logger.debug(f"SageMaker transcription: {transcribed_text}")
                return transcribed_text
            else:
                raise Exception("No text in SageMaker response")
                
        except Exception as e:
            logger.error(f"Error calling SageMaker endpoint: {e}")
            raise
    
    def test_connection(self):
        """Test if SageMaker endpoint is working properly"""
        if not self.client:
            return False, "Client not initialized"
        
        try:
            # Test endpoint availability
            response = self.client.describe_endpoint(EndpointName=self.endpoint_name)
            status = response.get('EndpointStatus', 'Unknown')
            
            if status == 'InService':
                return True, f"Endpoint {self.endpoint_name} is in service"
            else:
                return False, f"Endpoint {self.endpoint_name} status: {status}"
                
        except Exception as e:
            return False, str(e)
    
    def is_available(self):
        """Check if SageMaker client is available and configured"""
        return self.client is not None
    
    def get_endpoint_info(self):
        """Get information about the current endpoint configuration"""
        return {
            'endpoint_name': self.endpoint_name,
            'region': self.region_name,
            'available': self.is_available()
        }
