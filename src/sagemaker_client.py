#!/usr/bin/env python3
import boto3
import json
import os
from dotenv import load_dotenv
from logger_config import setup_logging

load_dotenv()
logger = setup_logging()

class SageMakerClient:
    def __init__(self):
        self.region_name = os.getenv('AWS_REGION', 'us-west-2')
        self.endpoint_name = os.getenv('SAGEMAKER_ENDPOINT_NAME', 'whisper-inference')
        
        try:
            self.client = boto3.client('sagemaker-runtime', region_name=self.region_name)
            logger.info(f"SageMaker client initialized with endpoint: {self.endpoint_name}")
        except Exception as e:
            logger.error(f"Error initializing SageMaker client: {e}")
            self.client = None
    
    def transcribe_audio(self, audio_file_path):
        if not self.client:
            raise Exception("SageMaker client not initialized")
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                audio_hex = audio_file.read().hex()
            
            payload = {
                "audio_input": audio_hex,
                "task": "transcribe",
                "language": "english"
            }
            
            response = self.client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            response_body = response['Body'].read().decode('utf-8')
            result = json.loads(response_body)
            
            if 'text' in result:
                text_data = result['text']
                if isinstance(text_data, list):
                    transcribed_text = ''.join(text_data).strip()
                else:
                    transcribed_text = str(text_data).strip()
                return transcribed_text
            else:
                raise Exception("No text in SageMaker response")
                
        except Exception as e:
            logger.error(f"Error calling SageMaker endpoint: {e}")
            raise
    
    def is_available(self):
        return self.client is not None
