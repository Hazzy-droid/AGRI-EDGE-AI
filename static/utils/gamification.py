"""
Utilities for handling gamification features and mechanics
"""
import logging
from datetime import datetime
from app import db
from models import (
    User, Achievement, UserAchievement, UserPractice,
    UserQuest, UserChallenge, LearningModule, UserLearningProgress
)

logger = logging.getLogger(__name__)

# Level thresholds - points needed for each level
LEVEL_THRESHOLDS = [
    0,      # Level 1
    100,    # Level 2
    250,    # Level 3
    500,    # Level 4
    1000,   # Level 5
    1750,   # Level 6
    3000,   # Level 7
    5000,   # Level 8
    8000,   # Level 9
    12000   # Level 10
]

def award_points(user_id, points, category='learning', description=None):
    """
    Award points to a user and update their level if needed
    
    Args:
        user_id (int): User ID to award points to
        points (int): Number of points to award
        category (str): Category of points (learning, farming, community)
        description (str): Optional description of why points were awarded
    
    Returns:
        tuple: (new_total_points, level_up, new_level)
    """
    user = User.query.get(user_id)
    if not user:
        logger.error(f"Cannot award points - User ID {user_id} not found")
        return None, False, None
    
    # Update the appropriate points category
    if category == 'learning':
        user.learning_points += points
    elif category == 'farming':
        user.farming_points += points
    elif category == 'community':
        user.community_points += points
    
    # Update total points
    old_total = user.total_points
    user.total_points = user.learning_points + user.farming_points + user.community_points
    
    # Check if user has leveled up
    old_level = user.level
    new_level = calculate_level(user.total_points)
    level_up = new_level > old_level
    
    if level_up:
        user.level = new_level
        logger.info(f"User {user_id} leveled up from {old_level} to {new_level}")
    
    # Record points transaction in a real app, we'd store this in a points history table
    if description:
        logger.info(f"Awarded {points} {category} points to User {user_id}: {description}")
    
    db.session.commit()
    
    return user.total_points, level_up, new_level

def calculate_level(total_points):
    """
    Calculate the level based on total points
    
    Args:
        total_points (int): User's total points
        
    Returns:
        int: The user's level based on their points
    """
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if total_points >= threshold:
            level = i + 1
        else:
            break
    
    return level

def get_user_level_progress(user_id):
    """
    Get information about a user's level progress
    
    Args:
        user_id (int): User ID to check
        
    Returns:
        dict: Information about user's level and progress to next level
    """
    user = User.query.get(user_id)
    if not user:
        logger.error(f"Cannot get level progress - User ID {user_id} not found")
        return None
    
    current_level = user.level
    current_points = user.total_points
    
    # If at max level
    if current_level >= len(LEVEL_THRESHOLDS):
        return {
            'level': current_level,
            'points': current_points,
            'points_to_next_level': 0,
            'progress_percentage': 100
        }
    
    # Calculate progress to next level
    current_level_threshold = LEVEL_THRESHOLDS[current_level - 1]
    next_level_threshold = LEVEL_THRESHOLDS[current_level]
    
    points_needed_for_next_level = next_level_threshold - current_level_threshold
    points_earned_since_last_level = current_points - current_level_threshold
    points_to_next_level = next_level_threshold - current_points
    
    progress_percentage = min(
        100,
        int((points_earned_since_last_level / points_needed_for_next_level) * 100)
    )
    
    return {
        'level': current_level,
        'points': current_points,
        'points_to_next_level': points_to_next_level,
        'progress_percentage': progress_percentage,
        'current_level_threshold': current_level_threshold,
        'next_level_threshold': next_level_threshold
    }

