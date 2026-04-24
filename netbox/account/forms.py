from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class NetBoxAuthenticationForm(AuthenticationForm):
    """
    Authentication form with widget attributes suitable for passkey-assisted login.
    """

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username webauthn',
            'autofocus': True,
            'id': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
            'id': 'password',
        })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data