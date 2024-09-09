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

from abc import ABC, abstractmethod
from promptweaver.core.prompt_template import PromptConfig

class BaseLLMClient(ABC):
    @abstractmethod
    def generate_content(self, prompt_config: PromptConfig) -> str:
        """
        Abstract method for generating content based on the provided PromptConfig.

        Args:
            prompt_config (PromptConfig): The configuration for the prompt.
        
        Returns:
            str: The generated content from the LLM.
        """
        pass

    @abstractmethod
    def validate_prompt(self, prompt_config: PromptConfig) -> bool:
        """
        Validates the prompt configuration to ensure it adheres to the requirements of the LLM.

        Args:
            prompt_config (PromptConfig): The configuration for the prompt.

        Returns:
            bool: True if valid, False otherwise.
        """
        pass
