from django.urls import path
from .views import *

urlpatterns = [
    path('createadd/', SellAdCreateView.as_view(), name='create_new_add'),
    path('attachimg/', AttachImageReq.as_view(), name='attach_img'),
    path('allposts/', AllSellPostsView.as_view(), name='all_posts'),
    path('groups/', SellPostsGroupCount.as_view(), name='group_count'),
    path('detail/<int:pk>/', SellAdDetailView.as_view(), name='product_detail'),
    path('closeadd/', CloseSellAdd.as_view(), name='close'),
]