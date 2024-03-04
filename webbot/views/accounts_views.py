from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webbot.serializers import UserSerializer
from webbot.models import Supervizor
from webbot.serializers import SupervizorSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class RegisterView(APIView):
    def get(self, request):
        queryset = Supervizor.objects.all()
        serializer = SupervizorSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Пользователь успешно создан",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Пользователь успешно аунтефицирован", 'token': token.key})
        else:
            return Response({'error': 'Неверные учетные данные'}, status=400)