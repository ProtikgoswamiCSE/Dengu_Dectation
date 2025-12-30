from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AnalysisResult, SignsWarning
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
    try:
        # Get all signs warning results from separate database
        results = SignsWarning.objects.all().order_by('-created_at')
        
        # Calculate statistics
        total_count = results.count()
        warning_count = results.filter(warning_prediction=True).count()
        safe_count = total_count - warning_count
        warning_rate = (warning_count / total_count * 100) if total_count > 0 else 0
        
        # Count positive cases
        positive_count = results.filter(ns1=True).count() + results.filter(igm=True).count() + results.filter(igg=True).count()
    except Exception as e:
        error_msg = str(e).lower()
        # Handle case where table doesn't exist yet (migration not run)
        if 'no such table' in error_msg or 'does not exist' in error_msg or 'relation' in error_msg:
            # Return empty results with migration message
            results = []
            total_count = 0
            warning_count = 0
            safe_count = 0
            warning_rate = 0
            positive_count = 0
            # Store error message to show in template
            import sys
            sys.stderr.write(f"Migration needed: {str(e)}\n")
        else:
            # Re-raise other errors
            raise
    
    # Prepare data for template
    data = {
        'results': results,
        'total_count': total_count,
        'positive_count': positive_count,
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

def save_signs_warnings_data(request):
    """Export all signs and warnings analysis data to CSV"""
    try:
        # Get all signs warning results from separate database
        results = SignsWarning.objects.all().order_by('-created_at')
    except Exception as e:
        # Handle case where table doesn't exist yet
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="error.txt"'
        response.write('Error: Database table does not exist. Please run migrations first.')
        return response
    
    # Create HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="signs_warnings_data_{}.csv"'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['ID', 'Name', 'Gender', 'Age', 'Division', 'Area', 'House Type', 'NS1 Test', 'IgM Test', 'IgG Test', 'Analysis Date', 'Model Prediction', 'Confidence', 'Status'])
    
    # Write data rows
    for result in results:
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
            'Warning' if result.warning_prediction else 'Safe',
            f'{result.warning_confidence:.2f}',
            'Warning' if result.warning_prediction else 'Safe'
        ])
    
    return response

