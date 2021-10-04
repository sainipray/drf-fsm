===============
Django FSM with Django Rest Framework.
===============

Overview
========
drf_fsm library provides an endpoint for defined each transition in models using Django FSM with Django Rest Framework library.


Features
========
This library provides endpoint for each transition of FSM and customize like:

1. Easy to define the number of FSM fields that's the endpoint you want to create automatically. default : No field.
2. Easy to define how many transitions endpoint you want to create for particular field: default: all transition of fields.
3. Easy to define serializer for each transition and field name wise: default: serializer_class of ViewSet.
4. Easy to handle response for each endpoint of transition and field, default: serializer.data .

Installation
============

- Install drf_fsm using pip::

    pip install drf_fsm

- Import Mixin from drf_fsm and Use in ViewSet views of DRF::

    from drf_fsm.mixins import FsmViewSetMixin


Uses with example
================

Lets Suppose a Post model that uses Django FSM

models.py::

    from django.contrib.auth import get_user_model
    from django.db import models
    from django_fsm import transition, FSMField

    User = get_user_model()


    class PostStatusChoices(models.TextChoices):
        Draft = 'draft', 'Draft'
        Pending = 'pending', 'Pending'
        Publish = 'publish', 'Publish'
        Future = 'future', 'Future'
        Trash = 'trash', 'Trash'


    class Post(models.Model):
        title = models.CharField(max_length=200, unique=True)
        slug = models.SlugField(max_length=200, unique=True)
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
        updated_on = models.DateTimeField(auto_now=True)
        content = models.TextField()
        created_on = models.DateTimeField(auto_now_add=True)
        status = FSMField('Status', max_length=20, default=PostStatusChoices.Draft,
                          choices=PostStatusChoices.choices, protected=True)

        @transition(field=status, source='*', target=PostStatusChoices.Draft)
        def draft(self):
            pass

        @transition(field=status, source=PostStatusChoices.Draft, target=PostStatusChoices.Pending)
        def pending(self):
            pass

        @transition(field=status, source=PostStatusChoices.Pending, target=PostStatusChoices.Publish)
        def publish(self):
            pass

        @transition(field=status, source=PostStatusChoices.Pending, target=PostStatusChoices.Future)
        def future(self):
            pass

        @transition(field=status, source='*', target=PostStatusChoices.Trash)
        def trash(self):
            pass




We define model with 5 choices above and added 5 transition for each status in model.

Now create ViewSet for Post model

views.py::

    from rest_framework.viewsets import ModelViewSet
    from drf_fsm.mixins import FsmViewSetMixin
    from .models import Post
    from .serializers import PostSerializer


    class PostViewSet(FsmViewSetMixin, ModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        fsm_fields = ['status']


Here we define "status" as a FSM field, we can define multiple in list if we have multiple in single model

Connect this views to DRF router
urls.py::

    from rest_framework.routers import DefaultRouter
    from .views import PostViewSet

    router = DefaultRouter()

    router.register('post', PostViewSet, basename="post_view_set")

    urlpatterns = router.urls


Finished. Cheers ✌️
------------------

Now checking Output in Swagger

.. image:: output.png
   :width: 100%


😎 :),
====

Let's move to customizations:

Customizations
============

1. Define number of fields of FSM in view like::

    fsm_fields = ['status', 'priority']

2. Define particular transitions for include, left will ignore for endpoints.
   suppose field name is "status" and have 5 transition according above example so we can
   handle which transition should include and other ignore.

   So write @classmethod in viewset for override this feature::

    @classmethod
    def status_transitions(cls):  # Here status in field name so it's dynamic based on FSM field name.
        return ['trash', 'publish']

Here "trash" and "publish" transition endpoint will available for API, other will ignore from endpoints

3. Define serializer class for each transition or field name wise::

    publish_status_serializer_class = PublishStatusPostSerializer # {transition}_{field_name}_serializer_class

    or

    status_serializer_class = StatusPostSerializer  # {field_name}_serializer_class

    or, default

    serializer_class = PostSerializer  # Default serializer class for each

Serializer class uses dynamic name for each transition if define otherwise default will use.

4. Define Response of each transition::

        def publish_status_response(self, serializer): # {transition}_{field_name}_response
            return {"message": "Post status updated published"}

        or

        def status_response(self, serializer): # {field_name}_response, but it'll show for all transition of status field
            return {"message": "Post status updated"}

        or, default

        serializer.data




If you feel this library is useful for your work just buy some coffee for me so I'll try improved this and will work on new libraries.

<a href="https://www.buymeacoffee.com/sainipray" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

License
=======

drf_fsm is an Open Source project licensed under the terms of the `MIT license <https://github.com/sainipray/drf-fsm/blob/main/LICENSE>`_

