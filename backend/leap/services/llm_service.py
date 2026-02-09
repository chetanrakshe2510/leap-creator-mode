import logging
from typing import Dict, Type, TypeVar
from openai import OpenAI
import instructor
from pydantic import BaseModel
import os

from leap.core.config import OPENAI_MODEL
from leap.workflow.tracing import traceable  # Import the traceable decorator

T = TypeVar('T', bound=BaseModel)

class LLMService:
    """Service for interacting with language models."""
    
    def __init__(self, model: str = OPENAI_MODEL):
        """Initialize the LLM service.
        
        Args:
            model: The OpenAI model to use
        """
        self.model = model
        self.client = instructor.from_openai(OpenAI())
        self.logger = logging.getLogger("leap")
    
    @traceable(run_type="llm", tags=["llm", "structured"])
    def generate_structured_response(
        self, 
        system_content: str,
        user_content: str,
        response_model: Type[T]
    ) -> T:
        """Generate a structured response using the LLM.
        
        Args:
            system_content: The system message content
            user_content: The user message content
            response_model: The Pydantic model to structure the response
            
        Returns:
            The structured response
        """
        self.logger.info(f"Generating structured response with model: {self.model}")
        
        response = self.client.chat.completions.create(
            model=self.model,
            response_model=response_model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
        )
        
        return response
        
    @traceable(run_type="llm", tags=["llm", "chat"])
    def chat(self, prompt: str, system_message: str = "You are a helpful assistant.") -> Dict[str, str]:
        """Generate a simple text response using the LLM.
        
        Args:
            prompt: The user prompt
            system_message: Optional system message
            
        Returns:
            A dictionary containing the response content
        """
        self.logger.info(f"Generating chat response with model: {self.model}")
        
        client = OpenAI()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {"content": response.choices[0].message.content} 