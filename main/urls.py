from django.urls import path
from .views import (
    submit_view, signup_view, login_view, logout_view,
    home_view, about_view, browse_view, contact_view, submissions_view,
    edit_recipe_view, delete_recipe_view,
    api_recipes_by_category, api_submit_recipe, contact_ajax, marketplace_home, marketplace_items, item_detail, create_item, edit_item ,delete_item, ajax_get_items ,ajax_submit_offer ,ajax_update_item_status , my_marketplace_items
)

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('about/', about_view, name='about'),
    path('browse/', browse_view, name='browse'),
    path('contact/', contact_view, name='contact'),
     path('contact/ajax/', contact_ajax, name='contact_ajax'),
    path('submissions/', submissions_view, name='submissions'),
    path('submit/', submit_view, name='submit'),
    path('edit/<int:recipe_id>/', edit_recipe_view, name='edit_recipe'),
    path('delete/<int:recipe_id>/', delete_recipe_view, name='delete_recipe'),

    # ✅ AJAX endpoints
    path('api/recipes/', api_recipes_by_category, name='api_recipes_by_category'),
    path('api/submit-recipe/', api_submit_recipe, name='api_submit_recipe'),
    path('marketplace/', marketplace_home, name='marketplace_home'),
    path('marketplace/items/', marketplace_items, name='marketplace_items'),
    path('marketplace/item/<int:item_id>/',item_detail, name='item_detail'),
    path('marketplace/create/', create_item, name='create_item'),
    path('marketplace/edit/<int:item_id>/',edit_item, name='edit_item'),
    path('marketplace/delete/<int:item_id>/',delete_item, name='delete_item'),
    # urls.py
path('marketplace/my-items/', my_marketplace_items, name='my_marketplace_items'),

    
    # AJAX endpoints
    path('marketplace/ajax/items/', ajax_get_items, name='ajax_get_items'),
    path('marketplace/ajax/offer/<int:item_id>/', ajax_submit_offer, name='ajax_submit_offer'),
    path('marketplace/ajax/status/<int:item_id>/', ajax_update_item_status, name='ajax_update_item_status'),
]