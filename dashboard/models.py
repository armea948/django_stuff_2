from django.db import models

# Create your models here.
class GA_Data(models.Model):
    pageview = models.IntegerField()
    bouncerate = models.FloatField()
    transactions = models.IntegerField()
    ctr = models.FloatField()
    sessions = models.IntegerField()
    costPerTransaction = models.FloatField()
    impressions = models.IntegerField()
    adClicks = models.IntegerField()
    
    date_start = models.DateField()
    date_end = models.DateField()
    profile = models.CharField(max_length=100)
    
        
    def get_pageview(self):
        return "%d" % (self.pageview)
    
    def get_bouncerate(self):
        return "%f" % (self.bouncerate)
    
    def get_transactions(self):
        return "%d" % (self.transactions)
        
    def get_ctr(self):
        return "%f" % (self.ctr)
        
    def get_sessions(self):
        return "%f" % (self.sessions)
        
    def get_costPerTransaction(self):
        return "%f" % (self.costPerTransaction)
    
    def get_impressions(self):
        return "%f" % (self.impressions)
    
    def get_adClicks(self):
        return "%f" % (self.adClicks)
        
    def get_date_start(self):
        return "%s" % (str(self.date_start))
    
    def get_date_end(self):
        return "%s" % (str(self.date_end))
        
    def get_profile(self):
        return "%s" % (self.profile)