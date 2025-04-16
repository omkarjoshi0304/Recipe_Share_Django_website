from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .models import Recipe
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import ContactForm
from .models import ContactMessage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ContactForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import MarketplaceItem, ItemCategory, ItemReview, ItemOffer
from .forms import ItemForm, ItemReviewForm, ItemOfferForm, ItemCategoryForm
from django.contrib.auth.decorators import login_required
from .models import MarketplaceItem

@login_required
def my_marketplace_items(request):
    items = MarketplaceItem.objects.filter(seller=request.user).prefetch_related('offers')
    return render(request, 'main/marketplace/my_items.html', {
        'items': items
    })


def marketplace_home(request):
    categories = ItemCategory.objects.all()
    latest_items = MarketplaceItem.objects.filter(is_available=True).order_by('-date_posted')[:8]
    return render(request, 'main/marketplace/home.html', {
        'categories': categories,
        'latest_items': latest_items
    })

def marketplace_items(request):
    items = MarketplaceItem.objects.filter(is_available=True).order_by('-date_posted')
    categories = ItemCategory.objects.all()
    
    # Filter by category if requested
    category_id = request.GET.get('category')
    if category_id:
        items = items.filter(category_id=category_id)
    
    return render(request, 'main/marketplace/items.html', {
        'items': items,
        'categories': categories,
        'selected_category': category_id
    })

@login_required(login_url='login')
def item_detail(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id)
    reviews = item.reviews.all().order_by('-date_posted')
    review_form = ItemReviewForm(request.POST or None)
    offer_form = ItemOfferForm()

    if request.method == 'POST':
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.item = item
            new_review.reviewer = request.user
            new_review.save()
            return redirect('item_detail', item_id=item_id)

    user_has_offer = ItemOffer.objects.filter(item=item, buyer=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'main/marketplace/item_detail.html', {
        'item': item,
        'reviews': reviews,
        'review_form': review_form,
        'offer_form': offer_form,
        'user_has_offer': user_has_offer
    })

@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm()
    
    return render(request, 'main/marketplace/create_item.html', {'form': form})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id)
    
    # Ensure only the seller can edit
    if item.seller != request.user and not request.user.is_staff:
        return redirect('item_detail', item_id=item.id)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'main/marketplace/edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id)
    
    # Ensure only the seller can delete
    if item.seller != request.user and not request.user.is_staff:
        return redirect('item_detail', item_id=item.id)
    
    if request.method == 'POST':
        item.delete()
        return redirect('marketplace_items')
    
    return render(request, 'main/marketplace/delete_item.html', {'item': item})

