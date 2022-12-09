from rest_framework import serializers
from UserApp.models import User

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['UserName', 'UserSurename', 'TOKEN', 'TOKENDATE']
        read_only_fields = ['UserName', 'UserSurename', 'TOKEN', 'TOKENDATE']
