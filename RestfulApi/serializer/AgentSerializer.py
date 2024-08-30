from rest_framework import serializers
from RestfulApi.models import UserAgentLog

class AgentLogSerializer (serializers.ModelSerializer) :
    class Meta :
        model = UserAgentLog
        fields = '__all__'