import factory
from mainapp.models import  TodoModel

class TodoModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TodoModel

    title = factory.Faker('sentence',nb_words = 4)
    description = factory.Faker('text')
    deadline = factory.Faker('date_this_decade', before_today=True)
    isComplete = False
