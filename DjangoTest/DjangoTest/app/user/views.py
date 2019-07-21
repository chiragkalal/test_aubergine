from django.shortcuts import render
from rest_framework import generics, mixins, status
from .models import User
from rest_framework.response import Response
from .responses import response
from .serializers import LoginSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


class UserCreateAPIView(APIView):
    """ User create Api view class """

    serializer_class = UserSerializer

    def post(self, request):
        """ create user using following logic. """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {'message': response['user']['created']},
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        
        return Response(
                {'message': response['user']['login'], 
                'access_token': serializer.data['access_token'],
                'refresh_token': serializer.data['refresh_token']},
                status=status.HTTP_200_OK
            )

class UserRetrieveAPIView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ Get specific user from the system. """

        try:
            user = User.objects.filter(id=request.user.id).first()
            if user is None:
                result = Response(
                    {'message': 'not exits'}, status=400)
            else:
                data = {
                    "email": user.email,
                    "name": user.name,
                    "city": user.city,
                }
                result = Response(data, status=200)
        except ValidationError as e:
            result = Response({"message": e}, status=400)

        return result