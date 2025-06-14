from django.db import models

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Mission(models.Model):
    cat = models.ForeignKey(SpyCat, null=True, blank=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)

class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField()
    completed = models.BooleanField(default=False)