def check_achievement_eligibility(user_id):
    """
    Check if a user is eligible for any achievements they haven't earned yet
    
    Args:
        user_id (int): User ID to check
        
    Returns:
        list: List of newly awarded achievement IDs
    """
    # Get achievements user has already earned
    earned_achievement_ids = [
        ua.achievement_id for ua in 
        UserAchievement.query.filter_by(user_id=user_id).all()
    ]
    
    # Get all achievements that user hasn't earned yet and aren't hidden
    available_achievements = Achievement.query.filter(
        ~Achievement.id.in_(earned_achievement_ids),
        Achievement.is_hidden == False
    ).all()
    
    newly_awarded = []
    
    for achievement in available_achievements:
        if is_eligible_for_achievement(user_id, achievement):
            award_achievement(user_id, achievement.id)
            newly_awarded.append(achievement.id)
    
    return newly_awarded

def is_eligible_for_achievement(user_id, achievement):
    """
    Check if a user is eligible for a specific achievement
    
    Args:
        user_id (int): User ID to check
        achievement (Achievement): Achievement object to check eligibility for
        
    Returns:
        bool: True if user is eligible, False otherwise
    """
    # Different logic based on achievement category
    category = achievement.category
    
    if category == 'learning':
        return check_learning_achievement_eligibility(user_id, achievement)
    elif category == 'farming' or category == 'sustainability':
        return check_farming_achievement_eligibility(user_id, achievement)
    elif category == 'community':
        return check_community_achievement_eligibility(user_id, achievement)
    else:
        return check_general_achievement_eligibility(user_id, achievement)

def check_learning_achievement_eligibility(user_id, achievement):
    """Check eligibility for learning-related achievements"""
    # Get user's learning progress
    user_progress = UserLearningProgress.query.filter_by(user_id=user_id).all()
    
    # Example achievement types:
    if 'complete_first_module' in achievement.criteria:
        return len([p for p in user_progress if p.completion_date is not None]) >= 1
    
    if 'complete_modules' in achievement.criteria:
        # Extract number from criteria like "complete_modules:5"
        try:
            num_required = int(achievement.criteria.split(':')[1])
            completed_modules = len([p for p in user_progress if p.completion_date is not None])
            return completed_modules >= num_required
        except (IndexError, ValueError):
            logger.error(f"Invalid achievement criteria format: {achievement.criteria}")
            return False
    
    if 'perfect_quiz' in achievement.criteria:
        # Check if user has gotten a perfect score on any quiz
        from models import QuizAttempt
        perfect_attempts = QuizAttempt.query.filter_by(
            user_id=user_id,
            score=100,
            passed=True
        ).count()
        return perfect_attempts > 0
    
    return False

def check_farming_achievement_eligibility(user_id, achievement):
    """Check eligibility for farming/sustainability-related achievements"""
    # Get user's sustainable practices
    user_practices = UserPractice.query.filter_by(user_id=user_id).all()
    
    # Import SustainablePractice here to avoid circular import
    from models import SustainablePractice
    
    # Example achievement types:
    if 'implement_first_practice' in achievement.criteria:
        return len([p for p in user_practices if p.status in ['completed', 'verified']]) >= 1
    
    if 'implement_practices' in achievement.criteria:
        # Extract number from criteria like "implement_practices:5"
        try:
            num_required = int(achievement.criteria.split(':')[1])
            implemented_practices = len([p for p in user_practices if p.status in ['completed', 'verified']])
            return implemented_practices >= num_required
        except (IndexError, ValueError):
            logger.error(f"Invalid achievement criteria format: {achievement.criteria}")
            return False
    
    if 'verify_practices' in achievement.criteria:
        # Extract number from criteria like "verify_practices:3"
        try:
            num_required = int(achievement.criteria.split(':')[1])
            verified_practices = len([p for p in user_practices if p.status == 'verified'])
            return verified_practices >= num_required
        except (IndexError, ValueError):
            logger.error(f"Invalid achievement criteria format: {achievement.criteria}")
            return False
    
    if 'complete_challenge' in achievement.criteria:
        # Check if user has completed any challenges
        completed_challenges = UserChallenge.query.filter_by(
            user_id=user_id,
            status='completed'
        ).count()
        return completed_challenges > 0
    
    if 'complete_quest' in achievement.criteria:
        # Check if user has completed any quests
        completed_quests = UserQuest.query.filter_by(
            user_id=user_id,
            status='completed'
        ).count()
        return completed_quests > 0
    
    # Check for category-specific implementations (soil, water, etc.)
    if 'category_expertise' in achievement.criteria:
        # Format: category_expertise:soil:3 (implement 3 soil practices)
        try:
            parts = achievement.criteria.split(':')
            category = parts[1]
            num_required = int(parts[2])
            
            # Get practices in this category
            category_practices = [
                p for p in user_practices 
                if p.status in ['completed', 'verified'] and
                SustainablePractice.query.get(p.practice_id).category == category
            ]
            
            return len(category_practices) >= num_required
        except (IndexError, ValueError):
            logger.error(f"Invalid achievement criteria format: {achievement.criteria}")
            return False
    
    return False

