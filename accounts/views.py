from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from datetime import datetime
from .models import UserProfile, UserEducationProfile
from .utils import get_learning_style_recommendations
from .content_recommendations import ContentRecommendationEngine
from companion.models import KnowledgeArea
import json

def signup(request):
    page_name = "Sign Up"

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Validate required fields
                username = request.POST.get('username', '').strip()
                email = request.POST.get('email', '').strip()
                password1 = request.POST.get('password1', '').strip()
                password2 = request.POST.get('password2', '').strip()
                first_name = request.POST.get('first_name', '').strip()
                last_name = request.POST.get('last_name', '').strip()
                agree_terms = request.POST.get('agree_terms')

                # Check required fields
                if not all([username, email, password1, password2, first_name, last_name]):
                    messages.error(request, 'Please fill in all required fields.')
                    return render(request, 'signup.html', {'page_name': page_name})

                # Check terms agreement
                if not agree_terms:
                    messages.error(request, 'You must agree to the Terms of Service and Privacy Policy.')
                    return render(request, 'signup.html', {'page_name': page_name})

                # Validate passwords
                if password1 != password2:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'signup.html', {'page_name': page_name})

                if len(password1) < 8:
                    messages.error(request, 'Password must be at least 8 characters long.')
                    return render(request, 'signup.html', {'page_name': page_name})

                # Check if username or email already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists.')
                    return render(request, 'signup.html', {'page_name': page_name})

                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists.')
                    return render(request, 'signup.html', {'page_name': page_name})

                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )

                # Parse date of birth safely
                date_of_birth = request.POST.get('date_of_birth', '').strip()
                parsed_date = None
                if date_of_birth:
                    try:
                        parsed_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                    except ValueError:
                        pass  # Keep as None if invalid

                # Create basic user profile without education/learning preferences
                user_profile = UserProfile.objects.create(
                    user=user,
                    phone_number=request.POST.get('phone_number', '').strip(),
                    date_of_birth=parsed_date,
                    profile_completed=False,  # Will be completed in profile settings
                    onboarding_completed=False
                )
                user_profile.save()

                # Auto-login the user
                user = authenticate(username=username, password=password1)
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome to Sua Pa AI, {user.first_name}! Your account has been created successfully.')

                    # Redirect to profile settings for final setup
                    return redirect('profile_settings')
                else:
                    messages.error(request, 'Account created but login failed. Please sign in manually.')
                    return redirect('signin')

        except Exception as e:
            import traceback
            error_msg = str(e)
            print(f"Signup Error: {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")

            # Provide user-friendly error messages
            if "UNIQUE constraint failed" in error_msg:
                messages.error(request, 'Username or email already exists. Please try different credentials.')
            elif "NOT NULL constraint failed" in error_msg:
                messages.error(request, 'Some required fields are missing. Please fill in all required information.')
            else:
                messages.error(request, f'An error occurred during signup. Please try again or contact support if the problem persists.')

            return render(request, 'signup.html', {'page_name': page_name})

    context = {
        'page_name': page_name
    }
    return render(request, 'signup.html', context)


def signin(request):
    page_name = "Sign In"

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if profile is completed
            try:
                profile = user.userprofile
                if not profile.onboarding_completed:
                    messages.info(request, 'Please complete your profile setup.')
                    return redirect('profile_settings')
                else:
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect('my-bot')  # Redirect to bot app
            except UserProfile.DoesNotExist:
                # Create basic profile if it doesn't exist
                UserProfile.objects.create(user=user)
                messages.info(request, 'Please complete your profile setup.')
                return redirect('profile_settings')
        else:
            messages.error(request, 'Invalid username or password.')

    context = {
        'page_name': page_name
    }
    return render(request, 'signin.html', context)

