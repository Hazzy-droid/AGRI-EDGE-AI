import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models import (
    User, LearningModule, LearningLesson, LearningQuiz, QuizQuestion, 
    QuestionChoice, UserLearningProgress, QuizAttempt, QuizAnswer,
    Achievement, UserAchievement
)
from utils.gamification import (
    award_points, complete_lesson, complete_quiz, get_user_learning_stats,
    check_achievements, get_achievements, calculate_points_to_next_level
)

learning_bp = Blueprint('learning', __name__, url_prefix='/learning')
logger = logging.getLogger(__name__)

@learning_bp.route('/')
def learning_dashboard():
    """Display the learning dashboard with available modules and progress"""
    
    # Get all active learning modules
    modules = LearningModule.query.filter_by(active=True).order_by(LearningModule.difficulty_level).all()
    
    # Handle both logged in and not logged in users
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # User is logged in, get actual data
        user_id = current_user.id
        
        # Get user's progress for each module
        user_progress = UserLearningProgress.query.filter_by(user_id=user_id).all()
        progress_by_module = {p.module_id: p for p in user_progress}
        
        # Get user's learning stats
        stats = get_user_learning_stats(user_id)
        
        # Get next level info
        next_level_info = calculate_points_to_next_level(user_id)
        
        # Check for new achievements
        achievement_check = check_achievements(user_id)
        new_achievements = achievement_check.get('newly_earned', [])
    else:
        # User is not logged in, provide demo data
        user_progress = []
        progress_by_module = {}
        stats = {
            'total_points': 0,
            'modules_completed': 0,
            'lessons_completed': 0,
            'quizzes_completed': 0,
            'achievement_count': 0,
            'current_level': 1
        }
        next_level_info = {
            'current_level': 1,
            'next_level': 2,
            'points_needed': 100,
            'progress_percentage': 0
        }
        new_achievements = []
    
    # Prepare modules with progress information
    modules_with_progress = []
    for module in modules:
        progress = progress_by_module.get(module.id)
        
        # Calculate completion percentage
        completion_percentage = 0
        if progress:
            # Count lessons and quizzes
            total_items = len(module.lessons) + len(module.quizzes)
            completed_items = 0
            
            if progress.lessons_completed:
                completed_items += len(progress.lessons_completed.split(','))
            
            if progress.quizzes_completed:
                completed_items += len(progress.quizzes_completed.split(','))
            
            if total_items > 0:
                completion_percentage = int((completed_items / total_items) * 100)
        
        # Format for template
        module_data = {
            'id': module.id,
            'title': module.title,
            'description': module.description,
            'category': module.category,
            'difficulty_level': module.difficulty_level,
            'points_available': module.points_available,
            'estimated_duration': module.estimated_duration,
            'image_url': module.image_url,
            'started': progress is not None,
            'completed': progress.completion_date is not None if progress else False,
            'completion_percentage': completion_percentage,
            'last_activity': progress.last_activity_date if progress else None
        }
        
        modules_with_progress.append(module_data)
    
    return render_template(
        'learning/dashboard.html', 
        modules=modules_with_progress,
        stats=stats,
        next_level=next_level_info,
        new_achievements=new_achievements
    )

