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

import re


def remove_blank_spaces(text: str) -> str:
    """Removes leading and trailing whitespace characters from a string.

    This function uses regular expressions to remove any combination of spaces, 
    tabs, and newlines at the beginning and end of the input string.

    Args:
        text (str): The input string to remove whitespace from.

    Returns:
        str: The input string with leading and trailing whitespace removed.
    """
    return re.sub(r"^\s+|\s+$", "", text)

def add_indent_filters(template_lines: list[str]) -> str:
    """
    Processes a list of lines from a Jinja2 template and adds the `indent` filter
    to any Jinja2 variables inside YAML block scalars to ensure proper indentation
    when rendering variables containing special characters or newlines.

    This function looks for lines within block scalars (indicated by `|` in YAML)
    and adds the `indent` filter to Jinja2 variables found within those blocks.
    
    Args:
        template_lines (list[str]): The lines of the Jinja2 template.

    Returns:
        str: The processed template as a single string with indent filters added to variables.
    """
    in_block_scalar = False
    block_scalar_indent = None
    output_lines = []
    variable_pattern = re.compile(r'{{\s*(.*?)\s*}}')

    for _, line in enumerate(template_lines):
        # Get current indentation level
        current_indent = len(line) - len(line.lstrip(' '))
        stripped_line = line.strip()

        # Check if line ends with '|' and not inside a block scalar
        if stripped_line.endswith('|') and not in_block_scalar:
            in_block_scalar = True
            block_scalar_indent = current_indent
            output_lines.append(line)
            continue

        if in_block_scalar:
            # Check if we've exited the block scalar
            if current_indent <= block_scalar_indent and stripped_line != '':
                # Exited block scalar
                in_block_scalar = False
                block_scalar_indent = None
                output_lines.append(line)
                continue
            else:
                # We are inside the block scalar
                # Check for Jinja2 variable
                def repl(m):
                    var_content = m.group(1)
                    # Check if variable already has an indent filter
                    if '| indent(' not in m.group(0):
                        # Add indent filter with correct indentation
                        return '{{ ' + var_content + ' | indent(' + str(current_indent) + ') }}'
                    else:
                        return m.group(0)
                # Replace variables with indent filter
                new_line = variable_pattern.sub(repl, line)
                output_lines.append(new_line)
                continue
        else:
            # Not inside block scalar
            output_lines.append(line)

    return ''.join(output_lines)
