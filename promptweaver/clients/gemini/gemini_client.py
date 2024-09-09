"""
 Copyright 2024 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

from promptweaver.core.base_llm_client import BaseLLMClient
from promptweaver.core.prompt_template import PromptConfig
from promptweaver.clients.gemini.multimodal_content_builder import GeminiMultimodalContentBuilder
from vertexai.generative_models import (
    GenerativeModel, GenerationConfig, SafetySetting,
    HarmCategory, HarmBlockThreshold
)

import vertexai 


class GeminiClient(BaseLLMClient):
    def __init__(self, project: str, location: str):
        """
        Initializes the Gemini client with the given project and location.

        Args:
            project (str): The project ID for Gemini.
            location (str): The location for the Gemini deployment.
        """
        vertexai.init(project=project, location=location)
    
    def generate_content(self, prompt_config: PromptConfig, verbose: bool = False) -> str:
        """
        Generates content using Gemini API based on the provided PromptConfig.

        Args:
            prompt_config (PromptConfig): The configuration for the prompt.
            verbose (bool): Whether to print verbose information.

        Returns:
            str: The generated content from Gemini.
        """
        model = GenerativeModel(
            model_name=prompt_config.model_name,
            system_instruction=[prompt_config.system_instruction] if prompt_config.system_instruction else [],
        )

        prompt = self._build_prompt(prompt_config.user)
        if verbose:
            print(f"Prompt: {prompt}")

        response = model.generate_content(
            contents=prompt,
            generation_config=GenerationConfig(**prompt_config.generation_config),
            safety_settings=self._get_safety_settings(prompt_config.safety_settings),
        )

        return response

    def validate_prompt(self, prompt_config: PromptConfig) -> bool:
        """
        Validates the prompt configuration for Gemini.

        Args:
            prompt_config (PromptConfig): The configuration for the prompt.

        Returns:
            bool: True if valid, False otherwise.
        """
        required_fields = ['model_name', 'system_instruction', 'generation_config', 'user']
        for field in required_fields:
            if not getattr(prompt_config, field, None):
                return False
        return True

    def _build_prompt(self, user_data: list) -> list:
        """
        Helper function to build the prompt string from user data.
        
        Args:
            user_data (list): User data containing text, image, audio, etc.
        
        Returns:
            list: Constructed prompt.
        """
        # Initialize the multimodal content builder
        builder = GeminiMultimodalContentBuilder()
        return builder.build_contents(user_data)

    def _get_safety_settings(self, safety_settings_config: list) -> list:
        """
        Converts safety settings from the config to Gemini SafetySetting objects.
        
        Args:
            safety_settings_config (list): List of safety settings.
        
        Returns:
            list: List of SafetySetting objects for Gemini.
        """
        safety_settings = []
        for setting in safety_settings_config:
            safety_settings.append(
                SafetySetting(
                    category=getattr(HarmCategory, setting['category']),
                    method=getattr(SafetySetting.HarmBlockMethod, setting['method']),
                    threshold=getattr(HarmBlockThreshold, setting['threshold'])
                )
            )
        return safety_settings
