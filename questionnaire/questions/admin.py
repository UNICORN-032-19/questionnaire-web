from django.contrib import admin
from django import forms
from .models import Questions
from .widgets import CustomTextarea
from django.db import models


class QuestionsAdminForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ("text", "multiple_answers", "tags", )


class QuestionsAdmin(admin.ModelAdmin):
    form = QuestionsAdminForm
    formfield_overrides = {
        models.TextField: {'widget': CustomTextarea},
    }


admin.site.register(Questions, QuestionsAdmin)
