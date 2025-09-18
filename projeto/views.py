from django.shortcuts import redirect, render
def generations_list():
    generations = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
        {"id": 6},
        {"id": 7},
        {"id": 8},
        {"id": 9}
        ]
    return generations

def home(request):
    generations = generations_list()
    return render(request, "home.html", {"generations": generations})
