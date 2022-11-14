from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from .models import *


from django import forms


class AnswersInline(NestedTabularInline):
    model = Answers
    can_delete = True
    extra = 1


class QuestionsInline(NestedStackedInline):
    inlines = [AnswersInline]
    model = Questions
    extra=1

class SetsAdmin(NestedModelAdmin):
    inlines = [QuestionsInline]

admin.site.register(Sets, SetsAdmin)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "mark", "checked",)





# @admin.register(Questions)
# class QuestionsAdmin(admin.ModelAdmin):
#     list_display = ("id", "name",)
#     list_display_links = ("name",)