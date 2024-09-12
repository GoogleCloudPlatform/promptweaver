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

from promptweaver.core.content_builder import ContentBuilder
from vertexai.generative_models import Part, Image
from promptweaver.utils.mime_utils import get_mime_type
from promptweaver.utils.string_utils import remove_blank_spaces

class GeminiMultimodalContentBuilder(ContentBuilder):
    def __init__(self):
        self.contents = []

    def build_contents(self, user_data: list) -> list:
        """
        Builds multimodal content specific to Gemini's SDK, ensuring the order of fields is preserved.

        Args:
          user_data (list): Ordered list of user-provided data (as dictionaries).

        Returns:
          list: A list of `Part` objects compatible with Gemini's SDK.
        """
        for entry in user_data:
            # Loop through each dictionary in the user section, ensuring order
            for modality, uri in entry.items():
                if entry.get(modality) == "None":
                    continue
                if uri.startswith("https://storage.googleapis.com/"):
                    uri = uri.replace("https://storage.googleapis.com/", "gs://")
                if modality == 'image':
                    self._add_image(uri)
                elif modality == 'video':
                    self._add_video(uri)
                elif modality == 'audio':
                    self._add_audio(uri)
                elif modality == 'document':
                    self._add_document(uri)
                elif modality == 'text':
                    self.contents.append(remove_blank_spaces(uri))
        
        return self.contents

    def _add_image(self, image_uri: str) -> None:
        if image_uri.startswith("gs://"):  # Check if it's a GCS URI
            mime_type = get_mime_type(image_uri)
            image_part = Part.from_uri(image_uri, mime_type=mime_type)
        else:  # Assume it's a local file path
            image_part = Image.load_from_file(image_uri)
        self.contents.append(image_part)

    def _add_video(self, video_uri: str) -> None:
        mime_type = get_mime_type(video_uri)
        video_part = Part.from_uri(video_uri, mime_type=mime_type)
        self.contents.append(video_part)

    def _add_audio(self, audio_uri: str) -> None:
        mime_type = get_mime_type(audio_uri)
        audio_part = Part.from_uri(audio_uri, mime_type=mime_type)
        self.contents.append(audio_part)

    def _add_document(self, document_uri: str) -> None:
        mime_type = get_mime_type(document_uri)
        document_part = Part.from_uri(document_uri, mime_type=mime_type)
        self.contents.append(document_part)
