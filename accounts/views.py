from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from datetime import datetime
from .models import UserProfile, UserEducationProfile
from .utils import get_learning_style_recommendations
from .content_recommendations import ContentRecommendationEngine
from companion.models import KnowledgeArea, UserLearningProgress
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
                    return redirect('profile-settings')
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

    # Redirect if user is already authenticated
    if request.user.is_authenticated:
        messages.info(request, 'You are already signed in.')
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'signin.html', {'page_name': page_name})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                # Set session expiry based on remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    request.session.set_expiry(1209600)  # 2 weeks

                # Get redirect URL from next parameter or default
                next_url = request.GET.get('next')
                if next_url:
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect(next_url)

                # Check if profile is completed
                try:
                    profile = user.userprofile
                    if not profile.onboarding_completed:
                        messages.info(request, 'Please complete your profile setup.')
                        return redirect('profile-settings')
                    else:
                        messages.success(request, f'Welcome back, {user.first_name}!')
                        # Redirect based on user type
                        if user.is_staff:
                            return redirect('admin:index')
                        else:
                            return redirect('my-bot')
                except UserProfile.DoesNotExist:
                    # Create basic profile if it doesn't exist
                    UserProfile.objects.create(user=user)
                    messages.info(request, 'Please complete your profile setup.')
                    return redirect('profile-settings')
            else:
                messages.error(request, 'Your account has been disabled. Please contact support.')
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

    # Get enhanced recommendations with companion app integration
    recommended_subjects = recommendation_engine.get_recommended_subjects(limit=8)
    daily_recommendations = recommendation_engine.get_daily_recommendations(limit=12)

    # Get personalized learning paths for top subjects
    learning_paths = []
    for subject in recommended_subjects[:4]:
        path = recommendation_engine.get_personalized_learning_path(subject)
        learning_paths.append(path)

    # Get time-based recommendations
    time_based_content = {
        'quick_15min': recommendation_engine.get_content_recommendations_by_time(15),
        'medium_30min': recommendation_engine.get_content_recommendations_by_time(30),
        'long_60min': recommendation_engine.get_content_recommendations_by_time(60)
    }

    # Get weakness improvement plan
    improvement_plan = recommendation_engine.get_weakness_improvement_plan()

    # Get streak motivation content
    streak_content = recommendation_engine.get_streak_motivation_content()

    # Prepare content by categories with enhanced grouping
    content_by_type = {}
    content_by_difficulty = {'beginner': [], 'intermediate': [], 'advanced': []}
    content_by_subject = {}

    for rec in daily_recommendations:
        content = rec['content']
        content_type = content.content_type
        difficulty = content.difficulty_level
        subject_name = rec['subject'].name

        # Group by type
        if content_type not in content_by_type:
            content_by_type[content_type] = []
        content_by_type[content_type].append(rec)

        # Group by difficulty
        content_by_difficulty[difficulty].append(rec)

        # Group by subject
        if subject_name not in content_by_subject:
            content_by_subject[subject_name] = []
        content_by_subject[subject_name].append(rec)

    # Get user's learning preferences summary with enhanced data
    learning_summary = {
        'education_level': user_profile.get_education_level_display(),
        'grade_level': user_profile.grade_level,
        'learning_style': user_profile.get_learning_style_display(),
        'difficulty_preference': user_profile.get_difficulty_preference_display(),
        'study_time_preference': user_profile.get_study_time_preference_display(),
        'preferred_content_types': education_profile.preferred_content_types,
        'motivation_type': education_profile.get_motivation_type_display(),
        'learning_pace': education_profile.get_learning_pace_display(),
        'average_study_session': education_profile.average_study_session,
        'overall_performance': round(education_profile.overall_performance, 1),
        'favorite_subjects_count': education_profile.favorite_subjects.count(),
        'strong_subjects_count': education_profile.strong_subjects.count(),
        'weak_subjects_count': education_profile.weak_subjects.count()
    }

    # Get user's recent learning activity for dashboard insights
    from django.utils import timezone
    from datetime import timedelta

    recent_activity = UserLearningProgress.objects.filter(
        user=request.user,
        updated_at__gte=timezone.now() - timedelta(days=7)
    ).count()

    learning_insights = {
        'recent_activity_count': recent_activity,
        'active_subjects': UserLearningProgress.objects.filter(
            user=request.user,
            status='in_progress'
        ).values_list('knowledge_area__name', flat=True).distinct(),
        'completed_this_week': UserLearningProgress.objects.filter(
            user=request.user,
            status__in=['completed', 'mastered'],
            updated_at__gte=timezone.now() - timedelta(days=7)
        ).count()
    }

    if request.method == 'POST':
        # Handle various user actions
        action = request.POST.get('action')

        if action == 'select_subjects':
            # Handle subject selection
            selected_subjects = request.POST.getlist('selected_subjects')
            if selected_subjects:
                for subject_id in selected_subjects:
                    try:
                        subject = KnowledgeArea.objects.get(id=subject_id)
                        education_profile.favorite_subjects.add(subject)
                    except KnowledgeArea.DoesNotExist:
                        continue
                education_profile.save()
                messages.success(request, 'Your subject preferences have been updated!')

        elif action == 'start_learning':
            # User wants to start learning with selected content
            selected_content = request.POST.getlist('selected_content')
            if selected_content:
                messages.success(request, 'Let\'s start your personalized learning journey!')
                return redirect('chat:index')

        elif action == 'update_preferences':
            # Update learning preferences based on user feedback
            new_content_types = request.POST.getlist('preferred_content_types')
            new_difficulty = request.POST.get('difficulty_preference')

            if new_content_types:
                education_profile.preferred_content_types = new_content_types
            if new_difficulty:
                user_profile.difficulty_preference = new_difficulty

            education_profile.save()
            user_profile.save()
            messages.success(request, 'Your learning preferences have been updated!')

        # Redirect to prevent form resubmission
        return redirect('content-recommendations')

    context = {
        'page_name': page_name,
        'user_profile': user_profile,
        'education_profile': education_profile,
        'recommended_subjects': recommended_subjects,
        'daily_recommendations': daily_recommendations,
        'learning_paths': learning_paths,
        'content_by_type': content_by_type,
        'content_by_difficulty': content_by_difficulty,
        'content_by_subject': content_by_subject,
        'time_based_content': time_based_content,
        'improvement_plan': improvement_plan,
        'streak_content': streak_content,
        'learning_summary': learning_summary,
        'learning_insights': learning_insights,
        # Additional context for template
        'content_types': ['lesson', 'exercise', 'quiz', 'project', 'resource', 'video', 'reading'],
        'difficulty_levels': ['beginner', 'intermediate', 'advanced'],
    }

    return render(request, 'content-recommendations.html', context)

