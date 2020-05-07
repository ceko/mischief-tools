from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultSocialAccountAdapter):

    def get_logout_redirect_url(self, request):
        return '/logout/'
