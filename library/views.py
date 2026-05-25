from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        User.objects.create_user(
            username=username, 
            email=email, 
            password=password
            )
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')