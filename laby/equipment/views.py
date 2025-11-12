from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Equipment, Supplier, UsageRecord, Alert
from .decorators import admin_required, staff_required, viewer_allowed
from .forms import RegisterForm


# 🏠 Home page — show few equipments
def home(request):
    equipments = Equipment.objects.all()[:5]
    return render(request, 'equipment/home.html', {'equipments': equipments})


# 📋 Equipment list — visible to all
# (Temporarily removed decorators while testing)
def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipment/list.html', {'equipments': equipments})


# 🔍 Equipment detail
def equipment_detail(request, id):
    eq = get_object_or_404(Equipment, id=id)
    alerts = eq.alerts.all()
    return render(request, 'equipment/detail.html', {'equipment': eq, 'alerts': alerts})


# ➕ Add new equipment (Admin, Staff)
def equipment_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        quantity = request.POST['quantity']
        location = request.POST['location']
        condition = request.POST['condition']
        description = request.POST['description']
        Equipment.objects.create(
            name=name,
            category=category,
            quantity=quantity,
            location=location,
            condition=condition,
            description=description,
        )
        return redirect('equipment_list')
    return render(request, 'equipment/add.html')


# ✏️ Edit equipment (Admin, Staff)
def equipment_edit(request, id):
    eq = get_object_or_404(Equipment, id=id)
    if request.method == 'POST':
        eq.name = request.POST['name']
        eq.category = request.POST['category']
        eq.quantity = request.POST['quantity']
        eq.location = request.POST['location']
        eq.condition = request.POST['condition']
        eq.description = request.POST['description']
        eq.save()
        return redirect('equipment_detail', id=id)
    return render(request, 'equipment/edit.html', {'equipment': eq})


# ❌ Delete equipment (Admin only)
def equipment_delete(request, id):
    eq = get_object_or_404(Equipment, id=id)
    eq.delete()
    return redirect('equipment_list')


# 🧍 Register new user
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'equipment/register.html', {'form': form})
