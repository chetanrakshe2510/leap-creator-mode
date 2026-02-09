"""
Base classes and utilities for prompt management.
"""

from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field
from enum import Enum
import json
import os
from pathlib import Path


class PromptVersion(str, Enum):
    """Enum for prompt versions."""
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"
    V4 = "v4"
    EXPERIMENTAL = "experimental"
    PRODUCTION = "production"
    

class PromptTemplate(BaseModel):
    """Base class for prompt templates."""
    system: str = Field(..., description="System message content")
    user: str = Field(..., description="User message template with placeholders")
    version: PromptVersion = Field(default=PromptVersion.V1, description="Version of this prompt")
    description: Optional[str] = Field(None, description="Description of what this prompt does")
    tags: List[str] = Field(default_factory=list, description="Tags for categorizing prompts (optional)")
    
    def format(self, **kwargs) -> Dict[str, str]:
        """
        Format the prompt template with the provided values.
        
        Args:
            **kwargs: Values to fill in the template placeholders
            
        Returns:
            Dict with formatted system and user messages
        """
        try:
            formatted_system = self.system.format(**kwargs)
            formatted_user = self.user.format(**kwargs)
            return {
                "system": formatted_system,
                "user": formatted_user
            }
        except KeyError as e:
            missing_key = str(e).strip("'")
            raise ValueError(f"Missing required parameter: {missing_key}")
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the template to a dictionary."""
        return self.model_dump()
    
    def to_json(self) -> str:
        """Convert the template to a JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "PromptTemplate":
        """Create a template from a JSON string."""
        data = json.loads(json_str)
        return cls(**data)
    
    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> "PromptTemplate":
        """Load a template from a JSON file."""
        with open(file_path, 'r') as f:
            return cls.from_json(f.read())


class PromptCollection:
    """Collection of prompt templates with version management."""
    
    def __init__(self, templates: Dict[PromptVersion, PromptTemplate]):
        self.templates = templates
        
    def get(self, version: Optional[PromptVersion] = None) -> PromptTemplate:
        """
        Get a prompt template by version.
        
        Args:
            version: The version to retrieve. If None, returns the production version.
            
        Returns:
            The prompt template
            
        Raises:
            KeyError: If the requested version doesn't exist
        """
        if version is None:
            version = PromptVersion.PRODUCTION
            
        if version not in self.templates:
            raise KeyError(f"Prompt version {version} not found")
            
        return self.templates[version]
    
    def add(self, version: PromptVersion, template: PromptTemplate) -> None:
        """Add a new template version."""
        self.templates[version] = template
        
    def list_versions(self) -> List[PromptVersion]:
        """List all available versions."""
        return list(self.templates.keys())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the collection to a dictionary."""
        return {
            version.value: template.to_dict() 
            for version, template in self.templates.items()
        }
    
    def to_json(self) -> str:
        """Convert the collection to a JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptCollection":
        """Create a collection from a dictionary."""
        templates = {
            PromptVersion(version): PromptTemplate(**template_data)
            for version, template_data in data.items()
        }
        return cls(templates)
    
    @classmethod
    def from_json(cls, json_str: str) -> "PromptCollection":
        """Create a collection from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> "PromptCollection":
        """Load a collection from a JSON file."""
        with open(file_path, 'r') as f:
            return cls.from_json(f.read()) 