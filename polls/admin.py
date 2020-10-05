"""The class for adjust admin web-page."""
from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Class for adjust the choice section in admin page."""

    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    """Class for adjust the Question section in admin page."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'end_date',
                    'was_published_recently')
    list_filter = ('pub_date', 'end_date')
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
