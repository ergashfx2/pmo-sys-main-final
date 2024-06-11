from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from django.contrib.auth import get_user_model, logout

User = get_user_model()


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.status !='Active':
            logout(request)
            return render(request,'blocked_page.html')
