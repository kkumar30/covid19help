from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse

User = get_user_model()


def list_users(request):
    context = {'user': User.objects.first()}
    return TemplateResponse(request, "home.html", context)
