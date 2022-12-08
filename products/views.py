from django.shortcuts import render
from django.http import HttpResponse

# def home(request):
#     return render(request, 'home.html')
def main(request):
    return render(request, 'films/main.html')
def user_info(request):
    return render(request, 'films/user_info.html')
def user_form(request):
    return render(request, 'films/user_form.html')
def user_recommend(request):
    prod_name = request.POST.get('product')
    submitbutton =  request.POST.get('submit')
    context = {'prod_name': prod_name, 'submitbutton': submitbutton}
    return render(request, 'films/user_form.html', context)
