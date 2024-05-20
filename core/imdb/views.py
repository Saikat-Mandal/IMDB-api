from .models import Watchlist , StreamPlatform , Review
from .serializers import WatchlistSerializer , StreamPlatformSerializer , ReviewSerializer
from .permissions import AdminOrReadOnly , ReviewUserOrReadOnly

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView , api_view
from rest_framework.reverse import reverse
from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated , IsAdminUser , IsAuthenticatedOrReadOnly




@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'watchlist': reverse('Watchlist-list', request=request, format=format),
        'streamingplatform': reverse('StreamPlatform-platform', request=request, format=format)
    })

    

# movies     
class movie_list(APIView):
    def get(self , request):
        movie_list = Watchlist.objects.all()
        serializer = WatchlistSerializer(movie_list , many =True)
        return Response(serializer.data )
    

class movie_detail(APIView):
    def get(self , request , pk):
        movie = Watchlist.objects.get(pk = pk)
        serializer = WatchlistSerializer(movie)
        return Response(serializer.data)


# streaming platform 
class stream_list(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# class StreamPlatformViewSet(viewsets.ModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer    


class stream_detail(APIView):

    def get_object(self, pk):
        try:
           return StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self , request , pk):
        serializer_context = {
            'request': request,
        }
        stream_platform  = self.get_object(pk)
        serializer = StreamPlatformSerializer(stream_platform , context=serializer_context)
        return Response(serializer.data)

    def put(self , request ,pk):
        stream_platform  = self.get_object(pk)
        serializer = StreamPlatformSerializer(stream_platform , data = request.data)
        if serializer.is_valid():
            serializer.save()     
            return Response(serializer.data)       

    def delete(self , request , pk):
        stream_platform  = self.get_object(pk)        
        stream_platform.delete() # type: ignore
        return Response(status=status.HTTP_204_NO_CONTENT)
    

 # reviews 
class reviewListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class reviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = Watchlist.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(review_user=review_user, watchlist=movie)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie.")
        
        if movie.number_rating == 0:
            movie.average_rating = serializer.validated_data['rating']
        else:
            movie.average_rating = (movie.average_rating + serializer.validated_data['rating']) / 2
        
        movie.number_rating += 1    
        movie.save()
        serializer.save(watchlist=movie , review_user = review_user)

# class reviewListViewDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer


class reviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer