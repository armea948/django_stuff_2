from django.db import models

# Create your models here.
class GA_Data(models.Model):
    source = models.TextField()
    pageview = models.IntegerField()
    bouncerate = models.FloatField()
    transactions = models.IntegerField()
    
    
    def get_source(self):
        return "%s" % (self.source)
        
    def get_pageview(self):
        return "%d" % (self.pageview)
    
    def get_bouncerate(self):
        return "%f" % (self.bouncerate)
    
    def get_transactions(self):
        return "%d" % (self.transactions)
        