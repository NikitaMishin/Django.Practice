from django.db import models



#CATEGORIES = ((1, "A"),(2,"B"),(3,"C") )

class Category(models.Model):
    name = models.CharField(max_length =30, unique = True)
    description = models.TextField()
    def __str__(self):
        return self.name

class Good(models.Model):
    name = models.CharField(max_length = 30,unique = True,verbose_name ="Name")
    in_stock = models.BooleanField(default=True, db_index = True, verbose_name= "In Stock")
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    price = models.IntegerField(verbose_name="Price")
    def __str__(self):
        if not self.in_stock:
            return self.name +" Not in Stock"
        return self.name
    class Meta:
        ordering = ["-price","name"]
        unique_together = ("category","name","price")
        verbose_name = "Item"
        verbose_name_plural="items"

class New(models.Model):
    title = models.CharField(max_length=100,db_index=True,verbose_name="Title")
    description=models.TextField(verbose_name="Description")
    content = models.TextField()
    pub_date=models.DateTimeField(db_index = True,auto_now_add = True,verbose_name="pub_date")    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural="Articles"        
    def __str__(self):
        return self.title+"  "+ str(self.pub_date)
