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


class ContentBuilder(ABC):
    @abstractmethod
    def build_contents(self, user_data: dict) -> list:
        """
        Constructs and returns a list of content parts based on user data.

        Args:
            user_data (dict): User-provided data containing various modalities.

        Returns:
            list: A list of content parts compatible with the LLM's SDK.
        """
        pass
