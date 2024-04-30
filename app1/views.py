from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
import bcrypt


def registration(request):
    user_id = request.session.get("user_id")

    if user_id:
        return redirect("app1:dashboard")

    return render(request, "registration.html")


def register(request):
    if request.method == "POST":

        errors = User.objects.validate(request.POST)

        # There is some errors
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("app1:registration")

        # بنستخرج المدخلات من الفورم
        first_name_form = request.POST["first_name"]
        last_name_form = request.POST["last_name"]
        email_form = request.POST["email"]
        password_form = request.POST["password1"]
        confirm_password_form = request.POST["password2"]

        if password_form == confirm_password_form:
            hash_password = bcrypt.hashpw(
                password_form.encode(), bcrypt.gensalt()
            ).decode()

            new_user = User.objects.create(
                first_name=first_name_form,
                last_name=last_name_form,
                email=email_form,
                password=hash_password,
            )

            request.session["user_id"] = new_user.id
            request.session["first_name"] = new_user.first_name

            return redirect("app1:dashboard")

        # if password didn't match
        else:
            messages.error(request, "Password not match.")
            return redirect("app1:registration")


def login(request):
    if request.method == "POST":
        email_form = request.POST["email"]
        password_form = request.POST["password1"]

        users = User.objects.filter(email=email_form)

        if len(users) == 0:
            messages.error(request, "Email doesn't exist.")
            return redirect("app1:registration")

        if bcrypt.checkpw(password_form.encode(), users.first().password.encode()):
            request.session["user_id"] = users[0].id
            request.session["first_name"] = users[0].first_name

            return redirect("app1:dashboard")
        # if password is wrong
        else:
            messages.error(request, "Password not correct.")
            return redirect("app1:registration")


def logout(request):
    request.session.flush()
    return redirect("app1:registration")


def dashboard(request):
    all_trips = Trip.objects.all()
    user = User.objects.get(id=request.session["user_id"])

    context = {"trips": all_trips, "current_user": user}
    return render(request, "dashboard.html", context)


def new_trip(request):
    return render(request, "newtrip.html")


def add(request):
    destination_form = request.POST["destination"]
    start_date_form = request.POST["start_date"]
    end_date_form = request.POST["end_date"]
    Itinerary_form = request.POST["Itinerary"]

    errors = Trip.objects.validate(request.POST)

    # There is some errors
    if len(errors) > 0:
        for error in errors.values():
            messages.error(request, error)
        return redirect("app1:new_trip")

    user = User.objects.get(id=request.session["user_id"])

    Trip.objects.create(
        start_date=start_date_form,
        end_date=end_date_form,
        destination=destination_form,
        Itinerary=Itinerary_form,
        organizer=user,
    )

    return redirect("app1:dashboard")


def view_trip(request, pk):
    trip = Trip.objects.get(pk=pk)
    context = {
        "trip": trip,
    }
    return render(request, "if_organized_by.html", context)


def edit(request, pk):
    destination_form = request.POST["destination"]
    start_date_form = request.POST["start_date"]
    end_date_form = request.POST["end_date"]
    Itinerary_form = request.POST["Itinerary"]

    trip = Trip.objects.get(pk=pk)

    trip.start_date = start_date_form
    trip.end_date = end_date_form
    trip.Itinerary = Itinerary_form
    trip.destination = destination_form

    trip.save()

    return redirect("app1:dashboard")


def delete(request, pk):
    trip = Trip.objects.get(pk=pk)
    trip.delete()
    return redirect("app1:dashboard")



def details(request, pk):
    trip = Trip.objects.get(pk=pk)
    context = {
        'trip': trip
    }
    return render(request, "if_not_organized_by.html", context)


def my_trips(request):
    user = User.objects.get(id=request.session["user_id"])
    
    my_trips = Trip.objects.filter(travelers=user)
    other_trips = Trip.objects.all().exclude(travelers=user)
    
    context = {
        'my_trips': my_trips,
        'other_trips': other_trips
    }
    
    return render(request, "mytrip.html", context)



def join(request, pk):
    user = User.objects.get(id=request.session["user_id"])
    trip = Trip.objects.get(id=pk)
    
    trip.travelers.add(user)
    
    return redirect("app1:my_trips")


def cancel(request, pk):
    user = User.objects.get(id=request.session["user_id"])
    trip = Trip.objects.get(id=pk)
    
    trip.travelers.remove(user)
    
    return redirect("app1:my_trips")