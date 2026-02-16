from django.db import models

# Create your models here.

class cheque_details(models.Model):
     cheque_number = models.CharField(max_length=200)
     cheque_date=models.CharField(max_length=200)
     cheque_bank=models.CharField(max_length=200)
     account_name=models.CharField(max_length=200)
     payee_name=models.CharField(max_length=200)
     cheque_amount=models.CharField(max_length=200)
     remarks=models.CharField(max_length=200)    
    
     def __str__(self):
         return self.cheque_number


    
   