def check_community_achievement_eligibility(user_id, achievement):
    """Check eligibility for community-related achievements"""
    # In a real app, this would check for community participation metrics
    # For this example, we'll just return False since we're not implementing
    # detailed community achievement logic yet
    return False

def check_general_achievement_eligibility(user_id, achievement):
    """Check eligibility for general achievements"""
    # Get user data
    user = User.query.get(user_id)
    
    # Example achievement types:
    if 'reach_level' in achievement.criteria:
        # Extract level from criteria like "reach_level:5"
        try:
            level_required = int(achievement.criteria.split(':')[1])
            return user.level >= level_required
        except (IndexError, ValueError):
            logger.error(f"Invalid achievement criteria format: {achievement.criteria}")
            return False
    
    if 'earn_points' in achievement.criteria:
        # Extract points from criteria like "earn_points:1000"
        try:
            points_required = int(achievement.criteria.split(':')[1])
            return user.total_points >= points_required
        except (IndexError, ValueError):
            logger.error(f"Invalid achievement criteria format: {achievement.criteria}")
            return False
    
    return False

def award_achievement(user_id, achievement_id):
    """
    Award an achievement to a user
    
    Args:
        user_id (int): User ID to award the achievement to
        achievement_id (int): Achievement ID to award
        
    Returns:
        bool: True if awarded successfully, False otherwise
    """
    # Check if user already has this achievement
    existing = UserAchievement.query.filter_by(
        user_id=user_id,
        achievement_id=achievement_id
    ).first()
    
    if existing:
        logger.info(f"User {user_id} already has achievement {achievement_id}")
        return False
    
    # Get achievement details
    achievement = Achievement.query.get(achievement_id)
    if not achievement:
        logger.error(f"Cannot award achievement - Achievement ID {achievement_id} not found")
        return False
    
    # Create user achievement record
    user_achievement = UserAchievement(
        user_id=user_id,
        achievement_id=achievement_id,
        date_earned=datetime.utcnow()
    )
    db.session.add(user_achievement)
    
    # Award points for the achievement
    award_points(
        user_id, 
        achievement.points_awarded, 
        category='learning' if achievement.category == 'learning' else 'farming', 
        description=f"Earned achievement: {achievement.name}"
    )
    
    db.session.commit()
    logger.info(f"Awarded achievement {achievement.name} to User {user_id}")
    
    return True

# Additional functions required by the learning module

