from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from feedbacks.models import Feedback

UserModel = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'email', 'phone')


class FeedbacksSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(required=False, allow_null=False)

    class Meta:
        model = Feedback
        fields = ('id', 'text', 'rating', 'user')

    # extra_kwargs = {
    #    'user': dict(required=False, allow_null=False)
    # }

    #  def validate(self, attrs):
    #      if "http" in attrs["text"]:
    #          raise ValidationError("The
    #          'text' field must not contains urls.")
    #      return attrs

    def validate_text(self, value):
        if 'http' in value:
            raise ValidationError("The 'text' field must not contains urls.")
        return value

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        instance = super().create(validated_data)
        return instance
