from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request, "myapp/index.html", {})


def menu(request):
    return render(request, "myapp/menu.html", {})


def signup(request):
    return render(request, "myapp/signup.html", {})


def insertuser(request):
    text_uname = request.POST['tuname']
    text_email = request.POST['tuemail']
    text_password = request.POST['tupassword']
    text_password2 = request.POST['tupassword2']

    if text_password != text_password2:
        messages.error(request, "Passwords do not match.")
        return redirect("/signup")

    if User.objects.filter(username=text_uname).exists():
        messages.error(request, "Username is already taken. Try another one.")
        return redirect("/signup")

    if User.objects.filter(email=text_email).exists():
        messages.error(request, "Email is already in use. Try logging in or use another email.")
        return redirect("/signup")

    ob = User(username=text_uname, email=text_email, password=text_password)
    ob.save()

    return redirect("/menu")


def login(request):
     return render(request, "myapp/login.html", {})

def loginuser(request):
    if request.method == "POST":
        text_uname = request.POST.get("tuname")
        text_password = request.POST.get("tupassword")

        try:
            user = User.objects.get(username=text_uname)  # Look up user by email
            if text_password == user.password:  # Compare passwords directly (⚠)
                request.session["user_id"] = user.id
                print(user.id)         # Manually set session
                messages.success(request, "Login successful!")
                return redirect("menu")
            else:
                messages.error(request, "Invalid username or password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, "myapp/login.html")


def logout(request):
    return render(request, "myapp/logout.html", {})


def logoutuser(request):
    if "user_id" in request.session:  # Check if the user is logged in
        del request.session["user_id"]  # Remove user from session
    messages.success(request, "You have been logged out.")
    return redirect("index")  # Redirect to login page after logout