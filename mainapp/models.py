from django.db import models

class TodoModel(models.Model):
    title = models.CharField(max_length=50,blank=False)
    description = models.TextField(blank=False)
    deadline = models.DateField()
    isComplete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
