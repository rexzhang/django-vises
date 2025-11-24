from django.shortcuts import render


# Create your views here.
def vises_django_settings(request):
    return render(request, "core/vises_django_settings.html")
