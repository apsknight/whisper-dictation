#!/usr/bin/env python3
"""
Simple configuration loader for environment variables
"""
import os

def load_config():
    """Load configuration from config.env file if it exists"""
    config_file = os.path.join(os.path.dirname(__file__), '..', 'config.env')
    
    if os.path.exists(config_file):
        print(f"Loading configuration from {config_file}")
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    else:
        print(f"Configuration file {config_file} not found, using environment variables or defaults")

if __name__ == "__main__":
    load_config()
