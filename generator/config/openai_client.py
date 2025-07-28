#!/usr/bin/env python3
"""
OpenAI-compatible client for OpenRouter API

Provides a unified interface for OpenAI-compatible models through OpenRouter.
Supports the environment variables the user has configured:
- OPENROUTER_API_BASE_URL
- OPENROUTER_API_KEY  
- OPENROUTER_MODEL
"""

import os
import requests
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ChatMessage:
    """Represents a chat message"""
    role: str  # 'system', 'user', 'assistant'
    content: str

@dataclass
class GenerationConfig:
    """Configuration for text generation"""
    temperature: float = 0.7
    max_tokens: int = 4000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[List[str]] = None

class OpenRouterClient:
    """OpenAI-compatible client for OpenRouter API"""
    
    def __init__(self):
        # Ensure base URL doesn't include /chat/completions
        base_url = os.getenv('OPENROUTER_API_BASE_URL', 'https://openrouter.ai/api/v1')
        self.api_base_url = base_url.rstrip('/chat/completions').rstrip('/')
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.model = os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o')
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://localhost:8080',  # Optional, for rankings
            'X-Title': 'Store Generator'  # Optional, for rankings
        }
    
    def chat_completion(
        self, 
        messages: List[ChatMessage], 
        config: Optional[GenerationConfig] = None
    ) -> Dict[str, Any]:
        """
        Create a chat completion using OpenRouter API
        
        Args:
            messages: List of chat messages
            config: Generation configuration
            
        Returns:
            API response dictionary
        """
        if config is None:
            config = GenerationConfig()
        
        # Convert messages to API format
        api_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        payload = {
            "model": self.model,
            "messages": api_messages,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty
        }
        
        if config.stop:
            payload["stop"] = config.stop
        
        try:
            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API request failed: {str(e)}")
    
    def generate_text(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> str:
        """
        Generate text from a prompt
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            config: Generation configuration
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append(ChatMessage(role="system", content=system_prompt))
        
        messages.append(ChatMessage(role="user", content=prompt))
        
        response = self.chat_completion(messages, config)
        
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {str(e)}")
    
    def generate_structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output
        
        Args:
            prompt: User prompt
            schema: Expected JSON schema
            system_prompt: Optional system prompt
            config: Generation configuration
            
        Returns:
            Parsed JSON response
        """
        # Add JSON formatting instruction to prompt
        json_prompt = f"""
{prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Respond ONLY with the JSON, no additional text.
"""
        
        if system_prompt:
            system_prompt += "\n\nAlways respond with valid JSON format."
        else:
            system_prompt = "You are a helpful assistant that responds with valid JSON format."
        
        response_text = self.generate_text(json_prompt, system_prompt, config)
        
        try:
            # Try to extract JSON from response
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text.strip())
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}\nResponse: {response_text}")
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List available models from OpenRouter
        
        Returns:
            List of model information
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/models",
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json().get('data', [])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to list models: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to OpenRouter API
        
        Returns:
            True if connection is successful
        """
        try:
            response = self.generate_text(
                "Hello! Please respond with 'OK' to confirm the connection.",
                config=GenerationConfig(max_tokens=10, temperature=0.1)
            )
            return "OK" in response.upper()
            
        except Exception:
            return False

# Global client instance
_client: Optional[OpenRouterClient] = None

def get_openai_client() -> OpenRouterClient:
    """Get the global OpenRouter client instance"""
    global _client
    if _client is None:
        _client = OpenRouterClient()
    return _client

def test_openai_setup() -> Dict[str, Any]:
    """
    Test the OpenAI setup and return configuration info
    
    Returns:
        Dictionary with setup information and test results
    """
    try:
        client = get_openai_client()
        
        # Test connection with detailed debugging
        print(f"Testing connection to: {client.api_base_url}/chat/completions")
        print(f"Using model: {client.model}")
        
        try:
            # Simple test message
            test_response = client.generate_text(
                "Respond with only 'OK' to confirm connection.",
                config=GenerationConfig(max_tokens=5, temperature=0.1)
            )
            connection_ok = "OK" in test_response.upper()
            print(f"Test response: {test_response}")
        except Exception as test_error:
            print(f"Connection test failed: {test_error}")
            connection_ok = False
        
        # Get model info
        try:
            models = client.list_models()
            available_models = [m.get('id', 'unknown') for m in models[:5]]  # First 5 models
        except Exception as model_error:
            print(f"Failed to list models: {model_error}")
            available_models = []
        
        return {
            "status": "success" if connection_ok else "connection_failed",
            "api_base_url": client.api_base_url,  # Show base URL, not full URL
            "model": client.model,
            "api_key_configured": bool(client.api_key),
            "connection_test": connection_ok,
            "sample_models": available_models
        }
        
    except Exception as e:
        print(f"Setup error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "api_key_configured": bool(os.getenv('OPENROUTER_API_KEY')),
            "connection_test": False
        }

if __name__ == "__main__":
    # Test the setup
    print("Testing OpenRouter API setup...")
    
    setup_info = test_openai_setup()
    print(f"Status: {setup_info['status']}")
    print(f"Model: {setup_info.get('model', 'Not configured')}")
    print(f"API Key: {'✓ Configured' if setup_info['api_key_configured'] else '✗ Missing'}")
    print(f"Connection: {'✓ OK' if setup_info['connection_test'] else '✗ Failed'}")
    
    if setup_info.get('sample_models'):
        print(f"Sample available models: {', '.join(setup_info['sample_models'])}")
    
    if setup_info['status'] == 'success':
        print("\n✅ OpenRouter API is ready for use!")
    else:
        print(f"\n❌ Setup issue: {setup_info.get('error', 'Connection failed')}") 