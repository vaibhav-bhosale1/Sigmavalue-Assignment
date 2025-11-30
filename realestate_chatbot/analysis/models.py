# analysis/models.py
from django.db import models

class RealEstateData(models.Model):
    final_location = models.CharField(max_length=100)
    year = models.IntegerField()
    city = models.CharField(max_length=100)
    loc_lat = models.FloatField()
    loc_lng = models.FloatField()
    
    # Sales Data
    total_sales_igr = models.FloatField()
    total_sold_igr = models.IntegerField()
    flat_sold_igr = models.IntegerField()
    office_sold_igr = models.IntegerField()
    others_sold_igr = models.IntegerField()
    shop_sold_igr = models.IntegerField()
    commercial_sold_igr = models.IntegerField()
    other_sold_igr = models.FloatField(null=True, blank=True)
    residential_sold_igr = models.IntegerField()
    
    # Rates
    flat_weighted_avg_rate = models.FloatField()
    office_weighted_avg_rate = models.FloatField()
    others_weighted_avg_rate = models.FloatField()
    shop_weighted_avg_rate = models.FloatField()
    
    # Prevailing Rate Ranges (stored as text)
    flat_prevailing_rate_range = models.CharField(max_length=50)
    office_prevailing_rate_range = models.CharField(max_length=50)
    others_prevailing_rate_range = models.CharField(max_length=50)
    shop_prevailing_rate_range = models.CharField(max_length=50)
    
    # Supply Data
    total_units = models.IntegerField()
    total_carpet_area_supplied = models.FloatField()
    flat_total = models.IntegerField()
    shop_total = models.IntegerField()
    office_total = models.IntegerField()
    others_total = models.IntegerField()

    def __str__(self):
        return f"{self.final_location} - {self.year}"