from django.db import models

class Filmrate(models.Model):
    content = models.CharField(max_length=1000) # 제목
    rate = models.IntegerField() # 제작 년도
    
    #def __str__(self):
    #    return self.title


