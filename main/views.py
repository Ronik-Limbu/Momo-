from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Contact,Foods,Category,Cart
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string

# Create your views here.
date = datetime.now()
# @login_required(login_url='login')
def index(request):
    date = datetime.now()  # Get the current date and time

    # Initialize the food categories
    drink_category = Category.objects.filter(name='Drinks').first()  # Use .first() to avoid DoesNotExist exception
    snack_category = Category.objects.filter(name='snaks').first()    # Use .first() to avoid DoesNotExist exception
    lunch_category = Category.objects.filter(name='Lunch').first()    # Use .first() to avoid DoesNotExist exception

    # Retrieve foods based on categories
    drinks = Foods.objects.filter(category=drink_category) if drink_category else []
    snacks = Foods.objects.filter(category=snack_category) if snack_category else []
    lunch = Foods.objects.filter(category=lunch_category) if lunch_category else []

    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        msg = request.POST.get('message')

        # Create a new Contact entry
        Contact.objects.create(name=name, email=email, phone=phone, message=msg)

        # Prepare the email
        subject = 'Python with Django Training'
        message = render_to_string('main/msg.html', {'name': name, 'date': date, 'phone': phone})
        from_email = 'limburonik4@gmail.com'
        recipient_list = [email]

        # Send the email
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request, 'Your form has been submitted successfully.')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')

        return redirect('index')

    # Render the index page with foods and categories
    return render(request, 'main/index.html', {
        'date': date,
        'drinks': drinks,
        'snacks': snacks,
        'lunch': lunch,
    })

def about(request):
    return render(request, 'main/about.html', {'date': date})



    
def contact(request):
    return render(request, 'main/contact.html', {'date': date})

# def menu(request):
#     try:
#         drink_category = Category.objects.get(name='Drinks')  # Match the casing
#         snack_category = Category.objects.get(name='snaks')   # Match the casing
#         lunch_category = Category.objects.get(name='Lunch')    # Match the casing
#     except Category.DoesNotExist:
#         drink_category = snack_category = lunch_category = None

#     # Retrieve foods based on categories
#     drinks = Foods.objects.filter(category=drink_category) if drink_category else []
#     snacks = Foods.objects.filter(category=snack_category) if snack_category else []
#     lunch = Foods.objects.filter(category=lunch_category) if lunch_category else []

#     # Debugging output
#     print("Drinks:", drinks)  # Check what foods are retrieved for drinks
#     print("Snaks:", snacks)  # Check what foods are retrieved for snacks
#     print("Lunch:", lunch)     # Check what foods are retrieved for lunch

#     return render(request, 'main/menu.html', {
#         'drinks': drinks,
#         'snacks': snacks,
#         'lunch': lunch
#     })

@login_required(login_url='login')
def services(request):
    return render(request, 'main/services.html', {'date': date})

def Register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('Register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('Register')
            else:
                # Create a new user
                User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=confirm_password)
                return redirect('login')
        else:
            messages.error(request, "Password and confirm password do not match!")
            return redirect("Register")
    return render(request, 'auth/Register.html', {'date': date})

def log_in(request):
    if request.method=='POST':
       username=request.POST['username']
       password=request.POST['password']

       user=authenticate(username=username,password=password)
       if not User.objects.filter(username=username).exists():
           messages.info(request,"username is not found")
       if user is not None:
          login(request,user)
          return redirect('index')
          
    return render(request, 'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
           form.save()
           return redirect('log_in')
    return render(request,'auth/change_password.html',{'form':form})





from django.http import JsonResponse

@login_required(login_url='login')
def add_to_cart(request, food_id):
    if request.method == 'POST':
        try:
            food_item = Foods.objects.get(id=food_id)
            cart_item, created = Cart.objects.get_or_create(user=request.user, food_item=food_item)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return JsonResponse({'success': True})
        except Foods.DoesNotExist:
            return JsonResponse({'error': 'Food item not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='login')  # Ensure user is logged in
def get_cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return JsonResponse({'count': count})


@login_required(login_url='login')
def get_cart_count(request):
    count = Cart.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})


def cart_view(request):
    """Display the cart items for the logged-in user."""
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        # Calculate total price for each cart item
        for item in cart_items:
            item.total_price = item.food_item.price * item.quantity  # Calculate total price for each item
        total_price = sum(item.total_price for item in cart_items)  # Calculate overall total price

        return render(request, 'main/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
        })
    else:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('login')

def update_cart(request, cart_item_id):
    """Update the quantity of a specific cart item."""
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
            return redirect('cart')
        except Cart.DoesNotExist:
            messages.error(request, 'Cart item not found.')
            return redirect('cart')

def remove_from_cart(request, cart_item_id):
    """Remove a specific item from the cart."""
    if request.method == 'POST':
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            cart_item.delete()
            messages.success(request, 'Item removed from cart successfully!')
            return redirect('cart')
        except Cart.DoesNotExist:
            messages.error(request, 'Cart item not found.')
            return redirect('cart')

@login_required(login_url='login')
def rate_food(request, food_id):
    """Handle star rating submission for a food item."""
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        try:
            food_item = Foods.objects.get(id=food_id)
            # Check if the user has already rated this food item
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                food_item=food_item,
                defaults={'rating': rating_value}  # Update rating if it exists
            )

            if created:
                messages.success(request, 'Rating submitted successfully!')
            else:
                messages.info(request, 'Your rating has been updated.')

            return JsonResponse({'success': True})
        except Foods.DoesNotExist:
            return JsonResponse({'error': 'Food item not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def proceed_to_payment(request):
    """Redirect to the payment page."""
    return render(request, 'payment.html') 




from django.shortcuts import render, redirect, get_object_or_404
from .models import Foods, Review


def menu(request):
    drinks = Foods.objects.filter(category__name='Drinks')
    snacks = Foods.objects.filter(category__name='Snacks')
    lunch = Foods.objects.filter(category__name='Lunch')

    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        rating_value = request.POST.get('rating')
        food_item = get_object_or_404(Foods, id=food_id)
        
        # Save the rating
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            food_item=food_item,
            defaults={'rating': rating_value}
        )
        return redirect('menu')  # Redirect to menu or wherever you want

    context = {
        'drinks': drinks,
        'snacks': snacks,
        'lunch': lunch,
    }
    return render(request, 'main/menu.html', context)

@login_required(login_url='login')
def food_details(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.food = food
            review.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ReviewForm()

    return render(request, 'food_details.html', {'Food': food, 'form': form})


