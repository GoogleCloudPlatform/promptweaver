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