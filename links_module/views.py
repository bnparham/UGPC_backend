from django.shortcuts import render
from .models import linksModel
# Create your views here.

def links_component(request):
    public_links = linksModel.objects.filter(is_public=True, is_show=True)
    privet_links = linksModel.objects.filter(is_public=False, is_show=True)
    context = {
        "public_links" : public_links,
        "privet_links" : privet_links,
    }
    return render(request, "links_module/links.html", context)