@learning_bp.route('/module/<int:module_id>')
def view_module(module_id):
    """Display a learning module with its lessons and quizzes"""
    
    module = LearningModule.query.get_or_404(module_id)
    
    # Get ordered lessons and quizzes
    lessons = LearningLesson.query.filter_by(module_id=module_id).order_by(LearningLesson.order_index).all()
    quizzes = LearningQuiz.query.filter_by(module_id=module_id).order_by(LearningQuiz.order_index).all()
    
    # Handle both logged in and not logged in users
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Get user's progress for this module
        progress = UserLearningProgress.query.filter_by(
            user_id=current_user.id,
            module_id=module_id
        ).first()
        
        # Track completed items
        lessons_completed = []
        quizzes_completed = []
        
        if progress:
            if progress.lessons_completed:
                lessons_completed = [int(id) for id in progress.lessons_completed.split(',')]
            
            if progress.quizzes_completed:
                quizzes_completed = [int(id) for id in progress.quizzes_completed.split(',')]
        
        # Check prerequisites if any
        prerequisites_met = True
        prerequisite_modules = []
        
        if module.prerequisites:
            prereq_ids = [int(id) for id in module.prerequisites.split(',')]
            
            # Get prerequisite modules
            prerequisite_modules = LearningModule.query.filter(LearningModule.id.in_(prereq_ids)).all()
            
            # Check if user has completed all prerequisites
            for prereq_id in prereq_ids:
                prereq_progress = UserLearningProgress.query.filter_by(
                    user_id=current_user.id,
                    module_id=prereq_id
                ).first()
                
                if not prereq_progress or not prereq_progress.completion_date:
                    prerequisites_met = False
                    break
        
        # Calculate progress percentage
        total_items = len(lessons) + len(quizzes)
        completed_items = len(lessons_completed) + len(quizzes_completed)
        
        completion_percentage = int((completed_items / total_items) * 100) if total_items > 0 else 0
    else:
        # User is not logged in, provide demo data
        progress = None
        lessons_completed = []
        quizzes_completed = []
        prerequisites_met = True
        prerequisite_modules = []
        completion_percentage = 0
    
    return render_template(
        'learning/module.html',
        module=module,
        lessons=lessons,
        quizzes=quizzes,
        progress=progress,
        lessons_completed=lessons_completed,
        quizzes_completed=quizzes_completed,
        prerequisites_met=prerequisites_met,
        prerequisite_modules=prerequisite_modules,
        completion_percentage=completion_percentage
    )

@learning_bp.route('/lesson/<int:lesson_id>')
def view_lesson(lesson_id):
    """Display a learning lesson"""
    
    lesson = LearningLesson.query.get_or_404(lesson_id)
    module = LearningModule.query.get(lesson.module_id)
    
    # Handle both logged in and not logged in users
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Check prerequisites if any
        prerequisites_met = True
        if module.prerequisites:
            prereq_ids = [int(id) for id in module.prerequisites.split(',')]
            
            # Check if user has completed all prerequisites
            for prereq_id in prereq_ids:
                prereq_progress = UserLearningProgress.query.filter_by(
                    user_id=current_user.id,
                    module_id=prereq_id
                ).first()
                
                if not prereq_progress or not prereq_progress.completion_date:
                    prerequisites_met = False
                    flash("You need to complete the prerequisite modules first.", "warning")
                    return redirect(url_for('learning.view_module', module_id=module.id))
        
        # Get user's progress for this module
        progress = UserLearningProgress.query.filter_by(
            user_id=current_user.id,
            module_id=module.id
        ).first()
        
        # Check if lesson is already completed
        is_completed = False
        if progress and progress.lessons_completed:
            lesson_ids = [int(id) for id in progress.lessons_completed.split(',')]
            is_completed = lesson_id in lesson_ids
    else:
        # User is not logged in, provide demo data
        prerequisites_met = True
        progress = None
        is_completed = False
    
    # Get next and previous lesson/quiz
    all_lessons = LearningLesson.query.filter_by(module_id=module.id).order_by(LearningLesson.order_index).all()
    all_quizzes = LearningQuiz.query.filter_by(module_id=module.id).order_by(LearningQuiz.order_index).all()
    
    # Create ordered list of all content
    module_content = []
    for l in all_lessons:
        module_content.append({
            'id': l.id,
            'type': 'lesson',
            'title': l.title,
            'order_index': l.order_index
        })
    
    for q in all_quizzes:
        module_content.append({
            'id': q.id,
            'type': 'quiz',
            'title': q.title,
            'order_index': q.order_index
        })
    
    # Sort by order index
    module_content.sort(key=lambda x: x['order_index'])
    
    # Find current, next and previous items
    current_index = next((i for i, item in enumerate(module_content) 
                           if item['type'] == 'lesson' and item['id'] == lesson_id), None)
    
    next_item = None
    prev_item = None
    
    if current_index is not None:
        if current_index < len(module_content) - 1:
            next_item = module_content[current_index + 1]
        
        if current_index > 0:
            prev_item = module_content[current_index - 1]
    
    return render_template(
        'learning/lesson.html',
        lesson=lesson,
        module=module,
        is_completed=is_completed,
        next_item=next_item,
        prev_item=prev_item
    )

