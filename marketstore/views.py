from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Category, ItemImage, Message
from django.contrib.auth.models import User


from django.db.models import Q

def about_view(request):
    return render(request, "about.html")

def contact_view(request):
    return render(request, "contact.html")

def homepage_view(request):
    query = request.GET.get("q")
    if query:
        items = Item.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            status="available",
            is_sold=False
        ).order_by("-date_posted")
    else:
        items = Item.objects.filter(status="available", is_sold=False).order_by("-date_posted")[:9]

    return render(request, "homepage.html", {"items": items, "query": query})


# ────────────────────────────────────────────
# AUTH
# ────────────────────────────────────────────

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect("item_list")
    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("item_list")
        messages.error(request, "Invalid credentials")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

# ────────────────────────────────────────────
# ITEMS
# ────────────────────────────────────────────

def item_list_view(request):
    items = Item.objects.filter(status="available", is_sold=False).order_by("-date_posted")
    q = request.GET.get("q")
    if q:
        items = items.filter(title__icontains=q)
    return render(request, "item_list.html", {"items": items})


def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.views_count += 1
    item.save(update_fields=["views_count"])
    return render(request, "item_detail.html", {"item": item})


@login_required(login_url='login')
def contact_seller_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(sender=request.user, receiver=item.seller, item=item, content=content)
            messages.success(request, "Message sent!")
    return redirect("item_detail", pk=pk)

@login_required(login_url='login')
def create_item_view(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        negotiable = bool(request.POST.get("negotiable"))
        category_id = request.POST.get("category")
        condition = request.POST.get("condition")
        location = request.POST.get("location")
        images = request.FILES.getlist("images")

        category = get_object_or_404(Category, pk=category_id)
        item = Item.objects.create(
            title=title,
            description=description,
            price=price,
            negotiable=negotiable,
            category=category,
            condition=condition,
            seller=request.user,
            location=location,
            is_sold=False,  # override default True in model
        )
        for idx, img in enumerate(images):
            ItemImage.objects.create(item=item, image=img, is_primary=(idx == 0))
        messages.success(request, "Item listed!")
        return redirect("item_detail", pk=item.pk)

    context = {"categories": categories, "condition_choices": Item.CONDITION_CHOICES}
    return render(request, "item_create.html", context)

@login_required(login_url='login')
def purchase_item_view(request, pk):
    item = get_object_or_404(Item, pk=pk, status="available", is_sold=False)
    if item.seller == request.user:
        messages.warning(request, "You can’t buy your own item.")
        return redirect("item_detail", pk=pk)

    if request.method == "POST":
        item.status = "sold"
        item.is_sold = True
        item.save(update_fields=["status", "is_sold"])
        messages.success(request, "Purchase successful!")
        return redirect("item_detail", pk=pk)

    return render(request, "item_purchase.html", {"item": item})


# ────────────────────────────────────────────
# USER VIEWS (ADDED)
# ────────────────────────────────────────────

@login_required(login_url='login')
def seller_dashboard_view(request):
    items = Item.objects.filter(seller=request.user).order_by("-date_posted")
    return render(request, "seller_dashboard.html", {"items": items})

@login_required(login_url='login')
def seller_messages_view(request):
    messages_received = Message.objects.filter(receiver=request.user).select_related("item", "sender").order_by("-sent_date")
    return render(request, "seller_messages.html", {"messages": messages_received})

@login_required(login_url='login')
def buyer_purchases_view(request):
    purchased_items = Item.objects.filter(status="sold", is_sold=True, messages__sender=request.user).distinct()
    return render(request, "buyer_purchases.html", {"items": purchased_items})