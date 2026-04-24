from django.test import override_settings
from django.urls import reverse

from utilities.testing import TestCase


class PasskeyViewsTestCase(TestCase):

    @override_settings(PASSKEYS_ENABLED=True)
    def test_login_page_includes_passkey_button(self):
        self.client.logout()
        response = self.client.get(reverse('login'))

        self.assertHttpStatus(response, 200)
        self.assertContains(response, 'Sign In With Passkey')

    @override_settings(PASSKEYS_ENABLED=False)
    def test_login_page_hides_passkey_button_when_disabled(self):
        self.client.logout()
        response = self.client.get(reverse('login'))

        self.assertHttpStatus(response, 200)
        self.assertNotContains(response, 'Sign In With Passkey')

    @override_settings(PASSKEYS_ENABLED=True)
    def test_passkey_page_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('account:passkeys'))

        self.assertHttpStatus(response, 302)

    @override_settings(PASSKEYS_ENABLED=True)
    def test_passkey_page_renders_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account:passkeys'))

        self.assertHttpStatus(response, 200)
        self.assertContains(response, 'Add a Passkey')
        self.assertContains(response, 'No passkeys found')

    @override_settings(PASSKEYS_ENABLED=True)
    def test_account_navigation_includes_passkey_tab_when_enabled(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account:profile'))

        self.assertHttpStatus(response, 200)
        self.assertContains(response, reverse('account:passkeys'))

    @override_settings(PASSKEYS_ENABLED=False)
    def test_account_navigation_hides_passkey_tab_when_disabled(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account:profile'))

        self.assertHttpStatus(response, 200)
        self.assertNotContains(response, reverse('account:passkeys'))

    @override_settings(PASSKEYS_ENABLED=False)
    def test_passkey_page_404_when_disabled(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account:passkeys'))

        self.assertHttpStatus(response, 404)