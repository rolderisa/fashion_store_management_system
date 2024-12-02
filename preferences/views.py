from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import CustomerPreference
from .forms import CustomerPreferenceForm,add
import logging

import traceback

logger = logging.getLogger(__name__)



@login_required
def customer_preference(request):
    try:
        preference, created = CustomerPreference.objects.get_or_create(user=request.user)
        logger.info(f"Preference fetched: {preference}, Created: {created}")  # Debugging log

        if request.method == 'POST':
            form = CustomerPreferenceForm(request.POST, instance=preference)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Preferences saved successfully'})
            else:
                logger.error(f"Form errors: {form.errors}")  # Log form errors
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        else:
            form = CustomerPreferenceForm(instance=preference)
        
        return render(request, 'preferences/customer_preference.html', {'form': form})

    except Exception as e:
        logger.error(f"Error in customer_preference view: {str(e)}")
        logger.error(traceback.format_exc())  # Log the full traceback
        return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your preferences.'}, status=500)
@login_required
def view_preference(request):
    try:
        # Ensure preference exists for the user
        preference = get_object_or_404(CustomerPreference, user=request.user)
        return render(request, 'preferences/view_preference.html', {'preference': preference})
    except Exception as e:
        logger.error(f"Error in view_preference view: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred while fetching your preferences.'}, status=500)

@login_required
@require_POST
def update_preference(request):
    try:
        preference = get_object_or_404(CustomerPreference, user=request.user)
        form = CustomerPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Preferences updated successfully'})
        else:
           
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    except Exception as e:
        logger.error(f"Error in update_preference view: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred while updating your preferences.'}, status=500)

def add_preference(request):
    if request.method == 'POST':
        form = CustomerPreferenceForm(request.POST)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.user = request.user  
            preference.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Preferences saved successfully.'
                })

            return redirect('preferences:view_preference')
        else:
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                })

    else:
        form = CustomerPreferenceForm()

    return render(request, 'preferences/add_preferences.html', {'form': form})