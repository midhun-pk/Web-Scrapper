from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from crawler.service import Crawler
import json

# Create your views here.


@require_http_methods(["GET"])
def index(request):
    return render(request, 'home.html')


@csrf_exempt
@require_http_methods(["POST"])
def crawl(request):
    body = json.loads(request.body.decode("utf-8"))
    print(body)
    results = []
    if 'url' in body and 'depth' in body:
        url = body['url']
        depth = body['depth']
        crawler = Crawler(url, depth)
        results = crawler.start_crawl()
    return HttpResponse(json.dumps(results), status=200)
