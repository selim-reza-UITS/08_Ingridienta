from django.db import models
from django_prose_editor.fields import ProseEditorField

options = ProseEditorField(
    extensions={
        # Core text formatting
        "Bold": True,
        "Italic": True,
        "Strike": True,
        "Underline": True,
        "HardBreak": True,

        # Structure
        "Heading": {
            "levels": [1, 2, 3, 4, 5, 6]  # Only allow h1, h2, h3
        },
        "BulletList": True,
        "OrderedList": True,
        "Blockquote": True,

        # Advanced extensions
        "Link": {
            "enableTarget": True,  # Enable "open in new window"
            "protocols": ["http", "https", "mailto"],  # Limit protocols
        },
        "Table": True,

        # Editor capabilities
        "History": True,       # Enables undo/redo
        "HTML": True,          # Allows HTML view
        "Typographic": True,   # Enables typographic chars
    },
    sanitize=True
)
class PrivacyPolicy(models.Model):
    content = options

    class Meta:
        verbose_name_plural = 'Privacy Policy'

    def __str__(self):
        return "Privacy Policy"

class TermsConditions(models.Model):
    content = options

    class Meta:
        verbose_name_plural = 'Terms & Conditions'

    def __str__(self):
        return "Terms & Conditions"


class AboutUs(models.Model):
    content = options

    class Meta:
        verbose_name_plural = 'About Us'

    def __str__(self):
        return "About Us"

