from django.db import models
from django.contrib.auth.models import User
import uuid


class Document(models.Model):
    STATUS_CHOICES = [
        ("uploaded", "Uploaded"),
        ("processing", "Processing"),
        ("done", "Done"),
        ("error", "Error"),
    ]

    FILE_TYPE_CHOICES = [
        ("pdf", "PDF"),
        ("jpg", "JPG"),
        ("png", "PNG"),
        ("docx", "DOCX"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    file_url = models.URLField(blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="uploaded")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name

        if self.file and not self.file_url:
            self.file_url = self.file.url if hasattr(self.file, "url") else ""

        if self.file and not self.file_type:
            ext = self.file.name.split(".")[-1].lower()
            if ext in ["pdf", "jpg", "png", "docx"]:
                self.file_type = ext

        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name


class Processing(models.Model):
    STATUS_CHOICES = [
        ("processing", "Processing"),
        ("done", "Done"),
        ("error", "Error"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="processing")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Processing for {self.document.file_name}"


class ExtractedData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="extracted_data_record")
    data = models.JSONField(default=dict)
    raw_text = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ExtractedData for {self.document.file_name}"


class Risk(models.Model):
    TYPE_CHOICES = [
        ("ownership", "Ownership"),
        ("cadastral", "Cadastral"),
        ("financial", "Financial"),
        ("legal", "Legal"),
        ("other", "Other"),
    ]

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="risks")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="other")
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="low")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} risk for {self.document.file_name}"


class Analytics(models.Model):
    PERIOD_CHOICES = [
        ("day", "Day"),
        ("week", "Week"),
        ("month", "Month"),
        ("year", "Year"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analytics", null=True, blank=True)
    total_documents = models.PositiveIntegerField(default=0)
    processed_documents = models.PositiveIntegerField(default=0)
    detected_risks = models.PositiveIntegerField(default=0)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="month")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics ({self.period})"