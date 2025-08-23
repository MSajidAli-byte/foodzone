from urllib import request
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
 
from foodapp.models import Order, Profile, Dish, Category

from foodapp.models import Contact

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact_us(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        obj = Contact(name=name, email=email, subject=subject, message=message)
        obj.save()
        if obj:
            messages.success(request, 'Your message has been sent successfully!')
            # return HttpResponse(f"Thank you dear {name} for contacting us!")
        context['message'] = f"Thank you dear {name} for contacting us!"
        
    return render(request, 'contact.html', context)

def register(request):
    """
    Handles user registration:
    1. Receives user data (name, email, password, contact) via POST request
    2. Checks if user with same email already exists
    3. If not, creates a new User and associated Profile
    4. Returns registration success or error message
    
    GET requests simply render the registration form
    """
    context={}
    if request.method=="POST":
        
        #fetch data from html form
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        contact = request.POST.get('number')
        
        # check user with email as username from the database
        check = User.objects.filter(username=email)
        
        if len(check)==0:
            #Save data to both tables
            usr = User.objects.create_user(email, email, password) # create user based on email
            usr.first_name = name
            usr.save()

            profile = Profile(user=usr, contact = contact)
            profile.save()
            
            context['status'] = f"User {name} Registered Successfully!"
        else:
            context['error'] = f"A User with this email already exists"
            
    return render(request, 'register.html')

def check_user_exists(request):
    email = request.GET.get('usern')
    check = User.objects.filter(username=email)
    
    if len(check)==0:
        return JsonResponse({'status':0,'message':'Not Exist'})
    else:
        return JsonResponse({'status':1,'message':'A user with this email already exists!'})
    
def signin(request):
    context={}
    if request.method=="POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')

        check_user = authenticate(username=email, password=passw)
        if check_user:
            login(request, check_user)
            if check_user.is_superuser or check_user.is_staff:
                return HttpResponseRedirect('/admin')
            return HttpResponseRedirect('/dashboard')
        else:
            context.update({'message':'Invalid Login Details!','class':'alert-danger'})
            
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def dashboard(request):
    context = {}
    orders = Order.objects.filter(customer__user=request.user).order_by('-ordered_on')
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Handle profile update
        if "update_profile" in request.POST:
            name = request.POST.get('name')
            contact = request.POST.get('contact_number')
            address = request.POST.get('address')

            profile.user.first_name = name
            profile.user.save()

            profile.contact = contact
            profile.address = address

            if "profile_picture" in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, 'Profile updated successfully!')            
            return HttpResponseRedirect(request.path_info)  # Redirect after successful POST
            
            #Change Password 
        if "change_pass" in request.POST:
            c_password = request.POST.get('current_password')
            n_password = request.POST.get('new_password')

            if request.user.check_password(c_password):
                request.user.set_password(n_password)
                request.user.save()
                login(request, request.user)
                messages.success(request, 'Password Updated Successfully!')
            else:
                messages.error(request, 'Current Password Incorrect!')
            return HttpResponseRedirect(request.path_info)  # Redirect after successful POST

    context = {'profile': profile, 'orders': orders}
    return render(request, 'dashboard.html', context)

def feature(request):
    return render(request, 'feature.html')

def team(request):
    return render(request, 'team.html')

def menu(request):
    return render(request, 'menu.html')

def all_dishes(request):
    context={}
    dishes = Dish.objects.all()
    if "q" in request.GET:
        id = request.GET.get("q")
        dishes = Dish.objects.filter(category__id=id)
        context['dish_category'] = Category.objects.get(id=id).name 

    context['dishes'] = dishes
    return render(request,'all_dishes.html', context)

    # Integration with PayPal
    """ 
def single_dish(request, id):
    dish = get_object_or_404(Dish, id=id)
    context = {'dish': dish}

    # Only prepare a payment form for authenticated, non-admin users.
    if request.user.is_authenticated and not request.user.is_staff:
        cust = get_object_or_404(Profile, user=request.user)
        order = Order(customer=cust, item=dish)
        order.save()
        inv = f'INV0000-{order.id}'

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': dish.discounted_price,
            'item_name': dish.name,
            'invoice': inv,
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('payment_done')),
            'cancel_url': request.build_absolute_uri(reverse('payment_cancel')),
        }

        order.invoice_id = inv
        order.save()
        request.session['order_id'] = order.id

        form = PayPalPaymentsForm(initial=paypal_dict)
        context['form'] = form

    return render(request,'dish.html', context)
 """


from datetime import datetime, timedelta
import hmac, hashlib

