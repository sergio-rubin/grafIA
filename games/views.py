from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import random
import math

from .models import LearnScore, GuessScore


def landing(request):
    """Landing page with game selection"""
    return render(request, 'games/landing.html')


def learn_game(request):
    """grafIA Learn game page"""
    return render(request, 'games/learn.html')


def guess_game(request):
    """grafIA Guess game page"""
    return render(request, 'games/guess.html')


def leaderboard_learn(request):
    """Leaderboard for grafIA Learn"""
    scores = LearnScore.objects.all()[:10]
    return render(request, 'games/leaderboard_learn.html', {'scores': scores})


def leaderboard_guess(request):
    """Leaderboard for grafIA Guess"""
    scores = GuessScore.objects.all()[:10]
    return render(request, 'games/leaderboard_guess.html', {'scores': scores})


# API Endpoints

@csrf_exempt
@require_http_methods(["POST"])
def api_fit_curve(request):
    """
    Fit polynomial regression to user-drawn points.
    Points are expected in real cartesian coordinates.
    Returns coefficients that work directly in GeoGebra/math software.
    """
    try:
        data = json.loads(request.body)
        points = data.get('points', [])
        
        if len(points) < 5:
            return JsonResponse({'success': False, 'message': 'Se necesitan al menos 5 puntos'}, status=400)
        
        # Extract x and y coordinates (already in real cartesian coords)
        x = np.array([p['x'] for p in points])
        y = np.array([p['y'] for p in points])
        
        x_min, x_max = x.min(), x.max()
        if x_max - x_min < 0.1:
            return JsonResponse({'success': False, 'message': 'Dibuja una curva más amplia horizontalmente'}, status=400)
        
        # Try different polynomial degrees and find best fit
        best_degree = 3
        best_mse = float('inf')
        best_coeffs = None
        
        for degree in range(1, 8):
            try:
                # Fit directly on real coordinates
                coeffs = np.polyfit(x, y, degree)
                y_pred = np.polyval(coeffs, x)
                mse = np.mean((y - y_pred) ** 2)
                
                # Penalize higher degrees to avoid overfitting
                adjusted_mse = mse * (1 + 0.15 * degree)
                
                if adjusted_mse < best_mse:
                    best_mse = mse
                    best_degree = degree
                    best_coeffs = coeffs
            except:
                continue
        
        # Calculate predictions with best model
        y_pred = np.polyval(best_coeffs, x)
        
        # Calculate RMSE for error display
        rmse = np.sqrt(np.mean((y - y_pred) ** 2))
        
        # Calculate R² (coefficient of determination) for more intuitive error
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        r_squared = max(0, min(1, r_squared))
        
        # Error as 1 - R² (percentage of variance not explained)
        error_rate = 1 - r_squared
        
        # Generate fitted curve points for visualization (more points for smoothness)
        x_fit = np.linspace(x_min, x_max, 200)
        y_fit = np.polyval(best_coeffs, x_fit)
        
        # Score: Higher error = higher score (user drew something hard for AI)
        score = round(1000 * error_rate)
        score = max(0, min(1000, score))
        
        # Prepare fitted points for frontend (in real coords)
        fitted_points = [
            {'x': float(x_fit[i]), 'y': float(y_fit[i])}
            for i in range(len(x_fit))
        ]
        
        # High precision coefficients for GeoGebra compatibility
        display_coeffs = [round(c, 6) for c in best_coeffs.tolist()]
        
        return JsonResponse({
            'success': True,
            'fitted_points': fitted_points,
            'degree': best_degree,
            'fitting_error': round(error_rate, 4),
            'r_squared': round(r_squared, 4),
            'rmse': round(rmse, 4),
            'score': score,
            'coefficients': display_coeffs
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_save_learn_score(request):
    """Save score for grafIA Learn"""
    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', '').strip()
        score = data.get('score', 0)
        fitting_error = data.get('fitting_error', 0)
        
        # Validate name
        if len(player_name) < 2 or len(player_name) > 20:
            return JsonResponse({'success': False, 'message': 'El nombre debe tener entre 2 y 20 caracteres'}, status=400)
        
        if not player_name.replace('_', '').isalnum():
            return JsonResponse({'success': False, 'message': 'El nombre solo puede contener letras, números y guiones bajos'}, status=400)
        
        # Save score
        LearnScore.objects.create(
            player_name=player_name,
            score=score,
            error=fitting_error
        )
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_generate_function(request):
    """Generate a random mathematical function for guessing game"""
    
    functions = [
        # Linear: ax + b
        {
            'type': 'linear',
            'generate': lambda: {
                'a': random.choice([-2, -1, 1, 2]),
                'b': random.randint(-3, 3)
            },
            'formula': lambda p: f"{p['a']}x {'+' if p['b'] >= 0 else '-'} {abs(p['b'])}",
            'eval': lambda x, p: p['a'] * x + p['b']
        },
        # Quadratic: ax^2 + bx + c
        {
            'type': 'quadratic',
            'generate': lambda: {
                'a': random.choice([-1, 1, 0.5, -0.5]),
                'b': random.choice([-2, -1, 0, 1, 2]),
                'c': random.randint(-2, 2)
            },
            'formula': lambda p: f"{p['a']}x² {'+' if p['b'] >= 0 else '-'} {abs(p['b'])}x {'+' if p['c'] >= 0 else '-'} {abs(p['c'])}",
            'eval': lambda x, p: p['a'] * x**2 + p['b'] * x + p['c']
        },
        # Sine: sin(ax)
        {
            'type': 'sine',
            'generate': lambda: {
                'a': random.choice([1, 2, 0.5])
            },
            'formula': lambda p: f"sin({p['a']}x)" if p['a'] != 1 else "sin(x)",
            'eval': lambda x, p: math.sin(p['a'] * x)
        },
        # Cosine: cos(ax)
        {
            'type': 'cosine',
            'generate': lambda: {
                'a': random.choice([1, 2, 0.5])
            },
            'formula': lambda p: f"cos({p['a']}x)" if p['a'] != 1 else "cos(x)",
            'eval': lambda x, p: math.cos(p['a'] * x)
        },
        # Absolute: a*|x| + b
        {
            'type': 'absolute',
            'generate': lambda: {
                'a': random.choice([1, 2, -1, -2]),
                'b': random.randint(-2, 2)
            },
            'formula': lambda p: f"{p['a']}|x| {'+' if p['b'] >= 0 else '-'} {abs(p['b'])}",
            'eval': lambda x, p: p['a'] * abs(x) + p['b']
        },
        # Cubic: ax^3
        {
            'type': 'cubic',
            'generate': lambda: {
                'a': random.choice([0.1, 0.2, -0.1, -0.2])
            },
            'formula': lambda p: f"{p['a']}x³",
            'eval': lambda x, p: p['a'] * x**3
        },
    ]
    
    # Select random function
    func_template = random.choice(functions)
    params = func_template['generate']()
    formula = func_template['formula'](params)
    
    # Generate points for graph
    x_values = np.linspace(-5, 5, 100)
    points = []
    
    for x in x_values:
        try:
            y = func_template['eval'](x, params)
            if not math.isnan(y) and not math.isinf(y) and abs(y) < 10:
                points.append({'x': float(x), 'y': float(y)})
        except:
            continue
    
    # Store function info in session or return as token
    function_id = random.randint(10000, 99999)
    
    # We'll evaluate user function later using the params
    return JsonResponse({
        'success': True,
        'function_id': function_id,
        'function_type': func_template['type'],
        'params': params,
        'points': points,
        'formula': formula
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_compare_function(request):
    """Compare user's function with the real function"""
    try:
        data = json.loads(request.body)
        user_function = data.get('user_function', '').strip()
        real_points = data.get('real_points', [])
        time_seconds = data.get('time_seconds', 0)
        
        if not user_function:
            return JsonResponse({'error': 'Ingresa una función'}, status=400)
        
        if not real_points:
            return JsonResponse({'error': 'No hay puntos de referencia'}, status=400)
        
        # Prepare safe evaluation environment
        safe_math = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'abs': abs,
            'log': math.log,
            'sqrt': math.sqrt,
            'exp': math.exp,
            'pi': math.pi,
            'e': math.e,
            'pow': pow,
        }
        
        # Clean user function
        user_func = user_function.lower()
        user_func = user_func.replace('^', '**')
        user_func = user_func.replace('sen', 'sin')
        user_func = user_func.replace('|x|', 'abs(x)')
        
        # Evaluate user function at same x values
        errors = []
        user_points = []
        
        for point in real_points:
            x = point['x']
            y_real = point['y']
            
            try:
                y_user = eval(user_func, {"__builtins__": {}, "x": x, **safe_math})
                
                if not math.isnan(y_user) and not math.isinf(y_user):
                    user_points.append({'x': x, 'y': float(y_user)})
                    errors.append(abs(y_real - y_user))
            except:
                continue
        
        if len(errors) < 10:
            return JsonResponse({
                'success': False,
                'error': 'No se pudo evaluar la función. Verifica la sintaxis.',
                'user_points': user_points
            }, status=400)
        
        # Calculate mean absolute error
        mean_error = np.mean(errors)
        
        # Calculate precision (1 = perfect, 0 = very bad)
        # Error threshold for "correct" is around 0.5
        precision = max(0, 1 - (mean_error / 2))
        precision = min(1, precision)
        
        # Calculate score
        score = round(1000 * precision) - round(time_seconds * 10)
        score = max(0, score)
        
        return JsonResponse({
            'success': True,
            'user_points': user_points,
            'mean_error': round(mean_error, 4),
            'precision': round(precision, 4),
            'score': score,
            'time_seconds': round(time_seconds, 2)
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Error al evaluar: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_save_guess_score(request):
    """Save score for grafIA Guess"""
    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', '').strip()
        score = data.get('score', 0)
        time_seconds = data.get('time_seconds', 0)
        precision = data.get('precision', 0)
        
        # Validate name
        if len(player_name) < 2 or len(player_name) > 20:
            return JsonResponse({'error': 'El nombre debe tener entre 2 y 20 caracteres'}, status=400)
        
        if not player_name.replace('_', '').isalnum():
            return JsonResponse({'error': 'El nombre solo puede contener letras, números y guiones bajos'}, status=400)
        
        # Save score
        GuessScore.objects.create(
            player_name=player_name,
            score=score,
            time_seconds=time_seconds,
            precision=precision
        )
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def api_leaderboard_learn(request):
    """Get leaderboard data for grafIA Learn"""
    scores = LearnScore.objects.all()[:10]
    data = [
        {
            'rank': i + 1,
            'player_name': s.player_name,
            'score': s.score,
            'error': round(s.error, 4),
            'date': s.created_at.strftime('%d/%m/%Y')
        }
        for i, s in enumerate(scores)
    ]
    return JsonResponse({'scores': data})


@require_http_methods(["GET"])
def api_leaderboard_guess(request):
    """Get leaderboard data for grafIA Guess"""
    scores = GuessScore.objects.all()[:10]
    data = [
        {
            'rank': i + 1,
            'player_name': s.player_name,
            'score': s.score,
            'time_seconds': round(s.time_seconds, 2),
            'precision': round(s.precision, 4),
            'date': s.created_at.strftime('%d/%m/%Y')
        }
        for i, s in enumerate(scores)
    ]
    return JsonResponse({'scores': data})