def profile_settings(request):
    page_name = "Profile Settings"

    # Ensure user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in to access profile settings.')
        return redirect('signin')

    try:
        user_profile = request.user.userprofile
        education_profile = user_profile.education_profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        education_profile = UserEducationProfile.objects.create(user_profile=user_profile)
    except UserEducationProfile.DoesNotExist:
        education_profile = UserEducationProfile.objects.create(user_profile=user_profile)

    # Get recommended subjects based on education level
    recommended_subjects = []
    if user_profile.education_level:
        recommended_subjects = education_profile.get_recommended_subjects()

    # Prepare context for template
    context = {
        'page_name': page_name,
        'user_profile': user_profile,
        'education_profile': education_profile,
        'recommended_subjects': recommended_subjects,
        'all_subjects': KnowledgeArea.objects.filter(is_active=True).order_by('education_level', 'name')
    }

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update education and learning preference fields
                education_level = request.POST.get('education_level', '').strip()

                # Validate education level is required if not already set
                if not user_profile.education_level and not education_level:
                    messages.error(request, 'Please select your education level.')
                    return render(request, 'profile-settings.html', context)

                # Parse grade level safely
                grade_level_str = request.POST.get('grade_level', '').strip()
                grade_level = None
                if grade_level_str:
                    try:
                        grade_level = int(grade_level_str)
                        if not (1 <= grade_level <= 12):
                            grade_level = None
                    except ValueError:
                        pass  # Keep as None if invalid

                # Update user profile with education and learning preferences
                user_profile.education_level = education_level or user_profile.education_level
                user_profile.grade_level = grade_level if grade_level_str else user_profile.grade_level
                user_profile.school_name = request.POST.get('school_name', '').strip() or user_profile.school_name
                user_profile.region = request.POST.get('region', '').strip() or user_profile.region
                user_profile.preferred_language = request.POST.get('preferred_language', 'english').strip()
                user_profile.learning_style = request.POST.get('learning_style', '').strip() or user_profile.learning_style
                user_profile.study_time_preference = request.POST.get('study_time_preference', 'flexible').strip()
                user_profile.difficulty_preference = request.POST.get('difficulty_preference', 'beginner').strip()
                user_profile.learning_goals = request.POST.get('learning_goals', '').strip() or user_profile.learning_goals
                user_profile.interests = request.POST.get('interests', '').strip() or user_profile.interests
                user_profile.profile_completed = True
                user_profile.onboarding_completed = True
                user_profile.save()

                # Update or create education profile
                motivation_type = request.POST.get('motivation_type', 'achievement')
                learning_style = user_profile.learning_style or 'mixed'

                # Get recommended content types based on learning style
                if learning_style:
                    preferred_content_types = get_learning_style_recommendations(learning_style)
                else:
                    preferred_content_types = ['text', 'video', 'quiz']

                education_profile.motivation_type = motivation_type
                education_profile.preferred_content_types = preferred_content_types
                education_profile.save()

                # Handle subject preferences if provided
                favorite_subjects = request.POST.getlist('favorite_subjects')
                strong_subjects = request.POST.getlist('strong_subjects')

                if favorite_subjects:
                    education_profile.favorite_subjects.set(favorite_subjects)
                if strong_subjects:
                    education_profile.strong_subjects.set(strong_subjects)

                messages.success(request, 'Profile setup completed successfully! Let\'s explore personalized content for you.')
                return redirect('content-recommendations')  # Redirect to content recommendations

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'profile-settings.html', context)

def content_recommendations(request):
    page_name = "Content Recommendations"

    # Ensure user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please sign in to view recommendations.')
        return redirect('signin')

    try:
        user_profile = request.user.userprofile
        education_profile = user_profile.education_profile
    except (UserProfile.DoesNotExist, UserEducationProfile.DoesNotExist):
        messages.error(request, 'Please complete your profile setup first.')
        return redirect('profile-settings')

    # Initialize recommendation engine
    recommendation_engine = ContentRecommendationEngine(request.user)

    # Get recommendations
    recommended_subjects = recommendation_engine.get_recommended_subjects(limit=6)
    daily_recommendations = recommendation_engine.get_daily_recommendations(limit=8)

    # Get learning paths for top 3 recommended subjects
    learning_paths = []
    for subject in recommended_subjects[:3]:
        path = recommendation_engine.get_learning_path(subject)
        learning_paths.append(path)

    # Prepare content by categories
    content_by_type = {}
    for rec in daily_recommendations:
        content_type = rec['content'].content_type
        if content_type not in content_by_type:
            content_by_type[content_type] = []
        content_by_type[content_type].append(rec)

    # Get user's learning preferences summary
    learning_summary = {
        'education_level': user_profile.get_education_level_display(),
        'grade_level': user_profile.grade_level,
        'learning_style': user_profile.get_learning_style_display(),
        'difficulty_preference': user_profile.get_difficulty_preference_display(),
        'study_time_preference': user_profile.get_study_time_preference_display(),
        'preferred_content_types': education_profile.preferred_content_types,
        'motivation_type': education_profile.get_motivation_type_display()
    }

    if request.method == 'POST':
        # Handle user choices (selecting subjects/content to start with)
        selected_subjects = request.POST.getlist('selected_subjects')

        if selected_subjects:
            # Save selected subjects as favorites if not already
            for subject_id in selected_subjects:
                try:
                    subject = KnowledgeArea.objects.get(id=subject_id)
                    education_profile.favorite_subjects.add(subject)
                except KnowledgeArea.DoesNotExist:
                    continue

            education_profile.save()
            messages.success(request, 'Your learning preferences have been saved! Let\'s start your learning journey.')
            return redirect('my-bot')

    context = {
        'page_name': page_name,
        'user_profile': user_profile,
        'education_profile': education_profile,
        'recommended_subjects': recommended_subjects,
        'daily_recommendations': daily_recommendations,
        'learning_paths': learning_paths,
        'content_by_type': content_by_type,
        'learning_summary': learning_summary,
    }

    return render(request, 'content-recommendations.html', context)