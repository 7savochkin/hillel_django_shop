from django import forms
from django.contrib.auth.models import User

from feedbacks.models import Feedback


class FeedbackForm(forms.Form):
    text = forms.CharField()
    user = forms.CharField()
    rating = forms.IntegerField(min_value=0, max_value=5)

    @staticmethod
    def check(text: str) -> str:
        """
        Delete special characters from text
        :return:
        """
        char_list = []
        for char in text:
            if char.isalnum():
                char_list.append(char)
            elif char == ' ':
                char_list.append(char)
        clear_text = ''.join(char_list)
        return clear_text

    def is_valid(self) -> bool:
        """
        Validate Date
        :return:
        """

        is_valid = super().is_valid()

        if is_valid:
            user_login = self.cleaned_data['user']
            try:
                user = User.objects.get(username=user_login)
            except User.DoesNotExist:
                self.errors.update({
                    'user': f"{user_login} doesn't exist"})
            else:
                self.cleaned_data['user'] = user
            text = self.cleaned_data['text']
            self.cleaned_data['text'] = self.check(text)
        return is_valid

    def save(self):
        """
        Create Feedback
        :return:
        """
        return Feedback.objects.create(**self.cleaned_data)