@csrf_exempt
def delete_all_signs_warnings_data(request):
    """
    Delete all signs and warnings analysis data from database.
    This function ONLY deletes SignsWarning records (Signs and Warnings page data).
    It does NOT affect any other data or pages.
    """
    if request.method == 'POST':
        try:
            # Get count before deletion
            count = SignsWarning.objects.count()
            
            # Delete all SignsWarning records (only Signs and Warnings page data)
            SignsWarning.objects.all().delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully deleted {count} record(s)',
                'deleted_count': count
            })
        except Exception as e:
            import traceback
            error_msg = str(e)
            # Check if it's a table doesn't exist error
            if 'no such table' in error_msg.lower() or 'does not exist' in error_msg.lower():
                return JsonResponse({
                    'success': False,
                    'error': 'Database table does not exist. Please run migrations first: python manage.py migrate'
                })
            return JsonResponse({
                'success': False,
                'error': str(e) + '\n' + traceback.format_exc()
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

@csrf_exempt
def analyze_warning(request):
    """Analyze warning using Warnings_model.pkl and save to SignsWarning database"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name', '')
            gender = request.POST.get('gender', 'Male')
            age = int(request.POST.get('age', 0))
            division = request.POST.get('division', 'Dhaka')
            area = request.POST.get('area', '-')
            house_type = int(request.POST.get('house_type', 0))
            ns1 = int(request.POST.get('ns1', 0))
            igg = int(request.POST.get('igg', 0))
            igm = int(request.POST.get('igm', 0))
            
            # Use ML model to predict warning
            has_warning, confidence = predict_warning(
                ns1=bool(ns1),
                igg=bool(igg),
                igm=bool(igm)
            )
            
            # Save to SignsWarning database
            try:
                warning_result = SignsWarning.objects.create(
                    name=name,
                    gender=gender,
                    age=age,
                    division=division,
                    area=area,
                    house_type=house_type,
                    ns1=bool(ns1),
                    igg=bool(igg),
                    igm=bool(igm),
                    warning_prediction=has_warning,
                    warning_confidence=confidence
                )
                result_id = warning_result.id
            except Exception as db_error:
                error_msg = str(db_error)
                # Check if it's a table doesn't exist error
                if 'no such table' in error_msg.lower() or 'does not exist' in error_msg.lower():
                    return JsonResponse({
                        'success': False,
                        'error': 'Database table does not exist. Please run migrations first: python manage.py migrate'
                    })
                raise db_error
            
            result = {
                'id': result_id,
                'ns1': 'Positive' if ns1 else 'Negative',
                'igg': 'Positive' if igg else 'Negative',
                'igm': 'Positive' if igm else 'Negative',
                'warning': has_warning,
                'warning_text': 'Warning Detected' if has_warning else 'Safe',
                'confidence': round(confidence * 100, 2)
            }
            
            return JsonResponse({
                'success': True,
                'results': result
            })

        except Exception as e:
            import traceback
            error_details = str(e) + '\n' + traceback.format_exc()
            print(f"Error in analyze_warning: {error_details}")
            return JsonResponse({
                'success': False,
                'error': error_details
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

@csrf_exempt
def analyze_symptoms_warning(request):
    """Analyze symptoms from awareness card and save to SignsWarning database"""
    if request.method == 'POST':
        try:
            import json
            
            # Get symptoms data (array of 0/1 values)
            symptoms_data = request.POST.get('symptoms', '[]')
            if isinstance(symptoms_data, str):
                try:
                    symptoms = json.loads(symptoms_data)
                except:
                    symptoms = []
            else:
                symptoms = symptoms_data if symptoms_data else []
            
            # Ensure symptoms is a list and has exactly 12 items
            if not isinstance(symptoms, list):
                symptoms = []
            
            # Pad or truncate to exactly 12 symptoms
            while len(symptoms) < 12:
                symptoms.append(0)
            symptoms = symptoms[:12]
            
            # Get optional user info
            name = request.POST.get('name', '')
            gender = request.POST.get('gender', 'Male')
            age = int(request.POST.get('age', 0))
            division = request.POST.get('division', 'Dhaka')
            area = request.POST.get('area', '-')
            house_type = int(request.POST.get('house_type', 0))
            
            # Count positive symptoms
            positive_symptoms = sum(1 for s in symptoms if int(s) > 0)
            total_symptoms = len(symptoms) if symptoms else 12
            
            # Convert symptoms to test predictions based on symptom count
            # If many symptoms are positive, treat as potential warning
            # Map to NS1, IgG, IgM based on symptom severity
            if positive_symptoms >= 8:
                # Very high risk - treat as positive for all tests
                ns1 = 1
                igg = 1
                igm = 1
            elif positive_symptoms >= 5:
                # High risk - treat as positive for NS1 and IgM
                ns1 = 1
                igg = 0
                igm = 1
            elif positive_symptoms >= 3:
                # Medium risk - treat as positive for IgM only
                ns1 = 0
                igg = 0
                igm = 1
            else:
                # Low risk - all negative
                ns1 = 0
                igg = 0
                igm = 0
            
            # Use ML model to predict warning
            has_warning, confidence = predict_warning(
                ns1=bool(ns1),
                igg=bool(igg),
                igm=bool(igm)
            )
            
            # Adjust confidence based on symptom count
            symptom_confidence = min(positive_symptoms / total_symptoms, 1.0) if total_symptoms > 0 else 0.0
            # Combine model confidence with symptom-based confidence
            final_confidence = max(confidence, symptom_confidence)
            
            # Save to SignsWarning database
            try:
                # Convert all symptoms to integers, ensure we have exactly 12
                symptoms_clean = [int(s) if s else 0 for s in symptoms[:12]]
                while len(symptoms_clean) < 12:
                    symptoms_clean.append(0)
                
                warning_result = SignsWarning.objects.create(
                    name=name or f'Symptom Analysis - {positive_symptoms} symptoms',
                    gender=gender,
                    age=age,
                    division=division,
                    area=area,
                    house_type=house_type,
                    ns1=bool(ns1),
                    igg=bool(igg),
                    igm=bool(igm),
                    warning_prediction=has_warning,
                    warning_confidence=final_confidence,
                    symptom_mild_fever=symptoms_clean[0],
                    symptom_eyelid_pain=symptoms_clean[1],
                    symptom_headache=symptoms_clean[2],
                    symptom_body_aches=symptoms_clean[3],
                    symptom_nausea=symptoms_clean[4],
                    symptom_skin_rash=symptoms_clean[5],
                    symptom_fatigue=symptoms_clean[6],
                    symptom_stomach_pain=symptoms_clean[7],
                    symptom_dry_throat=symptoms_clean[8],
                    symptom_lightheadedness=symptoms_clean[9],
                    symptom_chest_pain=symptoms_clean[10],
                    symptom_bleeding=symptoms_clean[11]
                )
                result_id = warning_result.id
            except Exception as db_error:
                error_msg = str(db_error)
                # Check if it's a table doesn't exist error
                if 'no such table' in error_msg.lower() or 'does not exist' in error_msg.lower():
                    return JsonResponse({
                        'success': False,
                        'error': 'Database table does not exist. Please run migrations first: python manage.py migrate'
                    })
                raise db_error
            
            # Calculate risk level
            risk_percentage = round((positive_symptoms / total_symptoms * 100) if total_symptoms > 0 else 0)
            
            result = {
                'id': result_id,
                'positive_symptoms': positive_symptoms,
                'total_symptoms': total_symptoms,
                'risk_percentage': risk_percentage,
                'ns1': 'Positive' if ns1 else 'Negative',
                'igg': 'Positive' if igg else 'Negative',
                'igm': 'Positive' if igm else 'Negative',
                'warning': has_warning,
                'warning_text': 'Warning Detected' if has_warning else 'Safe',
                'confidence': round(final_confidence * 100, 2)
            }
            
            return JsonResponse({
                'success': True,
                'results': result
            })

        except Exception as e:
            import traceback
            error_details = str(e) + '\n' + traceback.format_exc()
            print(f"Error in analyze_symptoms_warning: {error_details}")
            return JsonResponse({
                'success': False,
                'error': error_details
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })