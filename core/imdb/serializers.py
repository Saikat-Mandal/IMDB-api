from rest_framework import serializers 
from .models import Watchlist , StreamPlatform , Review
from django.contrib.auth.models import User
# class WatchlistSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     title= serializers.CharField(max_length=50)
#     storyline= serializers.CharField(max_length=100)
#     # platform= serializers.ForeignKey(StreamPlatform , on_delete=models.CASCADE)
#     active=serializers.BooleanField(default=True)
#     created=serializers.DateTimeField()

#     def create(self, validated_data):
#         """
#         Create and return a new `Watchlist` instance, given the validated data.
#         """
#         return Watchlist.objects.create(**validated_data) 

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Watchlist` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.storyline = validated_data.get('storyline', instance.storyline)
#         instance.active = validated_data.get('active', instance.active)
#         instance.created = validated_data.get('created', instance.created)
#         instance.save()
#         return instance       

# class StreamPlatformSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     about = serializers.CharField(max_length=100)
#     website = serializers.URLField(max_length=100)

#     def create(self, validated_data):
#         return StreamPlatform.objects.create(**validated_data)    



class WatchlistSerializer(serializers.ModelSerializer):
    platform = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Watchlist
        fields = '__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = WatchlistSerializer(many = True , read_only = True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'

    def validate_name(self, value):
        if len(value) <= 2:
            raise serializers.ValidationError("name is too short")
        return value  

    def validate(self,data):
        if data['name'] == data['name']:
            raise serializers.ValidationError("Name and about must be different")     
        return data  

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    watchlist = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'snippets']        

    