from django.db import models

class Item(models.Model) :
    name = models.CharField(max_length=50 )
    alt = models.CharField(max_length=150 )
    url = models.CharField(max_length=100 )
    order = models.IntegerField(blank = True, null=True)
    visible = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        model = self.__class__
        if self.order is None:
            try:
                last = model.objects.order_by('-order')[0]
                print '--------', last.order
                self.order = last.order + 1
            except IndexError:
                self.order = 0

        return  super(Item, self).save(*args,**kwargs)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

