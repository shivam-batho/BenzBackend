from rest_framework import serializers
from lead.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth  import authenticate
class GeneratePairTokenSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        email =  attrs.get('email')
        password = attrs.get('password')
        user = authenticate( email = email , password = password)
        if user is None :
            raise serializers.ValidationError({'details':'No active User found with the given credentials'})

        if not user.check_password(password) :
            raise serializers.ValidationError({'details':'Password does not match'})
        

        #Generate Token
        refresh = RefreshToken.for_user(user)

        return {
            'status' :200,
            'message':"User Login Successfully",
            'refresh_token' : str(refresh),
            'access_token' : str(refresh.access_token),
        }





class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoDetails
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    userInfo = UserInfoSerializer(read_only = True , required = False)
    
    class Meta:
        model = User
        fields = '__all__'
    
    def to_internal_value(self,data):
        validated_data = data.copy()
        userDetailsData = {}
        for key,value in data.items():
            userdetails_key = ['designation','experience','joining_date','birth_date','address','user_role','gender']
            if key in userdetails_key:
                userDetailsData[key] = value[0] if isinstance(value , list) else value
                del validated_data[key]
            else:
                validated_data[key] = value[0] if isinstance(value , list) else value
        new_dict = {('dob' if key == 'birth_date' else 'doj' if key == 'joining_date' else key) : val for key , val in userDetailsData.items()}
        validated_data['userInfo'] = new_dict
        return validated_data
            
    def create(self, validated_data):
        userInfo = validated_data.pop('userInfo')
        if userInfo is not None:
            password = validated_data.pop('password',None)
            password = password[0] if isinstance(password , list) else password
            userInstance = UserSerializer.Meta.model(**validated_data)
            if userInstance is not None:
                userInstance.set_password(password)
                userInstance.save()
                user_info = UserInfoDetails.objects.create(**userInfo , user = userInstance)
            return userInstance
