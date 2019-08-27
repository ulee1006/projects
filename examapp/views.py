from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def main(request):
    return redirect('/main')

def index(request):
    return render(request, "index.html")


def validate_login(request):
    errors = User.objects.loginValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/main')
    else:
        user_list = User.objects.filter(username=request.POST['username'])
        user = user_list[0]
        request.session['id'] = user.id
        return redirect('/dashboard')

def procregister(request):
    print(request.POST)
    errors=User.objects.regvalidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/main")
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user=User.objects.create(name=request.POST['name'],username=request.POST['username'],password=hash.decode())
        request.session['id']=user.id
        request.session['name']=user.name
        request.session['logged']=True
        request.session['password']=user.password

        return redirect("/dashboard")

def dashboard(request):
    if 'id' not in request.session:
        return redirect("/main")
    else:
        currentuser = User.objects.get(id=request.session["id"])
        all_plans = Plan.objects.all()
        user_plans = currentuser.plans.all()
        join = all_plans.difference(user_plans)
        context = {
            'user':currentuser,
            'userplans' : user_plans,
            'join' : join,
            
        }
        return render(request, "dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect('/main')
    
def add_plan(request):
    if 'id' not in request.session:
        return redirect("/main")
    else:
        return render(request, "addplan.html")

def create_plan(request):
    errors = Plan.objects.planvalidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_plan')
    else:
        plan=Plan.objects.create(destination=request.POST["destination"], description=request.POST["description"], travelstart=request.POST['travelstart'], travelend=request.POST['travelend'], added_by_id=request.session['id'])
        user = User.objects.get(id=request.session["id"])
        user.plans.add(plan)
        return redirect('/dashboard')

def show_plan(request, id):
    if 'id' not in request.session:
        return redirect("/main")
    else:
        plan=Plan.objects.get(id=id)
        users = plan.users.all()
        logged_in_user = User.objects.filter(id=plan.added_by_id)
        diff = users.difference(logged_in_user)
        context = {
            'plan': plan,
            # "all":allusers,
            "diff": diff
        }
        return render(request, "showplan.html", context)

def join_plan(request, plan_id):
    user = User.objects.get(id=request.session["id"])
    plan = Plan.objects.get(id=plan_id)
    user.plans.add(plan)
    return redirect("/dashboard")


