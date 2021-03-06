from haystack import indexes
from contacts.models import Contact


class ContactIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.NgramField(document=True, use_template=True)
    book = indexes.IntegerField(model_attr="book_id")

    def get_model(self):
        return Contact

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def get_updated_field(self):
        return 'changed'