from django.db import models

# Create your models here.

class Lense(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=50)
    p_desc = models.TextField()
    p_quantity = models.PositiveIntegerField()
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    p_image = models.ImageField(upload_to='uploads')

    def __str__(self):
        return self.p_name

    class Meta:
        db_table = 'p_app'
