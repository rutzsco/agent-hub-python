import os
import logging
from typing import Optional


class AgentUtils:
    """Utility class for shared agent functionality and orchestration"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_system_prompt(self, prompt_filename: str) -> str:
        """
        Load system prompt from a text file in the prompts directory
        
        Args:
            prompt_filename: Name of the prompt file (e.g., 'image_analysis_system_prompt.txt')
            
        Returns:
            The content of the prompt file as a string
        """
        try:
            # Get the directory of the agents module
            agents_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_file_path = os.path.join(agents_dir, "prompts", prompt_filename)
            
            with open(prompt_file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            self.logger.error(f"System prompt file not found at {prompt_file_path}")
            # Fallback to a basic prompt
            return "You are an AI assistant designed to help with various tasks."
        except Exception as e:
            self.logger.error(f"Error reading system prompt file: {e}")
            # Fallback to a basic prompt
            return "You are an AI assistant designed to help with various tasks."
    
    def validate_azure_openai_config(self, endpoint: Optional[str], api_key: Optional[str]) -> bool:
        """
        Validate Azure OpenAI configuration
        
        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            
        Returns:
            True if configuration is valid, False otherwise
        """
        if not endpoint or not api_key:
            self.logger.error("Azure OpenAI endpoint and API key must be configured")
            return False
        return True
    
    def log_agent_initialization(self, agent_name: str, config_details: dict) -> None:
        """
        Log agent initialization details
        
        Args:
            agent_name: Name of the agent being initialized
            config_details: Dictionary of configuration details to log
        """
        self.logger.info(f"Initializing {agent_name}")
        for key, value in config_details.items():
            # Mask sensitive information
            if 'key' in key.lower() or 'secret' in key.lower() or 'password' in key.lower():
                masked_value = f"{'*' * (len(str(value)) - 4)}{str(value)[-4:]}" if value else "Not configured"
                self.logger.info(f"  {key}: {masked_value}")
            else:
                self.logger.info(f"  {key}: {value}")
    
    def get_prompt_file_path(self, prompt_filename: str) -> str:
        """
        Get the full path to a prompt file
        
        Args:
            prompt_filename: Name of the prompt file
            
        Returns:
            Full path to the prompt file
        """
        agents_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(agents_dir, "prompts", prompt_filename)
    
    def validate_prompt_file_exists(self, prompt_filename: str) -> bool:
        """
        Check if a prompt file exists
        
        Args:
            prompt_filename: Name of the prompt file
            
        Returns:
            True if file exists, False otherwise
        """
        prompt_path = self.get_prompt_file_path(prompt_filename)
        exists = os.path.exists(prompt_path)
        if not exists:
            self.logger.warning(f"Prompt file does not exist: {prompt_path}")
        return exists
