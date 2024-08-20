from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that do not require authentication
        exempt_urls = [reverse('select'), reverse('login'), reverse('register')]

        if request.path in exempt_urls or request.path == '/':
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('select')  # Redirect to select page if not authenticated

        # Proceed with the normal request flow
        response = self.get_response(request)
        return response