@learning_bp.route('/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson_route(lesson_id):
    """Mark a lesson as completed"""
    
    result = complete_lesson(current_user.id, lesson_id)
    
    if not result.get('success'):
        flash("Could not mark lesson as completed: " + result.get('error', 'Unknown error'), "danger")
        return redirect(url_for('learning.view_lesson', lesson_id=lesson_id))
    
    # Show appropriate messages
    if result.get('already_completed'):
        flash("You have already completed this lesson.", "info")
    else:
        flash(f"Lesson completed! You earned {result.get('points_awarded', 0)} points.", "success")
        
        if result.get('module_complete'):
            flash("Congratulations! You have completed this module.", "success")
        
        if result.get('level_up'):
            flash(f"Level up! You are now level {result.get('new_level')}.", "success")
    
    # Get the lesson to redirect to module
    lesson = LearningLesson.query.get(lesson_id)
    
    # Redirect based on next item
    if request.form.get('next_item_type') and request.form.get('next_item_id'):
        next_type = request.form.get('next_item_type')
        next_id = int(request.form.get('next_item_id'))
        
        if next_type == 'lesson':
            return redirect(url_for('learning.view_lesson', lesson_id=next_id))
        elif next_type == 'quiz':
            return redirect(url_for('learning.view_quiz', quiz_id=next_id))
    
    # Default redirect to module
    return redirect(url_for('learning.view_module', module_id=lesson.module_id))

@learning_bp.route('/quiz/<int:quiz_id>')
def view_quiz(quiz_id):
    """Display a learning quiz"""
    
    quiz = LearningQuiz.query.get_or_404(quiz_id)
    module = LearningModule.query.get(quiz.module_id)
    
    # Handle both logged in and not logged in users
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Check prerequisites if any
        prerequisites_met = True
        if module.prerequisites:
            prereq_ids = [int(id) for id in module.prerequisites.split(',')]
            
            # Check if user has completed all prerequisites
            for prereq_id in prereq_ids:
                prereq_progress = UserLearningProgress.query.filter_by(
                    user_id=current_user.id,
                    module_id=prereq_id
                ).first()
                
                if not prereq_progress or not prereq_progress.completion_date:
                    prerequisites_met = False
                    flash("You need to complete the prerequisite modules first.", "warning")
                    return redirect(url_for('learning.view_module', module_id=module.id))
        
        # Get user's progress for this module
        progress = UserLearningProgress.query.filter_by(
            user_id=current_user.id,
            module_id=module.id
        ).first()
        
        # Check if quiz is already completed
        is_completed = False
        if progress and progress.quizzes_completed:
            quiz_ids = [int(id) for id in progress.quizzes_completed.split(',')]
            is_completed = quiz_id in quiz_ids
        
        # Get quiz attempts
        attempts = QuizAttempt.query.filter_by(
            user_id=current_user.id,
            quiz_id=quiz_id
        ).order_by(QuizAttempt.attempt_number.desc()).all()
    else:
        # User is not logged in, provide demo data
        prerequisites_met = True
        is_completed = False
        progress = None
        attempts = []
    
    # Get questions and choices
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).order_by(QuizQuestion.order_index).all()
    
    questions_with_choices = []
    for question in questions:
        choices = QuestionChoice.query.filter_by(question_id=question.id).all()
        
        questions_with_choices.append({
            'question': question,
            'choices': choices
        })
    
    # Get next and previous lesson/quiz
    all_lessons = LearningLesson.query.filter_by(module_id=module.id).order_by(LearningLesson.order_index).all()
    all_quizzes = LearningQuiz.query.filter_by(module_id=module.id).order_by(LearningQuiz.order_index).all()
    
    # Create ordered list of all content
    module_content = []
    for l in all_lessons:
        module_content.append({
            'id': l.id,
            'type': 'lesson',
            'title': l.title,
            'order_index': l.order_index
        })
    
    for q in all_quizzes:
        module_content.append({
            'id': q.id,
            'type': 'quiz',
            'title': q.title,
            'order_index': q.order_index
        })
    
    # Sort by order index
    module_content.sort(key=lambda x: x['order_index'])
    
    # Find current, next and previous items
    current_index = next((i for i, item in enumerate(module_content) 
                           if item['type'] == 'quiz' and item['id'] == quiz_id), None)
    
    next_item = None
    prev_item = None
    
    if current_index is not None:
        if current_index < len(module_content) - 1:
            next_item = module_content[current_index + 1]
        
        if current_index > 0:
            prev_item = module_content[current_index - 1]
    
    return render_template(
        'learning/quiz.html',
        quiz=quiz,
        module=module,
        questions=questions_with_choices,
        is_completed=is_completed,
        attempts=attempts,
        next_item=next_item,
        prev_item=prev_item
    )