def complete_lesson(user_id, lesson_id):
    """
    Mark a lesson as completed and award points
    
    Args:
        user_id (int): User ID completing the lesson
        lesson_id (int): Lesson ID being completed
        
    Returns:
        tuple: (success, points_earned, message)
    """
    from models import LearningLesson, UserLearningProgress
    
    # Get the lesson details
    lesson = LearningLesson.query.get(lesson_id)
    if not lesson:
        return False, 0, "Lesson not found"
    
    # Get or create user progress for this module
    user_progress = UserLearningProgress.query.filter_by(
        user_id=user_id,
        module_id=lesson.module_id
    ).first()
    
    if not user_progress:
        user_progress = UserLearningProgress(
            user_id=user_id,
            module_id=lesson.module_id,
            current_lesson_id=lesson_id,
            lessons_completed="",
            quizzes_completed="",
            points_earned=0,
            last_activity_date=datetime.utcnow()
        )
        db.session.add(user_progress)
    
    # Check if lesson is already completed
    completed_lessons = user_progress.lessons_completed.split(',') if user_progress.lessons_completed else []
    if str(lesson_id) in completed_lessons:
        return True, 0, "Lesson already completed"
    
    # Add lesson to completed lessons
    completed_lessons.append(str(lesson_id))
    user_progress.lessons_completed = ','.join(completed_lessons)
    
    # Update current lesson ID to next lesson
    from models import LearningLesson
    next_lesson = LearningLesson.query.filter(
        LearningLesson.module_id == lesson.module_id,
        LearningLesson.order_index > lesson.order_index
    ).order_by(LearningLesson.order_index).first()
    
    if next_lesson:
        user_progress.current_lesson_id = next_lesson.id
    
    # Award points
    points_earned = lesson.points_awarded
    user_progress.points_earned += points_earned
    user_progress.last_activity_date = datetime.utcnow()
    
    # Check if module is completed (all lessons and quizzes)
    from models import LearningModule, LearningQuiz
    all_lessons = LearningLesson.query.filter_by(module_id=lesson.module_id).all()
    all_lesson_ids = [str(l.id) for l in all_lessons]
    
    all_quizzes = LearningQuiz.query.filter_by(module_id=lesson.module_id).all()
    all_quiz_ids = [str(q.id) for q in all_quizzes]
    
    completed_quizzes = user_progress.quizzes_completed.split(',') if user_progress.quizzes_completed else []
    
    module_completed = set(completed_lessons) >= set(all_lesson_ids) and (not all_quiz_ids or set(completed_quizzes) >= set(all_quiz_ids))
    
    if module_completed and not user_progress.completion_date:
        # Award bonus points for completing module
        module = LearningModule.query.get(lesson.module_id)
        bonus_points = module.points_available
        user_progress.points_earned += bonus_points
        points_earned += bonus_points
        user_progress.completion_date = datetime.utcnow()
        
        award_points(user_id, points_earned, 'learning', f"Completed lesson '{lesson.title}' and module '{module.title}'")
    else:
        award_points(user_id, points_earned, 'learning', f"Completed lesson '{lesson.title}'")
    
    db.session.commit()
    
    # Check for achievements after completion
    check_achievement_eligibility(user_id)
    
    return True, points_earned, "Lesson completed successfully"

