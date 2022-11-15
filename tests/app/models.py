from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Sets(models.Model):
    name = models.CharField("Наборы", max_length=150)
    description = models.TextField("Описание набора")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Набор"
        verbose_name_plural = "Наборы"

    def get_absolute_url(self):
        return reverse('set_id', kwargs={'id': self.pk})



class Questions(models.Model):
    name = models.CharField("Вопросы", max_length=150)
    sets = models.ForeignKey(Sets, verbose_name = 'Набор', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Answers(models.Model):
    name = models.CharField("Ответ", max_length=150)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    IsTrue = models.BooleanField("Верный", default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    mark = models.BooleanField('Оценка', default=False)
    checked = models.BooleanField('Проходил', default=False)

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"