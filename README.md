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

# promptweaver

promptweaver is a Python library that streamlines prompt development and management in Generative AI workflows. It decouples prompts from Python scripts, enhancing portability, maintainability, and scalability for developers working with multiple LLMs or complex prompting workflows.

## Features

- Separate prompts from code for better modularity.
- Supports multimodal input (text, images, audio, video).
- Integration with large language models such as Gemini.
- YAML-based prompt configuration with sample and default values.
- Extensible to support other LLM APIs.

## Installation

You can install promptweaver via pip:

```bash
pip install promptweaver
```

## Usage

First, you need to start by creating a `.yml.j2` promptweaver template.

You will find template examples in our [promptweaver gallery](/tests/prompts/).

```yaml
name: Quickstart
description: A hello worlds prompt.
model:
  model_name: gemini-1.5-flash-001
  generation_config:
    temperature: 0.0
  safety_settings:
    - category: HARM_CATEGORY_DANGEROUS_CONTENT
      method: PROBABILITY
      threshold: BLOCK_LOW_AND_ABOVE
variables:
  character_name:
    sample: Lorem Ipsum
    default: Dolor Sit Amet
  user_message:
    sample: Hello world!
user:
  - text: |
      Now you need to answer the following question from the user: {{ user_message }}
```

Now you can call one of the supported LLM Clientes using the promptweaver template.

```python
from promptweaver.core.prompt_template import PromptConfig
from promptweaver.clients.gemini.gemini_client import GeminiClient

# Initialize the Gemini client
gemini_client = GeminiClient(project="your_project", location="your_location")

# Load the prompt configuration
example_prompt = PromptConfig.from_file_with_sample_values("tests/prompts/example.yml.j2")

# Generate content
generate_content = gemini_client.generate_content(example_prompt)
print(generate_content.text)
```


## Contributing

We welcome contributions! Please read our contributing guide for details on how to get started.

## Project Structure
```
promptweaver/
├── promptweaver/
│  ├── core/
│  │  ├── prompt_template.py
│  │  ├── base_llm_client.py
│  │  └── content_builder.py
│  ├── clients/
│  │  ├── gemini/
│  │  │  ├── gemini_client.py
|  |  |  └── multimodal_content_builder.py
│  ├── utils/
│  │  ├── mime_utils.py
│  │  └── string_utils.py
├── tests/
│  ├── prompts/
│  │  └── example.yml.j2
│  └── test_common.py
├── data/
│  ├── images/
|  |  └── ...
├── .gitignore
├── example_call.py
└── README.md
└── requirements.txt
```

## Roadmap
- Support for additional LLM clients.
- Expanded multimodal input options to support local audios, videos, and documents.
- Improved error handling and custom exception classes.
- Test coverage.
- Performance optimizations for large-scale usage.
- Support for LLM App evaluation templates.