def signout(request):
    """Logout view with proper cleanup"""
    if request.user.is_authenticated:
        user_name = request.user.first_name or request.user.username
        logout(request)
        messages.success(request, f'Goodbye {user_name}! You have been successfully signed out.')
    else:
        messages.info(request, 'You are not currently signed in.')

    return redirect('signin')

@login_required
def dashboard(request):
    """Main dashboard after login"""
    page_name = "Dashboard"

    try:
        user_profile = request.user.userprofile

        # If profile is not completed, redirect to profile settings
        if not user_profile.onboarding_completed:
            messages.info(request, 'Please complete your profile setup to access the dashboard.')
            return redirect('profile-settings')

    except UserProfile.DoesNotExist:
        # Create basic profile and redirect to settings
        UserProfile.objects.create(user=request.user)
        messages.info(request, 'Please complete your profile setup.')
        return redirect('profile-settings')

    # Redirect based on user type and preferences
    if request.user.is_staff:
        return redirect('admin:index')

    # For students, redirect to their preferred starting point
    try:
        education_profile = user_profile.education_profile

        # Check if user has learning progress
        from companion.models import UserLearningProgress
        has_progress = UserLearningProgress.objects.filter(user=request.user).exists()

        if has_progress:
            # User has been using the platform, go to their companion
            return redirect('companion:dashboard')
        elif education_profile.favorite_subjects.exists():
            # User has selected subjects, show recommendations
            return redirect('content-recommendations')
        else:
            # New user, show chat interface
            return redirect('chat:index')

    except UserEducationProfile.DoesNotExist:
        # No education profile, complete profile first
        return redirect('profile-settings')

@login_required
def password_change(request):
    """Change password view"""
    page_name = "Change Password"

    if request.method == 'POST':
        current_password = request.POST.get('current_password', '').strip()
        new_password1 = request.POST.get('new_password1', '').strip()
        new_password2 = request.POST.get('new_password2', '').strip()

        # Validate current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return render(request, 'password-change.html', {'page_name': page_name})

        # Validate new passwords
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return render(request, 'password-change.html', {'page_name': page_name})

        if len(new_password1) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
            return render(request, 'password-change.html', {'page_name': page_name})

        # Change password
        request.user.set_password(new_password1)
        request.user.save()

        # Update session to prevent logout
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password has been changed successfully.')
        return redirect('dashboard')

    context = {
        'page_name': page_name
    }
    return render(request, 'password-change.html', context)

def password_reset_request(request):
    """Password reset request view"""
    page_name = "Reset Password"

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'password-reset.html', {'page_name': page_name})

        try:
            user = User.objects.get(email=email)
            # Here you would typically send a password reset email
            # For now, we'll just show a success message
            messages.success(request,
                'If an account with this email exists, you will receive password reset instructions.')
            return redirect('signin')
        except User.DoesNotExist:
            # Don't reveal if email exists or not
            messages.success(request,
                'If an account with this email exists, you will receive password reset instructions.')
            return redirect('signin')

    context = {
        'page_name': page_name
    }
    return render(request, 'password-reset.html', context)