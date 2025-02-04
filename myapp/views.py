from django.shortcuts import render, redirect, get_object_or_404
from .models import User, DailyActivity, PersonalGoals, Journal
from django.contrib import messages
from .forms import DailyActivityForm, PersonalGoalsForm, JournalForm



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
            user = User.objects.get(username=text_uname)  # Look up user by username
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

def get_logged_in_user(request):
    """Returns the logged-in user or redirects to login if not authenticated."""
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "You need to log in first.")
        return None, redirect("login")  # Return None and redirect response

    user = get_object_or_404(User, id=user_id)  # Get user or return 404
    return user, None

def daily_activity_create(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    #Check if user is logged in
    # if "user_id" not in request.session:
    #     messages.error(request, "You need to log in first.")
    #     return redirect("login")  # Redirect to login if not logged in
    #
    # # Fetch the logged-in user
    # user_id = request.session["user_id"]
    # user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = DailyActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = user  # Link to the logged-in user manually
            activity.save()
            messages.success(request, "Daily activity recorded successfully!")
            return redirect("display_activity")  # Redirect to the display_activity page
    else:
        form = DailyActivityForm()
    return render(request, 'myapp/daily_activity.html', {'form': form})


def daily_activity_list_view(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    # # Check if user is logged in
    # if "user_id" not in request.session:
    #     messages.error(request, "You need to log in first.")
    #     return redirect("login")  # Redirect to login page
    #
    # # Fetch the logged-in user
    # user_id = request.session["user_id"]
    # user = User.objects.get(id=user_id)

    # Retrieve all daily activities for this user
    activities = DailyActivity.objects.filter(user=user).order_by('-date')  # Show newest first

    return render(request, 'myapp/display_daily_activity.html', {'activity_list': activities})

def daily_activity_delete(request,id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in
    # # Check if user is logged in
    # if "user_id" not in request.session:
    #     messages.error(request, "You need to log in first.")
    #     return redirect("login")  # Redirect to login page

    activity = DailyActivity.objects.get(id=id)
    activity.delete()
    messages.success(request, "Activity was deleted successfully!")
    return redirect('display_activity')


#Update View
def daily_activity_update(request, id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    # if "user_id" not in request.session:
    #     messages.error(request, "You need to log in first.")
    #     return redirect("login")  # Redirect to login page


    activity = DailyActivity.objects.get(id=id)
    form = DailyActivityForm(instance=activity)
    if request.method == "POST":
        form = DailyActivityForm(request.POST,instance=activity)
        if form.is_valid():
            form.save()
            return redirect('display_activity')
    return render(request, 'myapp/daily_activity.html', {'form':form})


def goal_create(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    if request.method == "POST":
        form = PersonalGoalsForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user  # Link to the logged-in user manually
            goal.save()
            messages.success(request, "Goal recorded successfully!")
            return redirect("display_goals")
    else:
        form = PersonalGoalsForm()
    return render(request, 'myapp/add_goal.html', {'form': form})


def goals_list_view(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response

    goals = PersonalGoals.objects.filter(user=user).order_by('-target_date')  # Show newest first

    return render(request, 'myapp/display_goals.html', {'goals_list': goals})

def goal_delete(request,id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    goal = PersonalGoals.objects.get(id=id)
    goal.delete()
    messages.success(request, "Goal was deleted successfully!")
    return redirect('display_goals')


#Update View
def goal_update(request, id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    goal = PersonalGoals.objects.get(id=id)
    form = PersonalGoalsForm(instance=goal)
    if request.method == "POST":
        form = PersonalGoalsForm(request.POST,instance=goal)
        if form.is_valid():
            form.save()
            return redirect('display_goals')
    return render(request, 'myapp/add_goal.html', {'form':form})


def journal_record_create(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    if request.method == "POST":
        form = JournalForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = user  # Link to the logged-in user manually
            record.save()
            messages.success(request, "Record added successfully!")
            return redirect("display_records")
    else:
        form = JournalForm()
    return render(request, 'myapp/add_journal_record.html', {'form': form})


def records_list_view(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response

    records = Journal.objects.filter(user=user).order_by('-entry_date')  # Show newest first

    return render(request, 'myapp/display_journal_records.html', {'records_list': records})


def record_delete(request,id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    record = Journal.objects.get(id=id)
    record.delete()
    messages.success(request, "Record deleted successfully!")
    return redirect('display_records')


#Update View
def record_update(request, id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response:
        return redirect_response  # Redirect if user is not logged in

    record = Journal.objects.get(id=id)
    form = JournalForm(instance=record)
    if request.method == "POST":
        form = JournalForm(request.POST,instance=record)
        if form.is_valid():
            form.save()
            return redirect('display_records')
    return render(request, 'myapp/add_journal_record.html', {'form':form})
