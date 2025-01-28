from operator import index

from django.urls import path
from .views import PredictView, index

urlpatterns = [
    path('analyze/', PredictView.as_view(), name='analyze'),
    path('', index, name='index')
]
