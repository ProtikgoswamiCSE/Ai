from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import pickle
import io
from .models import AnalysisResult

def home(request):
    return render(request, 'analyzer/home.html')

@csrf_exempt
def analyze_data(request):
    if request.method == 'POST':
        try:
            # Get form data
            gender = request.POST.get('gender', '-')
            age = request.POST.get('age', '-')
            ns1 = int(request.POST.get('ns1', 0))
            igg = int(request.POST.get('igg', 0))
            igm = int(request.POST.get('igm', 0))
            
            # Predict District based on the values
            # If any two tests are positive, predict True
            is_positive = (ns1 + igg + igm) >= 2
            
            result = {
                'Gender': gender,
                'Age': age,
                'NS1': ns1,
                'IgG': igg,
                'IgM': igm,
                'Area': '-',
                'District': is_positive
            }
            
            # Save to database
            AnalysisResult.objects.create(
                ns1=ns1,
                igm=igm,
                igg=igg
            )

            return JsonResponse({
                'success': True,
                'results': result
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })
