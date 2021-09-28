from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
from newsapi import NewsApiClient
from django.contrib.auth.decorators import login_required


# Create your views here.

temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"

@login_required
def news_page(request):

    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)
    domains = request.GET.get('domains', None)

    if ((search is None or search=="top") and (domains == None)):
        # get the top news
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "in",1,settings.APIKEY
        )
    elif(search!=None and domains == None):
        # get the search query request
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            search,"popularity",page,settings.APIKEY
        )
    elif((search is None or search=="top") and domains != None):
        url = "https://newsapi.org/v2/top-headlines?domains={}&page={}&apiKey={}".format(
            domains,1,settings.APIKEY
        )
    else:
        url = "https://newsapi.org/v2/everything?q={}&domains={}&sortBy={}&page={}&apiKey={}".format(
            search,domains,"popularity",page,settings.APIKEY
        )



    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search,
        "domains": domains
    }
    # seprating the necessary data
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"],
            "source" : i["source"]
        })

    # send the news feed to template in context
    return render(request, 'news/news_page.html', context=context)


def loadcontent(request):
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        domains = request.GET.get('domains', None)

        if ((search is None or search=="top") and (domains == None)):
            # get the top news
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "in",1,settings.APIKEY
            )
        elif(search!=None and domains == None):
            # get the search query request
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search,"popularity",page,settings.APIKEY
            )
        elif((search is None or search=="top") and domains != None):
            url = "https://newsapi.org/v2/top-headlines?domains={}&page={}&apiKey={}".format(
                domains,1,settings.APIKEY
            )
        else:
            url = "https://newsapi.org/v2/everything?q={}&domains={}&sortBy={}&page={}&apiKey={}".format(
                search,domains,"popularity",page,settings.APIKEY
            )

        print("url:",url)
        r = requests.get(url=url)

        data = r.json()
        if data["status"] != "ok":
            return JsonResponse({"success":False})
        data = data["articles"]
        context = {
            "success": True,
            "data": [],
            "search": search,
            "domains": domains
        }
        for i in data:
            context["data"].append({
                "title": i["title"],
                "description":  "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"],
                "source" : i["source"]
            })

        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"success":False})
