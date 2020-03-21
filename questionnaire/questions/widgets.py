from django.forms.widgets import Textarea

class CustomTextarea(Textarea):
    template_name = 'admin/custom_textarea.html'


class QuestionWidget(Textarea):
	template_name = 'admin/custom_textarea.html'
