from mod_auth.models import Role
from tests.base import BaseTestCase


class TestControllers(BaseTestCase):
    """Test main controllers."""

    def test_root(self):
        """Test the access of the home page."""
        response = self.app.test_client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home/index.html')

    def test_about(self):
        """Test the access of the about page."""
        response = self.app.test_client().get('/about')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home/about.html')

    def test_if_user_has_test_access_rights(self):
        """Test if the user will have rights to the tests."""
        self.create_user_with_role(
            self.user.name, self.user.email, self.user.password, Role.admin)

        with self.app.test_client() as c:
            response_login = c.post(
                '/account/login', data=self.create_login_form_data(self.user.email, self.user.password))

            response = c.get('/')
            self.assertEqual(response.status_code, 200)
            self.assert_context('test_access', True)
            self.assert_template_used('home/index.html')
