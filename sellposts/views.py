from .serializers import *
from .models import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Count
from .pagination import CustomPaginator



class SellAdCreateView(generics.GenericAPIView):
    serializer_class = SellAdCreateSrializer
    permissions = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwags):
        request.data['owner'] = request.user.id
        new_add = self.get_serializer(data=request.data)
        new_add.is_valid(raise_exception=True)
        new_add.save()

        return Response(new_add.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        sellpost_id = request.data['id']
        try:
            sellpost = SellAd.objects.get(id=sellpost_id)
            updated_post = self.get_serializer(sellpost, data=request.data, partial=True)
            updated_post.is_valid(raise_exception=True)
            updated_post.save()

            return Response(updated_post.data, status=status.HTTP_202_ACCEPTED)
        
        except SellAd.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        sellpost_id = request.data['id']
        try:
            sellpost = SellAd.objects.get(id=sellpost_id)
            sellpost.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except SellAd.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AttachImageReq(generics.GenericAPIView):
    permissions = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        no_img = int(request.data.get('num', 0))
        post_id = request.data.get('post_id')
        if post_id is not None:
            for i in range(no_img):
                field = 'image' + str(i)
                img = request.data[field]
                img_ins = AdImages(product_img=img, add_id_id=int(post_id))
                img_ins.save()
            
            return Response(status=status.HTTP_200_OK)
        
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AllSellPostsView(generics.GenericAPIView):
    serializer_class = SellAdDetailSerializer2
    permissions = [permissions.AllowAny, ]
    pagination_class = CustomPaginator

    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        if category is not None:
            posts = SellAd.objects.filter(category=category, is_active=True).order_by('-posted_at')
        else:
            posts = SellAd.objects.filter(is_active=True).order_by('-posted_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            post_lists = self.get_paginated_response(self.get_serializer(page, context={'request': request}, many=True).data)
        else:
            post_lists = self.get_serializer(posts, context={'request': request}, many=True)

        return Response(post_lists.data)


class SellPostsGroupCount(generics.GenericAPIView):
    serializer_class = GroupCountSerializer
    permissions = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        group = SellAd.objects.all().values('category').annotate(total=Count('category'))
        list_data = self.get_serializer(group, many=True)

        return Response(list_data.data, status=status.HTTP_200_OK)


class SellAdDetailView(generics.GenericAPIView):
    serializer_class = SellAdDetailSerializer
    permissions = [permissions.AllowAny, ]

    def get(self, request, *args, **kwags):
        try:
            sellad = SellAd.objects.get(pk=kwags['pk'])
            serializer = self.get_serializer(sellad)

            return Response(serializer.data)
        except SellAd.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CloseSellAdd(generics.GenericAPIView):
    permissions = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        post_id = request.data['id']
        print(f'{post_id} kamne somvob')
        try:
            post = SellAd.objects.get(id=post_id)
            if post.owner.id == request.user.id:
                post.is_active = False
                post.save()

                return Response(status=status.HTTP_202_ACCEPTED)
            
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        
        except SellAd.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

