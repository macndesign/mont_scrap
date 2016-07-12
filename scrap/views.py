from channels import Channel
from django.shortcuts import render

BASE_URL = 'http://www.montenegroleiloes.com.br/'


def extract(request):
    msg = {}
    Channel('extract').send(msg)
    return render(request, 'scrap/extract.html', {})
