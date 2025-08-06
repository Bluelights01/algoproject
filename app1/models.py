from django.db import models

# Create your models here.
class Users(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    user_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)


class Question(models.Model):
    QUESTION_TYPES = [
        ('array', 'Array'),
        ('dynamic', 'Dynamic Programming'),
        ('string', 'String'),
        ('graph', 'Graph'),
        ('tree', 'Tree'),
        ('math', 'Mathematics'),
        ('greedy', 'Greedy'),
        ('other', 'Other'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    name = models.CharField(max_length=200, unique=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    description = models.TextField() 

    input_format = models.TextField(blank=True, null=True)
    output_format = models.TextField(blank=True, null=True)
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)

    testcases = models.JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
