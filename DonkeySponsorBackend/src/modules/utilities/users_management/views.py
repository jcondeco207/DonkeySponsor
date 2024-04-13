from django.db import IntegrityError
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from two_factor.views import LoginView as TFLoginView
from django.utils.http import url_has_allowed_host_and_scheme
from axes.utils import reset as attemptsReset
from axes.models import AccessAttempt
from Donkey_Sponsor.settings import AXES_FAILURE_LIMIT
import bleach
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth.hashers import make_password
from rest_framework import filters
from django.db.models import Q
from rest_framework.views import APIView
from . import serializers as usersSerializers
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, generics
from .models import MustReset, User, Role
from .serializers import RoleSerializer, UserSerializer, CreateUserSerializer
from . import permissions as usersPermissions

# Methods to reenable users blocked by axes
# Can use ip or username
@extend_schema(tags=["Manage - Users"])
class Reenable(APIView):
    authentication_classes = (TokenAuthentication, authentication.SessionAuthentication)
    def post(self, request):
        username = request.data.get('username')
        ip = request.data.get('ip')
        if username:
            bleach.clean(username)
            usersEnabled = attemptsReset(username=username)
            return Response(data={'enabled': usersEnabled}, status=status.HTTP_200_OK)

        elif ip:
            bleach.clean(ip)
            usersEnabled = attemptsReset(username=username)
            return Response(data={'enabled': usersEnabled}, status=status.HTTP_200_OK)

        return Response(data={"enabled": False, "details": "no fields 'username' or 'ip' found."})

@extend_schema(
    tags=["Manage - Users"],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
    description="Upgrades a user to an admin",
    )
class UpgradeToAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        userId = self.kwargs.get('pk', None)
        if not userId:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            newRole = Role.objects.get(name='SOCAdmin')
            user.role = newRole
        except:
            return Response(data={"error":"Role not found"},
                            status=status.HTTP_400_BAD_REQUEST)


        user.is_staff = True
        user.is_superuser = True
        user.save()

        return Response({"message": f"User {user.username} has been upgraded to SOC Administritator"}, status=status.HTTP_200_OK)

@extend_schema(tags=["Manage - Users"])
class ChangeUserRole(APIView):
    permission_classes = [permissions.IsAdminUser |  usersPermissions.IsDonkeyAdmin]
    authentication_classes = [TokenAuthentication, authentication.SessionAuthentication]

    def allowChange(self, userRole, oldRole, role):

        if userRole == "SOCAdmin" and oldRole != "SOCAdmin":
            print("HEERE 1")
            return True

        elif userRole == "Admin" and oldRole != "Admin" and role != "SOCAdmin":
            print("HEERE 2")
            return True

        print("Here FALSE")
        return False

    def post(self, request, *args, **kwargs):
        userId = self.kwargs.get('pk', None)
        roleName = request.data.get('role', None)
        if not roleName:
            return Response({"error": "Role not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            newRole = Role.objects.get(name=roleName)

            if self.allowChange(request.user.role.name, user.role.name, newRole):
                if roleName == "SOCAdmin":
                    return Response(data={"error":"In order to perform that action use '/make_admin' instead"},
                                    status=status.HTTP_400_BAD_REQUEST)
                user.role = newRole
            else:
                print("Here")
                return Response(data={"error":"You are not allowed to perform the requested role change"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response(data={"error":"Role not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        user.save()

        return Response({"message": f"User {user.username} has been changed to {roleName}"}, status=status.HTTP_200_OK)

@extend_schema(tags=["Manage - Users"])
class BlockUser(APIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (TokenAuthentication, authentication.SessionAuthentication,)
    def post(self, request):
        username = request.data.get('username')
        ip = request.data.get('ip')
        if username:
            bleach.clean(username)

            try:
                AccessAttempt.objects.get(username=username)
                AccessAttempt.objects.filter(username=username).update(failures_since_start= AXES_FAILURE_LIMIT)
            except AccessAttempt.DoesNotExist:
                AccessAttempt.objects.create(username=username, failures_since_start=AXES_FAILURE_LIMIT)

            return Response(data={'blocked': username}, status=status.HTTP_200_OK)

        elif ip:
            bleach.clean(ip)
            try:
                AccessAttempt.objects.get(ip_address=ip)
                AccessAttempt.objects.filter(ip_address=ip).update(failures_since_start= AXES_FAILURE_LIMIT)
            except AccessAttempt.DoesNotExist:
                AccessAttempt.objects.create(ip_address=ip, failures_since_start=AXES_FAILURE_LIMIT)

            return Response(data={'blocked': ip}, status=status.HTTP_200_OK)

        return Response(data={"blocked": False, "details": "no fields 'username' or 'ip' found."})

@extend_schema(tags=["Manage - Users"])
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, authentication.SessionAuthentication]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        # Retrieve relevant information
        search_param = self.request.query_params.get('search', "")

        if search_param:
            queryset = queryset.filter(
                Q(username__icontains=search_param) |
                Q(email__icontains=search_param)
            )


        return queryset

    @extend_schema(
        description="Create user",
        request=usersSerializers.CreateUserSerializer(),
        responses={200: usersSerializers.UserSerializer()}
    )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ['username', 'first_name', 'last_name', 'email', 'password']

        if not all(field in data for field in required_fields):
            return Response(data={"error":"Must provide username, first_name, last_name, email and password"},
                            status=status.HTTP_400_BAD_REQUEST)

        role = data.get('role', 'Observer')
        try:
            role = Role.objects.get(name=role)
        except:
            return Response(data={"error":"Role not found"},
                            status=status.HTTP_400_BAD_REQUEST)

        if role == 'SOCAdmin' and not request.user.is_superuser:
            return Response(data={"error":"You don't have permissions"},
                            status=status.HTTP_401_UNAUTHORIZED)

        data['password'] = make_password(data['password'])
        data['role'] = role.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                return Response(data={"error": "A user with these details already exists. Please try again with different details."},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"error": f"An error occurred. Details: {str(e)}"},
                                status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        user_id = serializer.data["id"]

        if User.objects.filter(id=user_id).exists():
            MustReset.objects.create(requestedBy=User.objects.get(id=user_id)).save()
            user = User.objects.get(id=user_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@extend_schema(tags=["Manage - Users"])
class RolesList(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, authentication.SessionAuthentication]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        if self.request.user.is_superuser:

            return Role.objects.all()

        super_role = Role.objects.filter(name='SOCAdmin')
        return Role.objects.exclude(super_role)

@extend_schema(tags=["Manage - Users"])
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, authentication.SessionAuthentication]

@extend_schema(tags=["Manage - Users"])
class ResetUserPassword(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, authentication.SessionAuthentication]
    def post(self, request, *args, **kwargs):
        try:
            id = kwargs.get('pk')
            password = request.data.get("password")
            if not password or not id:
                return Response({"error": "id and password must be provided"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Get the created user
            user = User.objects.get(pk=id)
            user.set_password(password)
            user.save()

            mr = MustReset.objects.create(requestedBy=user)
            mr.save()

            return Response({'ok': "password reset"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Manage - Users"])
class ChangeUserState(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication, authentication.SessionAuthentication]
    def post(self, request, *args, **kwargs):

        try:
            id = kwargs.get('pk')

            # Get the created user
            user = User.objects.get(pk=id)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True

            user.save()

            return Response({'is_active': user.is_active}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
