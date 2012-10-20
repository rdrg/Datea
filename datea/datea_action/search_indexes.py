from haystack import indexes
from models import DateaAction

"""
class ActionIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    category = indexes.CharField(model_attr='category', null=True)
    
    def get_model(self):
        return DateaAction
    
    def index_queryset(self):
        return self.get_model().objects.filter(published=True)
"""
    

        
        