def complete_quiz(user_id, quiz_id, score, time_spent, passed, answers=None):
    """
    Record quiz completion and award points if passed
    
    Args:
        user_id (int): User ID completing the quiz
        quiz_id (int): Quiz ID being completed
        score (int): Score as percentage (0-100)
        time_spent (int): Time spent in seconds
        passed (bool): Whether user passed the quiz
        answers (list): Optional list of answer data
        
    Returns:
        tuple: (success, points_earned, message)
    """
    from models import LearningQuiz, UserLearningProgress, QuizAttempt, QuizAnswer
    
    # Get the quiz details
    quiz = LearningQuiz.query.get(quiz_id)
    if not quiz:
        return False, 0, "Quiz not found"
    
    # Get or create user progress for this module
    user_progress = UserLearningProgress.query.filter_by(
        user_id=user_id,
        module_id=quiz.module_id
    ).first()
    
    if not user_progress:
        user_progress = UserLearningProgress(
            user_id=user_id,
            module_id=quiz.module_id,
            lessons_completed="",
            quizzes_completed="",
            points_earned=0,
            last_activity_date=datetime.utcnow()
        )
        db.session.add(user_progress)
    
    # Create quiz attempt record
    previous_attempts = QuizAttempt.query.filter_by(
        user_id=user_id,
        quiz_id=quiz_id
    ).count()
    
    attempt = QuizAttempt(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        passed=passed,
        time_spent=time_spent,
        attempt_number=previous_attempts + 1,
        started_at=datetime.utcnow() - timedelta(seconds=time_spent),
        completed_at=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.flush()  # To get attempt.id
    
    # Record answers if provided
    if answers:
        for answer_data in answers:
            answer = QuizAnswer(
                attempt_id=attempt.id,
                question_id=answer_data.get('question_id'),
                selected_choice_id=answer_data.get('selected_choice_id'),
                text_answer=answer_data.get('text_answer'),
                is_correct=answer_data.get('is_correct', False),
                points_earned=answer_data.get('points_earned', 0)
            )
            db.session.add(answer)
    
    points_earned = 0
    
    # If this is the first successful completion, award points and mark as completed
    if passed:
        completed_quizzes = user_progress.quizzes_completed.split(',') if user_progress.quizzes_completed else []
        first_completion = str(quiz_id) not in completed_quizzes
        
        if first_completion:
            # Add quiz to completed quizzes
            completed_quizzes.append(str(quiz_id))
            user_progress.quizzes_completed = ','.join(completed_quizzes)
            
            # Award points
            points_earned = quiz.points_awarded
            user_progress.points_earned += points_earned
            award_points(user_id, points_earned, 'learning', f"Passed quiz '{quiz.title}'")
            
            # Check if module is completed (all lessons and quizzes)
            from models import LearningModule, LearningLesson
            all_lessons = LearningLesson.query.filter_by(module_id=quiz.module_id).all()
            all_lesson_ids = [str(l.id) for l in all_lessons]
            
            all_quizzes = LearningQuiz.query.filter_by(module_id=quiz.module_id).all()
            all_quiz_ids = [str(q.id) for q in all_quizzes]
            
            completed_lessons = user_progress.lessons_completed.split(',') if user_progress.lessons_completed else []
            
            module_completed = set(completed_lessons) >= set(all_lesson_ids) and set(completed_quizzes) >= set(all_quiz_ids)
            
            if module_completed and not user_progress.completion_date:
                # Award bonus points for completing module
                module = LearningModule.query.get(quiz.module_id)
                bonus_points = module.points_available
                user_progress.points_earned += bonus_points
                points_earned += bonus_points
                user_progress.completion_date = datetime.utcnow()
                
                award_points(user_id, bonus_points, 'learning', f"Completed module '{module.title}'")
    
    user_progress.last_activity_date = datetime.utcnow()
    db.session.commit()
    
    # Check for achievements after completion
    if passed:
        check_achievement_eligibility(user_id)
    
    return True, points_earned, "Quiz completed" + (" and passed" if passed else " but not passed")

def get_user_learning_stats(user_id):
    """
    Get statistics about a user's learning progress
    
    Args:
        user_id (int): User ID to get stats for
        
    Returns:
        dict: Statistics about user's learning progress
    """
    from models import (User, UserLearningProgress, LearningModule, 
                       UserAchievement, Achievement)
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Get count of completed modules
    completed_modules = UserLearningProgress.query.filter(
        UserLearningProgress.user_id == user_id,
        UserLearningProgress.completion_date != None
    ).count()
    
    # Get in-progress modules
    in_progress_modules = UserLearningProgress.query.filter(
        UserLearningProgress.user_id == user_id,
        UserLearningProgress.completion_date == None
    ).count()
    
    # Get learning achievements
    learning_achievements = UserAchievement.query.join(
        Achievement, Achievement.id == UserAchievement.achievement_id
    ).filter(
        UserAchievement.user_id == user_id,
        Achievement.category == 'learning'
    ).count()
    
    # Get total available modules
    total_modules = LearningModule.query.filter_by(active=True).count()
    
    # Get recently active modules
    recent_activity = UserLearningProgress.query.filter(
        UserLearningProgress.user_id == user_id,
        UserLearningProgress.last_activity_date >= datetime.utcnow() - timedelta(days=7)
    ).order_by(UserLearningProgress.last_activity_date.desc()).all()
    
    recent_modules = []
    for progress in recent_activity:
        module = LearningModule.query.get(progress.module_id)
        if module:
            recent_modules.append({
                'id': module.id,
                'title': module.title,
                'last_activity': progress.last_activity_date,
                'completion_percentage': calculate_module_completion_percentage(user_id, module.id)
            })
    
    return {
        'learning_points': user.learning_points,
        'completed_modules': completed_modules,
        'in_progress_modules': in_progress_modules,
        'learning_achievements': learning_achievements,
        'total_modules': total_modules,
        'completion_percentage': int(completed_modules / total_modules * 100) if total_modules > 0 else 0,
        'recent_modules': recent_modules
    }

def calculate_module_completion_percentage(user_id, module_id):
    """
    Calculate completion percentage for a specific module
    
    Args:
        user_id (int): User ID
        module_id (int): Module ID
        
    Returns:
        int: Completion percentage (0-100)
    """
    from models import (LearningModule, LearningLesson, LearningQuiz,
                       UserLearningProgress)
    
    # Get user progress
    progress = UserLearningProgress.query.filter_by(
        user_id=user_id,
        module_id=module_id
    ).first()
    
    if not progress:
        return 0
    
    # If module is marked as completed, return 100%
    if progress.completion_date:
        return 100
    
    # Get all lessons and quizzes in the module
    all_lessons = LearningLesson.query.filter_by(module_id=module_id).all()
    all_quizzes = LearningQuiz.query.filter_by(module_id=module_id).all()
    
    total_items = len(all_lessons) + len(all_quizzes)
    if total_items == 0:
        return 0
    
    # Count completed items
    completed_lessons = progress.lessons_completed.split(',') if progress.lessons_completed else []
    completed_quizzes = progress.quizzes_completed.split(',') if progress.quizzes_completed else []
    
    if '' in completed_lessons:
        completed_lessons.remove('')
    if '' in completed_quizzes:
        completed_quizzes.remove('')
    
    completed_items = len(completed_lessons) + len(completed_quizzes)
    
    return int(completed_items / total_items * 100)

def get_achievements(user_id=None, category=None):
    """
    Get achievements for a user or all available achievements
    
    Args:
        user_id (int): Optional user ID to get earned achievements
        category (str): Optional category to filter achievements
        
    Returns:
        list: List of achievement objects
    """
    from models import Achievement, UserAchievement
    
    query = Achievement.query
    
    if category:
        query = query.filter(Achievement.category == category)
    
    if user_id:
        # Get achievements earned by this user
        achievements = UserAchievement.query.filter_by(user_id=user_id).all()
        achievement_ids = [ua.achievement_id for ua in achievements]
        return Achievement.query.filter(Achievement.id.in_(achievement_ids)).all()
    else:
        # Get all available achievements (excluding hidden ones)
        return query.filter(Achievement.is_hidden == False).all()

def check_achievements(user_id):
    """
    Legacy wrapper for check_achievement_eligibility
    """
    return check_achievement_eligibility(user_id)

def calculate_points_to_next_level(user_id):
    """
    Calculate points needed to reach the next level
    
    Args:
        user_id (int): User ID
        
    Returns:
        dict: Dictionary with points_to_next_level and percentage
    """
    user = User.query.get(user_id)
    if not user:
        return {'points_to_next_level': 100, 'percentage': 0}
    
    level_progress = get_user_level_progress(user_id)
    
    return {
        'points_to_next_level': level_progress['points_to_next_level'],
        'percentage': level_progress['progress_percentage']
    }