def single_dish(request, id):
    dish = get_object_or_404(Dish, id=id)
    context = {'dish': dish}

    if request.method == "POST" and request.user.is_authenticated and not request.user.is_staff:
        cust = get_object_or_404(Profile, user=request.user)
        order = Order(customer=cust, item=dish)
        order.save()
        request.session['order_id'] = order.id

        # Prepare JazzCash payment data
        txn_datetime = datetime.now()
        expiry_datetime = txn_datetime + timedelta(hours=1)
        txn_ref_no = f"TXN{txn_datetime.strftime('%Y%m%d%H%M%S')}{order.id}"

        post_url = "https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagement/merchantform/"

        post_data = {
            "pp_Version": "1.1",
            "pp_TxnType": "",
            "pp_Language": "EN",
            "pp_MerchantID": settings.JAZZCASH_MERCHANT_ID,
            "pp_SubMerchantID": "",
            "pp_Password": settings.JAZZCASH_PASSWORD,
            "pp_BankID": "TBANK",
            "pp_ProductID": "RETL",
            "pp_TxnRefNo": txn_ref_no,
            "pp_Amount": str(int(dish.discounted_price * 100)),
            "pp_TxnCurrency": "PKR",
            "pp_TxnDateTime": txn_datetime.strftime("%Y%m%d%H%M%S"),
            "pp_BillReference": "billRef",
            "pp_Description": dish.name,
            "pp_TxnExpiryDateTime": expiry_datetime.strftime("%Y%m%d%H%M%S"),
            "pp_ReturnURL": request.build_absolute_uri(reverse('payment_done')),
            "pp_SecureHash": "",
            "ppmpf_1": cust.user.first_name,
            "ppmpf_2": "",
            "ppmpf_3": "",
            "ppmpf_4": "",
            "ppmpf_5": ""
        }

        ordered_keys = [
            "pp_Amount", "pp_BankID", "pp_BillReference", "pp_Description", "pp_Language",
            "pp_MerchantID", "pp_Password", "pp_ProductID", "pp_ReturnURL", "pp_SubMerchantID",
            "pp_TxnCurrency", "pp_TxnDateTime", "pp_TxnExpiryDateTime", "pp_TxnRefNo",
            "pp_TxnType", "pp_Version", "ppmpf_1", "ppmpf_2", "ppmpf_3", "ppmpf_4", "ppmpf_5"
        ]

        hash_string = '&'.join(f"{key}={post_data[key]}" for key in ordered_keys)
        secure_hash = hmac.new(
            settings.JAZZCASH_INTEGRITY_SALT.encode('utf-8'),
            hash_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()

        post_data["pp_SecureHash"] = secure_hash

        order.invoice_id = txn_ref_no
        order.save(update_fields=['invoice_id'])

        context['jazzcash_data'] = post_data
        context['post_url'] = post_url
        context['order'] = order

    return render(request, 'dish.html', context) 

 
@csrf_exempt
def payment_done(request):
    """Handle successful payment completion and update order status"""
    if request.method == "POST":
        # Extract JazzCash response fields
        txn_ref = request.POST.get('pp_TxnRefNo')
        response_code = request.POST.get('pp_ResponseCode')
        
        # print("\n\n\nResponse Code: ", response_code)
        
        # Only mark as paid if JazzCash says payment was successful
        if response_code:  
            try:
                order = Order.objects.get(invoice_id=txn_ref)
                order.status = True  # Mark as successful
                order.save()
                messages.success(request, "Your payment was successful! Order has been completed.")
            except Order.DoesNotExist:
                messages.error(request, "Order not found.")
        else:
            # Payment failed - mark as cancelled
            try:
                order = Order.objects.get(invoice_id=txn_ref)
                order.status = False  # Mark as failed/cancelled
                order.save()
                messages.error(request, "Payment failed or was cancelled.")
            except Order.DoesNotExist:
                messages.error(request, "Order not found.")
    else:
        # Handle GET requests (fallback)
        order_id = request.session.get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                # Check if this was a successful payment
                if order.status is None:  # Not yet processed
                    order.status = True  # Assume success for GET requests
                    order.save()
                    messages.success(request, "Your payment was successful! Order has been completed.")
            except Order.DoesNotExist:
                pass

    return render(request, 'payment_done.html')
@csrf_exempt
def payment_cancel(request):
    messages.warning(request, "Your payment was cancelled or failed.")
    return render(request, 'payment_cancel.html')

from django.views.decorators.http import require_POST

@require_POST
@login_required
def buy_dish(request, id):
    dish = get_object_or_404(Dish, id=id)
    if not dish.is_available or request.user.is_staff:
        messages.error(request, "You cannot buy this dish.")
        return redirect('dish', id=id)
    cust = get_object_or_404(Profile, user=request.user)
    order = Order(customer=cust, item=dish)
    order.save()
    request.session['order_id'] = order.id
    return redirect('process_jazzcash_payment', order_id=order.id)

@login_required
def clear_order(request, order_id):
    
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, customer__user=request.user)
        
        # Store the invoice id before deleting for showing message
        invoice_id = order.invoice_id
        
        order.delete()
        messages.success(request, f"Order {invoice_id} has been cleared.")
    return redirect('dashboard')