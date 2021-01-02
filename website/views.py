from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def contact(request):
    if request.method == 'POST':
        message_name = request.POST['message.name']
        message_email = request.POST['message.email']
        message = request.POST['message']  
        return render(request, 'contact.html', {'message_name': message_name})

    else:
        return render(request, 'contact.html', {})

def gallery(request):
    return render(request, 'gallery.html', {})

def products(request):
    return render(request, 'products.html', {})

def test(request):
    return render(request, 'test.html', {})