# AJAX views for Q3
@login_required
@require_POST
def ajax_submit_offer(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id)
    
    # Prevent offering on own items
    if item.seller == request.user:
        return JsonResponse({
            'success': False,
            'errors': ['You cannot make an offer on your own item']
        }, status=400)
    
    form = ItemOfferForm(request.POST)
    if form.is_valid():
        offer = form.save(commit=False)
        offer.item = item
        offer.buyer = request.user
        offer.save()
        
        return JsonResponse({
            'success': True,
            'offer_id': offer.id,
            'offer_price': float(offer.offer_price),
            'message': 'Your offer has been submitted successfully!'
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)

def ajax_get_items(request):
    """AJAX endpoint to get filtered items"""
    category_id = request.GET.get('category')
    max_price = request.GET.get('max_price')
    condition = request.GET.get('condition')
    search = request.GET.get('search')
    
    items = MarketplaceItem.objects.filter(is_available=True)
    
    if category_id:
        items = items.filter(category_id=category_id)
    
    if max_price:
        try:
            max_price = float(max_price)
            items = items.filter(price__lte=max_price)
        except ValueError:
            pass
    
    if condition:
        items = items.filter(condition=condition)
        
    if search:
        items = items.filter(title__icontains=search)
    
    items_data = [{
        'id': item.id,
        'title': item.title,
        'price': float(item.price),
        'condition': item.get_condition_display(),
        'image_url': item.image.url if item.image else None,
        'seller': item.seller.username,
        'date_posted': item.date_posted.strftime('%b %d, %Y'),
        'url': f'/marketplace/item/{item.id}/'
    } for item in items]
    
    return JsonResponse({
        'success': True,
        'items': items_data
    })

@login_required
@require_POST
def ajax_update_item_status(request, item_id):
    """AJAX endpoint to update item availability status"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Not authorized'}, status=401)
        
    item = get_object_or_404(MarketplaceItem, id=item_id)
    
    # Only the seller can update status
    if item.seller != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Not authorized'}, status=403)
    
    is_available = request.POST.get('is_available') == 'true'
    item.is_available = is_available
    item.save()
    
    return JsonResponse({
        'success': True,
        'is_available': item.is_available,
        'message': f'Item marked as {"available" if is_available else "unavailable"}'
    })


@require_POST
def contact_ajax(request):
    """View that only handles AJAX POST requests and returns JSON"""
    form = ContactForm(request.POST)
    if form.is_valid():
        try:
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()
            return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
        except Exception as e:
            print(f"Error in contact form: {e}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@ensure_csrf_cookie
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        # Check for AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json'
        
        if form.is_valid():
            try:
                contact = form.save(commit=False)
                if request.user.is_authenticated:
                    contact.user = request.user
                contact.save()
                
                # If this is an AJAX request, return JSON
                if is_ajax or request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
                else:
                    # For regular form submissions, redirect to success page or show success message
                    return render(request, 'main/contact.html', {
                        'form': ContactForm(),
                        'success_message': 'Your message has been sent successfully!'
                    })
            except Exception as e:
                print(f"Error in contact form: {e}")
                if is_ajax or request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'success': False, 'message': 'Server error occurred'}, status=500)
                else:
                    return render(request, 'main/contact.html', {
                        'form': form,
                        'error_message': 'Server error occurred'
                    })
        else:
            if is_ajax or request.headers.get('Accept') == 'application/json':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            else:
                return render(request, 'main/contact.html', {'form': form})
    
    # GET request: show the form
    form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "main/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})

@login_required
def home_view(request):
    return render(request, "main/index.html")
def about_view(request):
    return render(request, "main/about.html")
def browse_view(request):
    return render(request, "main/browse.html")
def contact_view(request):
    return render(request, "main/contact.html")
def submissions_view(request):
    return render(request, "main/submissions.html")


@login_required
def submit_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # assign logged-in user
            recipe.save()
            return redirect('browse')
    else:
        form = RecipeForm()
    
    return render(request, 'main/submit.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("login")

from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

@login_required
def submit_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'main/submit.html', {'form': form})


from .models import Recipe

def browse_view(request):
    category = request.GET.get('category')
    if category:
        recipes = Recipe.objects.filter(category=category)
    else:
        recipes = Recipe.objects.all()
    categories = ['breakfast', 'lunch', 'dinner', 'snack', 'dessert', 'beverage']
    return render(request, 'main/browse.html', {
        'recipes': recipes,
        'categories': categories,
        'selected_category': category
    })

from django.shortcuts import get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('browse')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'main/edit_recipe.html', {'form': form})


@login_required
def delete_recipe_view(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id, user=request.user)
    except Recipe.DoesNotExist:
        # Redirect to browse or raise a nicer error
        return redirect('browse')

    if request.method == 'POST':
        recipe.delete()
        return redirect('browse')

    return render(request, 'main/confirm_delete.html', {'recipe': recipe})
from django.http import JsonResponse
from .models import Recipe
from .forms import RecipeForm
from django.views.decorators.csrf import csrf_exempt

def api_recipes_by_category(request):
    category = request.GET.get("category")
    recipes = Recipe.objects.filter(category=category).values("name", "email", "ingredients", "duration", "category", "uploaded_file")
    return JsonResponse(list(recipes), safe=False)

@csrf_exempt
def api_submit_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user if request.user.is_authenticated else None
            recipe.save()
            return JsonResponse({"success": True, "message": "Recipe submitted successfully."})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)

# submission page 
@login_required
def submissions_view(request):
    user = request.user
    user_recipes = Recipe.objects.filter(user=user).order_by('-created_at')
    context = {
        'recipes': user_recipes,
        'total': user_recipes.count()
    }
    return render(request, 'main/submissions.html', context)