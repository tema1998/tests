from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from .forms import *
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

# class BillForm(forms.ModelForm):
#     class Meta:
#         model = Questions
#         fields = '__all__'
#     def clean(self):
#         if self.name == '123':
#             raise ValidationError(_('123 нельзя!'))
        # if self.status == 'draft' and self.pub_date is not None:
        #     raise ValidationError(_('Draft entries may not have a publication date.'))
        # # Set the pub_date for published items if it hasn't been set already.
        # if self.status == 'published' and self.pub_date is None:
        #     self.pub_date = datetime.date.today()

class AnswerOptionsInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        answers_yesno = []
        for form in self.forms:
            if not form.is_valid():
                return  # Проверка на другие ошибки формы
            if form.cleaned_data and not form.cleaned_data.get("DELETE"): #Если все ок и поле НЕ УДАЛЯЕТСЯ!
                print(form.cleaned_data)
                answers_yesno.append(form.cleaned_data.get("IsTrue")) #составляем список TRUE and FALSE для всех ответов

        if answers_yesno:  # проверяем по списку все true или не все
            if all(answers_yesno):
                raise ValidationError("Not every answer can be 'yes'")
            if not any(answers_yesno):
                raise ValidationError("Not every answer can be 'no'")



class AnswersInline(NestedTabularInline):
    model = Answers
    can_delete = True
    extra = 1
    formset = AnswerOptionsInlineFormSet


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