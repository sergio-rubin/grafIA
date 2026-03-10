from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # Pages
    path('', views.landing, name='landing'),
    path('learn/', views.learn_game, name='learn'),
    path('guess/', views.guess_game, name='guess'),
    path('leaderboard/learn/', views.leaderboard_learn, name='leaderboard_learn'),
    path('leaderboard/guess/', views.leaderboard_guess, name='leaderboard_guess'),
    
    # API endpoints
    path('api/fit-curve/', views.api_fit_curve, name='api_fit_curve'),
    path('api/save-learn-score/', views.api_save_learn_score, name='api_save_learn_score'),
    path('api/generate-function/', views.api_generate_function, name='api_generate_function'),
    path('api/compare-function/', views.api_compare_function, name='api_compare_function'),
    path('api/save-guess-score/', views.api_save_guess_score, name='api_save_guess_score'),
    path('api/leaderboard/learn/', views.api_leaderboard_learn, name='api_leaderboard_learn'),
    path('api/leaderboard/guess/', views.api_leaderboard_guess, name='api_leaderboard_guess'),
]
