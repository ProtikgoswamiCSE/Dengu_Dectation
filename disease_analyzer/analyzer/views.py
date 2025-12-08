from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
            ns1 = bool(int(request.POST.get('ns1', 0)))
            igg = bool(int(request.POST.get('igg', 0)))
            igm = bool(int(request.POST.get('igm', 0)))
            
            # Predict District based on the values
            # If any two tests are positive, predict True
            is_positive = (int(ns1) + int(igg) + int(igm)) >= 2
            
            result = {
                'Gender': gender,
                'Age': age,
                'NS1': int(ns1),
                'IgG': int(igg),
                'IgM': int(igm),
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

def signs_warnings(request):
    # Get all analysis results from database
    results = AnalysisResult.objects.all().order_by('-created_at')
    
    # Prepare data for template
    data = {
        'results': results,
        'total_count': results.count(),
        'positive_count': results.filter(ns1=True).count() + results.filter(igm=True).count() + results.filter(igg=True).count()
    }
    
    return render(request, 'analyzer/signs_warnings.html', data)

def disease_analyst(request):
    # Get all analysis results from database
    results = AnalysisResult.objects.all().order_by('-created_at')
    
    # Count positive cases (any test positive)
    from django.db.models import Q
    positive_cases = results.filter(Q(ns1=True) | Q(igm=True) | Q(igg=True))
    total_count = results.count()
    positive_count = positive_cases.count()
    negative_count = total_count - positive_count
    
    # Prepare data for template
    data = {
        'results': results,
        'total_count': total_count,
        'positive_cases': positive_cases,
        'positive_count': positive_count,
        'negative_count': negative_count
    }
    
    return render(request, 'analyzer/disease_analyst.html', data)