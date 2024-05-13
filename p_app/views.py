from django.shortcuts import render,redirect
from django.db import transaction
from .models import *
from django.db.models import Q
from django.contrib import messages
from . forms import checkoutform
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Lense
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf(request, order_id):
    # Retrieve order details based on order_id
    order = Orders.objects.get(pk=order_id)
    
    # Render HTML template for invoice
    template_path = 'invoice_template.html'
    context = {'order': order}
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Return PDF as response
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def admin_view(request):
    p = Lense.objects.all()
    context = {'P':p}
    return render(request,'admin_view.html',context)

def admin_lense_add(request):
    if request.method == "POST":
        name = request.POST['pname']
        desc = request.POST['pdesc']
        
        price = request.POST['pprice']
        quantity = request.POST['pquantity']
        image = request.FILES['pimage']
        category = request.POST['pcategory'] 
        cat=Category.objects.get(id=category)
        # Check if the price is valid
        if not price.isdigit() or int(price) <= 0:
            messages.error(request, "Please enter a valid price greater than 0.")
            return redirect('admin_add')
        if Lense.objects.filter(p_name=name).exists():
                messages.info(request,"Lens with this name already exists.")
                return redirect('admin_add')
        lense = Lense.objects.create(p_name = name,p_desc = desc,p_quantity = quantity,p_price = price,p_image = image,cat=cat)
        lense.save()
        messages.success(request, "Product Added Successfully!")
        return redirect('admin_view')
    cat=Category.objects.all()
    return render(request,'admin_lenseadd.html',{"cat":cat})

def update_lens(request, pk):
    lens = Lense.objects.get(pk=pk)
    if request.method == 'POST':
        lens.p_name = request.POST['pname']
        lens.p_desc = request.POST['pdesc']
        lens.category = Category.objects.get(id=request.POST['pcategory'])
        lens.p_quantity = request.POST['pquantity']
        lens.p_price = request.POST['pprice']
        if 'pimage' in request.FILES:
            lens.p_image = request.FILES['pimage']
        lens.save()
        return redirect('admin_view')
    categories = Category.objects.all()
    return render(request, 'admin_lenseupdate.html', {'lens': lens, 'cat': categories})


from decimal import Decimal
def admin_lense_update(request,pk):
    p = Lense.objects.get(pk=pk)
    
    if request.method == 'POST':
        if 'pname' in request.POST:
            p.p_name = request.POST['pname']
        if 'pdesc' in request.POST:
            p.p_desc = request.POST['pdesc']
        if 'pprice' in request.POST:
            price = request.POST['pprice']
            try:
                price = Decimal(price)
                if price <= 0:
                    messages.error(request, "Please enter a valid price greater than 0.")
                    return redirect('admin_update', pk=pk)
                p.p_price = price
            except ValueError:
                messages.error(request, "Please enter a valid numeric price.")
                return redirect('admin_update', pk=pk)
        if 'pquantity' in request.POST:
            p.p_quantity = request.POST['pquantity']
        if 'pimage' in request.FILES:
            p.p_image = request.FILES['pimage']
        
        p.save()

        messages.success(request, "Product Updated Successfully!")
        return redirect('admin_view')
    
    context = {'P': p}
    return render(request,'admin_lenseupdate.html',context)

def admin_lense_delete(request,pk):
    try:
        p = Lense.objects.filter(pk=pk)
        p.delete()
        messages.success(request,"Product Deleted Successfully!")
        return redirect('admin_view')
        # return HttpResponse("<h1 style='color:Black;text-align:center;margin-top:20%;'>Product Deleted Successfully</h1>")
    except Lense.DoesNotExist:
        messages.error(request,'Product Not Found')
        return redirect('admin_view')

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile_phone = request.POST.get('phone')

        # Check if the username already exists
        if UserDetails.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return render(request, 'register.html')

        if first_name and last_name and username and password and mobile_phone:
            user = UserDetails.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email = email,
                mobile_phone=mobile_phone
            )
            user.save()
            return redirect('login')
    
    return render(request, 'register.html')

     
def userLogin(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        user=UserDetails.objects.filter(email=email,password=password)
        admin=admin_login.objects.filter(username=email,password=password)

        if len(user) >= 1:
            request.session['user_id']=user[0].id
            return redirect('homepage')
        elif len(admin) >= 1:
            request.session['user_id']=admin[0].id
            return redirect('admin_view')

        else:
            messages.info(request,'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request,'login.html')
    
def home_page(request):
    p = Lense.objects.all()[:3]
    context = {'P':p}
    return render(request,'home.html',context)

def user_logout(request):
    del request.session['user_id']
    return redirect('homepage')

def allProducts(request):
    p = Lense.objects.all()
    context = {'P':p}
    return render(request,'shop.html',context)

def view_product(request,id):
    product=Lense.objects.get(p_id=id)
    return render(request,'product_detail.html',{'perfume':product})

def mycart(request):
    user_id = request.session['user_id']
    up = UserDetails.objects.get(id=int(user_id))
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart1 = cart.objects.get(id=cart_id)
    else:
        cart1 = None
    context = {'cart': cart1,'u':up}


    return render(request, 'mycart.html', context)

def addtocart(request, id):
    try:
        product_obj = Lense.objects.get(p_id=id)
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = cart.objects.get(id=cart_id)
            product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            # item already exist in cart
            if product_in_cart.exists():
                cartproduct = product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.p_price
                cartproduct.save()
                cart_obj.total += product_obj.p_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.p_price,
                                                        quantity=1, subtotal=product_obj.p_price)
                cart_obj.total += product_obj.p_price
                cart_obj.save()
        else:
                user_id = request.session['user_id']
                up = UserDetails.objects.get(id=int(user_id))
                cart_obj = cart.objects.create(customer=up,total=0)
                request.session['cart_id'] = cart_obj.id
                print("new cart")
                cp = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.p_price, quantity=1,
                                                        subtotal=product_obj.p_price)
                cart_obj.total += product_obj.p_price
                cart_obj.save()
    except:
        messages.error(request, "Login to add to Cart!")
    return redirect("/")