@learning_bp.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit a quiz attempt"""
    
    quiz = LearningQuiz.query.get_or_404(quiz_id)
    
    # Get questions
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
    
    # Process answers
    correct_count = 0
    total_possible = 0
    
    answers = []
    for question in questions:
        # Get the answer for this question
        answer_key = f'question_{question.id}'
        selected_choice_id = request.form.get(answer_key)
        
        # For multiple choice questions
        is_correct = False
        if selected_choice_id and selected_choice_id.isdigit():
            choice_id = int(selected_choice_id)
            
            # Check if the answer is correct
            choice = QuestionChoice.query.get(choice_id)
            if choice and choice.is_correct:
                is_correct = True
                correct_count += question.points
            
            total_possible += question.points
            
            answers.append({
                'question_id': question.id,
                'selected_choice_id': choice_id,
                'is_correct': is_correct
            })
    
    # Calculate score as percentage
    score = int((correct_count / total_possible) * 100) if total_possible > 0 else 0
    
    # Check if passed
    passed = score >= quiz.passing_score
    
    # Record the attempt
    result = complete_quiz(current_user.id, quiz_id, score, passed, answers)
    
    if not result.get('success'):
        flash("Could not save quiz results: " + result.get('error', 'Unknown error'), "danger")
        return redirect(url_for('learning.view_quiz', quiz_id=quiz_id))
    
    # Show appropriate messages
    if passed:
        flash(f"Congratulations! You passed the quiz with a score of {score}%.", "success")
        
        if not result.get('already_completed'):
            flash(f"You earned {result.get('points_awarded', 0)} points.", "success")
        
        if result.get('module_complete'):
            flash("Congratulations! You have completed this module.", "success")
        
        if result.get('level_up'):
            flash(f"Level up! You are now level {result.get('new_level')}.", "success")
    else:
        flash(f"You scored {score}%. You need {quiz.passing_score}% to pass this quiz.", "warning")
    
    # Redirect based on next item if passed, otherwise stay on quiz
    if passed and request.form.get('next_item_type') and request.form.get('next_item_id'):
        next_type = request.form.get('next_item_type')
        next_id = int(request.form.get('next_item_id'))
        
        if next_type == 'lesson':
            return redirect(url_for('learning.view_lesson', lesson_id=next_id))
        elif next_type == 'quiz':
            return redirect(url_for('learning.view_quiz', quiz_id=next_id))
    
    if passed:
        # If passed and no next item, go back to module
        return redirect(url_for('learning.view_module', module_id=quiz.module_id))
    else:
        # If failed, stay on quiz
        return redirect(url_for('learning.view_quiz', quiz_id=quiz_id))

@learning_bp.route('/achievements')
@login_required
def view_achievements():
    """Display user achievements"""
    
    # Get all user achievements
    achievements_data = get_achievements(current_user.id)
    
    if not achievements_data.get('success'):
        flash("Could not retrieve achievements: " + achievements_data.get('error', 'Unknown error'), "danger")
        return redirect(url_for('learning.learning_dashboard'))
    
    # Get next level info
    next_level_info = calculate_points_to_next_level(current_user.id)
    
    return render_template(
        'learning/achievements.html',
        earned=achievements_data.get('earned', []),
        locked=achievements_data.get('locked', []),
        stats={
            'total_earned': achievements_data.get('total_earned', 0),
            'total_available': achievements_data.get('total_available', 0),
            'completion_percentage': int((achievements_data.get('total_earned', 0) / achievements_data.get('total_available', 1)) * 100)
        },
        next_level=next_level_info
    )

@learning_bp.route('/leaderboard')
@login_required
def leaderboard():
    """Display learning leaderboard"""
    
    # Get top users by learning points
    top_learners = User.query.order_by(User.learning_points.desc()).limit(10).all()
    
    # Get the current user's rank
    user_rank_query = db.session.query(
        db.func.count(User.id)
    ).filter(
        User.learning_points > current_user.learning_points
    ).scalar()
    
    user_rank = user_rank_query + 1 if user_rank_query is not None else 1
    
    return render_template(
        'learning/leaderboard.html',
        top_learners=top_learners,
        user_rank=user_rank
    )