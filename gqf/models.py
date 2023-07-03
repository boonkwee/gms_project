from django.db import models

# Create your models here.
class GQF(models.Model):
    code = models.CharField(primary_key=True, max_length=8,
                            verbose_name="Facility Code",
                            db_column='code')
    name = models.CharField(max_length=80,
                            verbose_name="Facility Name",
                            db_column='name')
    enabled = models.BooleanField(default=False,
                                  verbose_name="In operation",
                                  db_column='enabled')
    modified = models.DateTimeField(auto_now=True, verbose_name="Modified")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")

    class Meta:
        db_table = "tbl_cbk_gqf"
        ordering = ('code',)
    
    def __str__(self):
        return f"{self.code}"