def managecart(request, id):
    print("im in manage cart")
    action = request.GET.get("action")
    cp_obj = CartProduct.objects.get(id=id)
    cart_obj = cp_obj.cart

    if action == "inc":
        cp_obj.quantity += 1
        cp_obj.subtotal += cp_obj.rate
        cp_obj.save()
        cart_obj.total += cp_obj.rate
        cart_obj.save()
    elif action == "dcr":
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart_obj.total -= cp_obj.rate
        cart_obj.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
            del request.session['cart_id']
    elif action == 'rmv':
        cart_obj.total -= cp_obj.subtotal
        cart_obj.save()
        cp_obj.delete()
    else:
        pass
    return redirect('/my-cart')

def emptycart(request):
    cart_id=request.session.get("cart_id",None)
    cart1=cart.objects.get(id=cart_id)
    cart1.cartproduct_set.all().delete()
    cart1.total=0
    cart1.save()

    return redirect('/my-cart')

def checkout(request):
    user_id=request.session['user_id']
    user=UserDetails.objects.get(id=user_id)
    cart_id = request.session.get("cart_id")
    cart_obj = cart.objects.get(id=cart_id)
    form = checkoutform(request.POST)
    if request.method == "POST":
        order_status = "Order recived"
        address = request.POST["address"]
        mobile =request.POST["contact"]
        total = request.POST["total"]
        with transaction.atomic():
            cart_products = CartProduct.objects.filter(cart=cart_obj)
            for cart_product in cart_products:
                product = cart_product.product
                product.p_quantity -= cart_product.quantity
                product.save()
        new_order = Orders.objects.create(cart=cart_obj, customer=user, address=address, mobile=mobile,
                                              total=total, order_status=order_status)
        new_order.save()
        del request.session['cart_id']
        messages.info(request,"Order Placed")
        return redirect('/')
    else:
        context = {'cart': cart_obj, 'form': form,'user': user}
        return render(request, 'checkout.html', context)

def my_orders(request):
    user_id = request.session['user_id']
    up = UserDetails.objects.get(id=int(user_id))
    
    user_orders = Orders.objects.filter(customer=up).order_by('-created_at')

    return render(request, 'my_orders.html', {'user_orders': user_orders})

def searchresult(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Lense.objects.all().filter(Q(p_name__contains=query) | Q(p_desc__contains=query) | Q(p_fragrance__contains=query) | Q(p_desc__contains=query))
        return render(request, 'search.html', {'query': query, 'products': products})
    
@login_required
def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Lense, p_id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        return redirect('wishlist')
    else:
        # Handle the case where the request method is not POST (optional)
        return render(request, 'shop.html')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Lense, p_id=product_id)  # Assuming 'p_id' is the primary key of Perfume model
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')


def display_orders(request):
    orders = Orders.objects.all()
    context = {'orders': orders, 'ORDER_STATUS': ORDER_STATUS}
    return render(request, 'display_orders.html', context)


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = Orders.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order.order_status = new_status
        order.save()
    return redirect('display_orders')


from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .models import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View


class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.password + str(timestamp)
        )



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserDetails.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = CustomTokenGenerator().make_token(user)
            reset_password_url = request.build_absolute_uri('/reset_password/{}/{}/'.format(uid, token))
            email_subject = 'Reset Your Password'

            # Render both HTML and plain text versions of the email
            email_body_html = render_to_string('reset_password_email.html', {
                'reset_password_url': reset_password_url,
                'user': user,
            })
            email_body_text = "Click the following link to reset your password: {}".format(reset_password_url)

            # Create an EmailMultiAlternatives object to send both HTML and plain text versions
            email = EmailMultiAlternatives(
                email_subject,
                email_body_text,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.attach_alternative(email_body_html, 'text/html')  # Attach HTML version
            email.send(fail_silently=False)

            messages.success(request, 'An email has been sent to your email address with instructions on how to reset your password.')
            return redirect('login')
        except UserDetails.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    return render(request, 'forgot_password.html')



def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserDetails.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserDetails.DoesNotExist):
        user = None

    if user is not None and CustomTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                # Update the password hash manually
                user.password = new_password
                user.save()
                messages.success(request, "Password reset successfully. You can now login with your new password.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'reset_password.html')
    else:
        messages.error(request, "Invalid reset link. Please try again or request a new reset link.")
        return redirect('login')
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Lense)

def check_quantity_and_send_email(sender, instance, created, **kwargs):
    if int(instance.p_quantity) < 5:
        subject = 'Low Quantity Alert'
        message = f"The quantity of {instance.p_name} is now {instance.p_quantity}. Please restock."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)

def low_quantity_products(request):
    low_quantity_lenses = Lense.objects.filter(p_quantity__lt=5)
    return render(request, 'low_quantity_products.html', {'low_quantity_lenses': low_quantity_lenses})
