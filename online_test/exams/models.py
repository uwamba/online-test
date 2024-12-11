from django.db import models
from companies.models import Company 
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class Test(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_marks = models.IntegerField()

    def __str__(self):
        return self.title
class Question(models.Model):
    SINGLE_ANSWER = 'single'
    MULTIPLE_ANSWER = 'multiple'
    TEXT_ANSWER = 'text'

    QUESTION_TYPE_CHOICES = [
        (SINGLE_ANSWER, _('Multiple Choice (Single Answer)')),
        (MULTIPLE_ANSWER, _('Multiple Choice (Multiple Answers)')),
        (TEXT_ANSWER, _('Text Answer')),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE,related_name='questions')
    text = models.TextField()
    marks = models.IntegerField()
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPE_CHOICES,
        default=SINGLE_ANSWER,
    )
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    answer_text = models.TextField(null=True, blank=True)  # For storing text answers
    def __str__(self):
        return f"Question: {self.text[:50]}..."  # Truncate text for readability in the admin


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]