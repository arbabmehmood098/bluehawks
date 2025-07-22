from django.contrib import admin
from .models import ContactSubmission
from firebase_admin import firestore
from django.db import models

# Register your models here.

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "submitted_at")
    search_fields = ("name", "email", "phone", "city", "message")
    list_filter = ("submitted_at",)
    readonly_fields = ("submitted_at",)

class FirebaseContactAdmin(admin.ModelAdmin):
    change_list_template = 'admin/firebase_contact_changelist.html'
    model = None  # Not a real model

    def changelist_view(self, request, extra_context=None):
        db = firestore.client()
        contacts = db.collection('contact_submissions').order_by('submitted_at', direction=firestore.Query.DESCENDING).stream()
        contact_list = []
        for doc in contacts:
            data = doc.to_dict()
            contact_list.append(data)
        extra_context = extra_context or {}
        extra_context['contact_list'] = contact_list
        return super().changelist_view(request, extra_context=extra_context)

class DummyContactModel(models.Model):
    class Meta:
        verbose_name = 'Firebase Contact Submission'
        verbose_name_plural = 'Firebase Contact Submissions'
        app_label = 'mainwebsite'
        managed = False

admin.site.register(DummyContactModel, FirebaseContactAdmin)

# Note: Create the template at 'mainwebsite/templates/admin/firebase_contact_changelist.html' for the custom Firebase contact admin view.
