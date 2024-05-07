import base64

from django.core.files.base import ContentFile
from django.db.models.fields.files import FileField, ImageFieldFile
from rest_framework import serializers

MEDIA_TYPES = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "pdf": "application/pdf",
}


class Base64FileField(serializers.FileField):
    def __init__(self, default_filename: str, *args, **kwargs):
        self.default_filename = default_filename
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        # Verify if the data is a base64 string
        if isinstance(data, str) and data.startswith("data:"):
            header, encoded = data.split(",", 1)
            decoded_file = base64.b64decode(encoded)
            file = ContentFile(decoded_file)

            # If a default filename is provided, set it
            if ";filename" in header:
                filename_start = header.index("filename=") + len("filename=")
                filename_end = header.index(";", filename_start)
                filename = header[filename_start:filename_end]
                filename = filename.strip('"')
                file.name = filename

            else:
                file.name = self.default_filename

            return file
        # If the data is not a base64 string, just return it
        return super().to_internal_value(data)

    def to_representation(self, value):
        if not value:
            return None

        valid_types = (ContentFile, ImageFieldFile, FileField)

        if isinstance(value, valid_types):
            content = value.read()
            encoded_content = base64.b64encode(content).decode("utf-8")
            filename = value.name
            file_extension = filename.split(".")[-1]
            media_type = MEDIA_TYPES.get(
                file_extension, "application/octet-stream"
            )
            base64_representation = (
                f"data:{media_type};base64,{encoded_content}"
            )
            return base64_representation
        # If the value is not a ContentFile, just return it
        return super().to_representation(value)
