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

import os


def get_mime_type(file_uri: str) -> str:
    """
    Determines the MIME type based on the file extension.

    Args:
        file_uri (str): The URI of the file.

    Returns:
        str: The corresponding MIME type.
    """
    extension = os.path.splitext(file_uri)[1].lower()
    mime_types = {
        '.png': 'image/png',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.flv': 'video/x-flv',
        '.mov': 'video/mov',
        '.mpeg': 'video/mpeg',
        '.mpg': 'video/mpg',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.wmv': 'video/wmv',
        '.3gpp': 'video/3gpp',
        '.aac': 'audio/aac',
        '.flac': 'audio/flac',
        '.mp3': 'audio/mp3',
        '.m4a': 'audio/m4a',
        '.opus': 'audio/opus',
        '.pcm': 'audio/pcm',
        '.wav': 'audio/wav',
        '.pdf': 'application/pdf'
    }
    return mime_types.get(extension, 'application/octet-stream')
