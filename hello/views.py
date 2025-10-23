from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    if "count" not in request.session:
        request.session["count"] = 0

    if request.method == "POST":
        request.session["count"] += 1

    return render(
        request,
        "hello/index.html",
        {"count": request.session["count"]},
    )
