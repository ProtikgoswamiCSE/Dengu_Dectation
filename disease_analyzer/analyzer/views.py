from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AnalysisResult
import sys
import os
import csv
from django.db.models import Q
from datetime import datetime

# Import utils from parent directory (disease_analyzer/utils.py)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from utils import predict_dengue, predict_warning
except ImportError:
    # Fallback function if import fails
    def predict_dengue(gender, age, ns1, igg, igm, division, area, house_type):
        return (int(ns1) + int(igg) + int(igm)) >= 2
    def predict_warning(ns1, igg, igm):
        has_warning = bool(ns1) or bool(igm) or bool(igg)
        return has_warning, 1.0 if has_warning else 0.0

def home(request):
    return render(request, 'analyzer/home.html')

@csrf_exempt
def analyze_data(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('Name', '')
            gender = request.POST.get('gender', 'Male')
            age = int(request.POST.get('age', 0))
            ns1 = int(request.POST.get('ns1', 0))
            igg = int(request.POST.get('igg', 0))
            igm = int(request.POST.get('igm', 0))
            division = request.POST.get('division', 'Dhaka')
            area = request.POST.get('Area', '-')
            house_type = int(request.POST.get('house_type', '0'))
            
            # Use ML model to predict dengue
            is_positive = predict_dengue(
                gender=gender,
                age=str(age),
                ns1=ns1,
                igg=igg,
                igm=igm,
                division=division,
                area=area,
                house_type=house_type
            )
            
            result = {
                'Gender': gender,
                'Age': age,
                'NS1': int(ns1),
                'IgG': int(igg),
                'IgM': int(igm),
                'Area': area,
                'District': is_positive
            }
            
            # Save to database with all fields
            AnalysisResult.objects.create(
                name=name,
                gender=gender,
                age=age,
                division=division,
                area=area,
                house_type=house_type,
                ns1=bool(ns1),
                igm=bool(igm),
                igg=bool(igg)
            )

            return JsonResponse({
                'success': True,
                'results': result
            })

        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'error': str(e) + '\n' + traceback.format_exc()
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def signs_warnings(request):
    # Get all analysis results from database
    results = AnalysisResult.objects.all().order_by('-created_at')
    
    # Use Warnings_model.pkl to predict warnings for each result
    results_with_predictions = []
    warning_count = 0
    
    for result in results:
        # Get prediction from Warnings_model.pkl
        has_warning, confidence = predict_warning(
            ns1=result.ns1,
            igg=result.igg,
            igm=result.igm
        )
        
        # Add prediction results to the result object
        result.warning_prediction = has_warning
        result.warning_confidence = confidence
        
        results_with_predictions.append(result)
        
        if has_warning:
            warning_count += 1
    
    # Calculate additional statistics
    total_count = results.count()
    safe_count = total_count - warning_count
    warning_rate = (warning_count / total_count * 100) if total_count > 0 else 0
    
    # Prepare data for template
    data = {
        'results': results_with_predictions,
        'total_count': total_count,
        'positive_count': results.filter(ns1=True).count() + results.filter(igm=True).count() + results.filter(igg=True).count(),
        'warning_count': warning_count,
        'safe_count': safe_count,
        'warning_rate': round(warning_rate, 1)
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

def save_disease_data(request):
    """Export all disease analysis data to CSV"""
    # Get all analysis results from database
    results = AnalysisResult.objects.all().order_by('-created_at')
    
    # Create HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="disease_analysis_data_{}.csv"'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['ID', 'Name', 'Gender', 'Age', 'Division', 'Area', 'House Type', 'NS1 Test', 'IgM Test', 'IgG Test', 'Analysis Date', 'Risk Level'])
    
    # Write data rows
    for result in results:
        # Determine risk level (True if any test is positive, False otherwise)
        risk_level = 'True' if (result.ns1 or result.igm or result.igg) else 'False'
        
        writer.writerow([
            result.id,
            result.name or '-',
            result.gender or '-',
            result.age or 0,
            result.division or '-',
            result.area or '-',
            result.house_type or 0,
            'Positive' if result.ns1 else 'Negative',
            'Positive' if result.igm else 'Negative',
            'Positive' if result.igg else 'Negative',
            result.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            risk_level
        ])
    
    return response

@csrf_exempt
def delete_all_disease_data(request):
    """
    Delete all disease analysis data from database.
    This function ONLY deletes AnalysisResult records (Disease Analyst page data).
    It does NOT affect any other data or pages.
    """
    if request.method == 'POST':
        try:
            # Get count before deletion
            count = AnalysisResult.objects.count()
            
            # Delete all AnalysisResult records (only Disease Analyst page data)
            AnalysisResult.objects.all().delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully deleted {count} record(s)',
                'deleted_count': count
            })
        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'error': str(e) + '\n' + traceback.format_exc()
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })