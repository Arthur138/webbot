from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webbot.serializers import UserSerializer
from webbot.models import Supervizor, Agent
from webbot.serializers import SupervizorSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from django.db import IntegrityError

class CreateAgent(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        file_path = 'webbot/agent.json'

        with open(file_path, 'r', encoding='utf-8') as file:
            d = json.load(file)
            # print(d)
            agents = d.get('agent_user_id')
            for agent in agents:
                # print(agent)
                name = agent['surname']

                try:
                    sv = Supervizor.objects.get(supervizer_hydra_id=agent['supervizer'])
                    user, created = UserModel.objects.get_or_create(username=agent['login'])
                    if created:
                        user.set_password(agent['password'])
                        user.save()
                        agentus = Agent.objects.create(user=user, bx_id=agent['bx_id'], surname=agent['surname'],
                                                       supervizer=sv, hydra_id_sales=agent['hydra_id_sales'])
                        agentus.save()
                        print(f'new = {agentus}')
                    elif user:
                        agentus = Agent.objects.create(user=user, bx_id=agent['bx_id'], surname=agent['surname'],
                                                       supervizer=sv, hydra_id_sales=agent['hydra_id_sales'])
                        agentus.save()
                        print(f'^^^^^^^^^^^^^old = {agentus}')

                    # user = UserModel.objects.create(username=agent['login'])
                    # user.set_password(agent['password'])
                    # user.save()

                    # print(f'{user} --->  {agentus}')
                except ObjectDoesNotExist:
                    print(f"============================-----------------------------{name}Супер не найден")




                # user = UserModel.objects.create(username=agent['login'])
                # user.set_password(agent['password'])
                # user.save()
                # agentus = Agent.objects.create(user=user, bx_id=agent['bx_id'], surname=agent['surname'])
        return Response({"message": "suka"}, status=status.HTTP_200_OK)


class CreateSupervizor(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        file_path = 'webbot/supervizers.json'

        with open(file_path, 'r', encoding='utf-8') as file:
            d = json.load(file)
            # print(d)
            supervizers = d.get('agent_core_supervizer','nihua')
            for supervizer in supervizers:
                # print(supervizer['login'])
                user = UserModel.objects.create(username=supervizer['login'])
                user.set_password(supervizer['password'])
                user.save()
                super = Supervizor.objects.create(user=user, region=supervizer['region'], supervizer_hydra_id= supervizer['supervizer_id'], supervizer_surname=supervizer['supervizer_surname'])
                print(f'{user} ---> {super}')
        return Response({"message": "Pizdec"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"message": "Пользователь успешно вышел из системы"}, status=status.HTTP_200_OK)

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