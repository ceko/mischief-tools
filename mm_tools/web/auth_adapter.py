from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        return False

    def get_logout_redirect_url(self, request):
        return '/logout/'
