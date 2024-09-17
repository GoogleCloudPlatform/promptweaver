<!--
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
 -->

PromptWeaver is a Python library that streamlines prompt development and management in Generative AI workflows. It decouples prompts from Python scripts, enhancing portability, maintainability, and scalability for developers working with multiple LLMs or complex prompting workflows.

> This project is currently under active development and may undergo significant changes. We welcome your feedback and contributions!

## Features

- Separate prompts from code for better modularity.
- Supports multimodal input (text, images, audio, video).
- Integration with large language models such as Gemini.
- YAML-based prompt configuration with sample and default values.
- Extensible to support other LLM APIs.

## Installation

PromptWeaver can be easily installed using pip:

```bash
pip install promptweaver
```

> **Note:** PromptWeaver requires Python 3.8 or higher.

## Usage

First, you need to start by creating a `.yml.j2` promptweaver template.

You will find template examples in our [promptweaver gallery](/samples/).

```yaml
name: Hello World
description: A quickstart prompt showcasing how to answer a simple user message using gemini.
model:
  model_name: gemini-1.5-flash-001
  generation_config:
    temperature: 0.3
    max_output_tokens: 250
  system_instruction: You are an AI model trained to answer questions. Be kind and objective in your answers.
# ---
variables:
  user_message:
    sample: Hi!
# ---
user:
  - text: {{ user_message }}
```

Now you can call one of the supported LLM Clientes using the promptweaver template.

```python
from promptweaver.core.prompt_template import PromptConfig
from promptweaver.clients.gemini.gemini_client import GeminiClient

# Initialize the Gemini client
gemini_client = GeminiClient(project="your_project", location="your_location")

# Load the prompt configuration
example_prompt = PromptConfig.from_file_with_sample_values("samples/example.yml.j2")

# Generate content
generate_content = gemini_client.generate_content(example_prompt)
print(generate_content.text)
```

## Contributing

We welcome contributions! Please read our contributing guide for details on how to get started. The project can be found on [GitHub](https://github.com/GoogleCloudPlatform/promptweaver).
