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

from typing import Dict, Any, Set, Tuple
import re
import yaml
from jinja2 import Template, UndefinedError, Environment, meta
from promptweaver.utils.string_utils import remove_blank_spaces


class YAMLParser:
    @staticmethod
    def load_and_render_template(file_path: str, params: Dict[str, str]) -> str:
        """
        Loads and renders the .yml.j2 template using the provided parameters.

        Args:
            file_path (str): The path to the .yml.j2 file.
            params (Dict[str, str]): Parameters to use for rendering the template.

        Returns:
            str: The rendered YAML content as a string.
        """
        with open(file_path, 'r') as file:
            template_str = file.read()
        template = Template(template_str)
        try:
            return template.render(**params)
        except UndefinedError as e:
            raise ValueError(f"Missing parameters for rendering: {e}")

    @staticmethod
    def get_variables(file_path: str) -> Dict[str, str]:
        """
        Extracts the 'variables' section from the .yml.j2 template.

        Args:
            file_path (str): The path to the .yml.j2 file.
        """
        with open(file_path, 'r') as file:
            raw_yaml = file.read()
        match = re.search(r"variables:\s*(\n(?:[ \t]+.*\n?)*)", raw_yaml)
        if match:
            variables_section = match.group(1)
        else:
            print("Variables section not found.")
        return YAMLParser.parse_rendered_yaml(variables_section)

    @staticmethod
    def get_sample_values(file_path: str) -> Dict[str, str]:
        """
        Extracts sample values from the 'variables' section.

        Args:
            file_path (str): The path to the .yml.j2 file.

        Returns:
            Dict[str, str]: A dictionary of variable names and their sample values.
        """        
        variables_section = YAMLParser.get_variables(file_path)
        return {var: details['sample'] for var, details in variables_section.items() if 'sample' in details}

    @staticmethod
    def get_default_values(file_path: str) -> Dict[str, str]:
        """
        Extracts default variables from the 'variables' section.

        Args:
            variables_section (Dict[str, Dict[str, str]]): The 'variables' section of the YAML.

        Returns:
            Dict[str, str]: A dictionary of variable names and their default values.
        """
        variables_section = YAMLParser.get_variables(file_path)
        return {var: details.get('default') for var, details in variables_section.items() if 'default' in details}

    @staticmethod
    def extract_required_variables(template_str: str) -> Set[str]:
        """
        Extracts all the variables used in the Jinja2 template.
        """
        env = Environment()
        parsed_content = env.parse(template_str)
        return meta.find_undeclared_variables(parsed_content)

    @staticmethod
    def parse_rendered_yaml(rendered_yaml: str) -> Dict[str, Any]:
        """
        Parses the rendered YAML string.

        Args:
            rendered_yaml (str): The rendered YAML content.

        Returns:
            Dict[str, Any]: Parsed YAML data.
        """
        return yaml.safe_load(rendered_yaml)

    @staticmethod
    def load_config(file_path: str, params: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Loads, renders, and parses the YAML configuration from a .yml.j2 file.

        Args:
            file_path (str): The path to the .yml.j2 file.
            params (Dict[str, str]): Parameters to use for rendering the template.

        Returns:
            Dict[str, Any]: Parsed YAML data after rendering.
            Dict[str, str]: The parameters used for rendering the template.
        """
        # Get the default values for variables
        default_values = YAMLParser.get_default_values(file_path)

        # Merge provided params with default values (params override defaults)
        merged_params = {**default_values, **params}

        # Render the template with merged params
        rendered_yaml = YAMLParser.load_and_render_template(file_path, merged_params)
        parsed_yaml = YAMLParser.parse_rendered_yaml(rendered_yaml)
        return (parsed_yaml, merged_params)

    @staticmethod
    def load_config_with_sample_values(file_path: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Loads, renders, and parses the YAML configuration from a .yml.j2 file
        using the sample values provided in the variables section.

        Args:
            file_path (str): The path to the .yml.j2 file.

        Returns:
            Dict[str, Any]: Parsed YAML data after rendering with sample values.
            Dict[str, str]: The parameters used for rendering the template.
        """
        sample_config = YAMLParser.get_sample_values(file_path)
        parsed_yaml, merged_params = YAMLParser.load_config(file_path, sample_config)
        return (parsed_yaml, merged_params)


def extract_variables_from_template(template_str: str) -> Set[str]:
    """
    Extracts all the variables used in the Jinja2 template.

    Args:
        template_str (str): The Jinja2 template as a string.

    Returns:
        Set[str]: A set of all variable names used in the template.
    """
    env = Environment()
    parsed_content = env.parse(template_str)
    return meta.find_undeclared_variables(parsed_content)


class PromptConfig:
    """
    Represents the configuration for the LLM prompt, loaded from a .yml.j2 file.

    Attributes:
        name (str): Name of the prompt.
        description (str): Description of the prompt.
        model_name (str): Name of the model to use.
        generation_config (Dict[str, Any]): Configuration options for the model generation.
        system_instruction (str): Instruction for the LLM's system behavior.
        sample (Dict[str, Any]): Sample values for rendering the template.
    """

    def __init__(self, config_data: Dict[str, Any], provided_variables: Dict[str, str], verbose: bool = False) -> None:
        """
        Initializes the PromptConfig.

        Args:
            config_data (Dict[str, Any]): The parsed YAML configuration.
            provided_params (Dict[str, str]): The dictionary of provided parameters.
            verbose (bool): Whether to print verbose information.

        Raises:
            ValueError: If any required parameter is missing.
        """
        self.name = config_data.get('name', '')
        self.description = config_data.get('description', '')
        self.model_name = config_data.get('model', {}).get('model_name', '')
        self.generation_config = config_data.get('model', {}).get('generation_config', {})
        self.safety_settings = config_data.get('model', {}).get('safety_settings', [])
        self.system_instruction = remove_blank_spaces(config_data.get('model', {}).get('system_instruction', ''))
        self.variables = config_data.get('variables', {})
        self.provided_variables = provided_variables
        self.user = config_data.get('user', [])

        # Validate user section
        self.validate_user_section()

        if verbose:
            print(self)


    def validate_user_section(self) -> None:
        """
        Validates that at least one input modality (text, image, audio video or document)
        is provided in the user section. Ensures that the 'user' list contains at
        least one valid modality dictionary.
        """
        user_data = self.user
        modalities = ['text', 'image', 'audio', 'video', 'document']
        
        # Track whether any valid modality is provided
        provided_modalities = []
        
        # Loop through the user list (each entry is a dictionary with one modality)
        for entry in user_data:
            for modality, value in entry.items():
                if modality in modalities and value:
                    provided_modalities.append(modality)

        # If no valid modalities were found, raise an exception
        if not provided_modalities:
            raise ValueError("At least one input modality (text, image, audio, or video) must be provided in the user section.")

    @classmethod
    def from_file(cls, file_path: str, params: Dict[str, str], verbose: bool = False) -> 'PromptConfig':
        """
        Creates a PromptConfig instance from a .yml.j2 file using provided params.

        Args:
            file_path (str): The path to the .yml.j2 file.
            params (Dict[str, str]): Parameters to use for rendering the template.
            verbose (bool): Whether to print verbose information.

        Returns:
            PromptConfig: An instance of the PromptConfig class.
        """
        config_data, merged_params = YAMLParser.load_config(file_path, params)
        return cls(config_data, merged_params, verbose)

    @classmethod
    def from_file_with_sample_values(cls, file_path: str, verbose: bool = False) -> 'PromptConfig':
        """
        Creates a PromptConfig instance from a .yml.j2 file using sample values.

        Args:
            file_path (str): The path to the .yml.j2 file.
            verbose (bool): Whether to print verbose information.

        Returns:
            PromptConfig: An instance of the PromptConfig class.
        """
        config_data, merged_params = YAMLParser.load_config_with_sample_values(file_path)
        return cls(config_data, merged_params, verbose)
    
    def __str__(self) -> str:
        """Returns a string representation of the PromptConfig object."""
        return (
        "\nPromptConfig(\n"
        f"  name='{self.name}',\n"
        f"  description='{self.description}',\n"
        f"  model_name='{self.model_name}',\n"
        f"  generation_config={self.generation_config},\n"
        f"  safety_settings={self.safety_settings},\n"
        f"  system_instruction='{self.system_instruction}',\n"
        f"  variables={self.variables},\n"
        f"  provided_variables={self.provided_variables},\n"
        ")\n"
    )
