"""
Routes for sustainability features including sustainable practices, 
challenges, and achievements
"""
import logging
import os
import json
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import (
    db, User, SustainablePractice, SustainabilityChallenge, 
    SustainabilityQuest, UserQuest, QuestStep, ChallengePractice,
    UserSustainablePractice, UserChallenge, UserQuestProgress
)
from utils.gamification import award_points, check_achievement_eligibility

# Create Blueprint
sustainability_bp = Blueprint('sustainability', __name__, url_prefix='/sustainability')
logger = logging.getLogger(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads/practices'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper functions
def allowed_file(filename):
    """Check if a file is allowed based on its extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_implementation_photos(photos, user_id, practice_id):
    """Process and store photo uploads for practice implementation"""
    if not photos:
        return None
        
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    user_dir = os.path.join(UPLOAD_FOLDER, f'user_{user_id}')
    os.makedirs(user_dir, exist_ok=True)
    
    # Timestamp for unique filenames
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    
    saved_files = []
    # Limit to 3 files
    for i, photo in enumerate(photos):
        if i >= 3:
            break
            
        if photo and allowed_file(photo.filename):
            original_filename = secure_filename(photo.filename)
            extension = original_filename.rsplit('.', 1)[1].lower()
            new_filename = f'practice_{practice_id}_{timestamp}_{i}.{extension}'
            
            # Save the file
            file_path = os.path.join(user_dir, new_filename)
            photo.save(file_path)
            
            # Add to saved files list (with path relative to static folder)
            relative_path = '/'.join(file_path.split(os.sep)[1:])  # Remove 'static/' prefix
            saved_files.append('/' + relative_path)
    
    # Return JSON string of file paths
    return json.dumps(saved_files) if saved_files else None

@sustainability_bp.route('/')
@login_required
def index():
    """Sustainability dashboard view"""
    # Get sustainability stats
    stats = {
        'implemented_practices': UserSustainablePractice.query.filter_by(
            user_id=current_user.id, 
            status='verified'
        ).count(),
        'active_challenges': UserChallenge.query.filter_by(
            user_id=current_user.id, 
            status='in_progress'
        ).count(),
        'completed_challenges': UserChallenge.query.filter_by(
            user_id=current_user.id, 
            status='completed'
        ).count(),
        'active_quests': UserQuest.query.filter_by(
            user_id=current_user.id, 
            status='in_progress'
        ).count()
    }
    
    # Get recent sustainable practices
    recent_practices = UserSustainablePractice.query.filter_by(
        user_id=current_user.id
    ).order_by(
        UserSustainablePractice.updated_at.desc()
    ).limit(5).all()
    
    # Get active challenges
    active_challenges = UserChallenge.query.filter_by(
        user_id=current_user.id, 
        status='in_progress'
    ).all()
    
    # Get recommended practices (those not yet implemented)
    implemented_practices = [
        p.practice_id for p in UserSustainablePractice.query.filter_by(
            user_id=current_user.id
        ).all()
    ]
    
    recommended_practices = SustainablePractice.query.filter(
        SustainablePractice.active == True,
        ~SustainablePractice.id.in_(implemented_practices) if implemented_practices else True
    ).order_by(
        SustainablePractice.impact_level.desc()
    ).limit(3).all()
    
    return render_template(
        'sustainability/dashboard.html',
        stats=stats,
        recent_practices=recent_practices,
        active_challenges=active_challenges,
        recommended_practices=recommended_practices
    )

@sustainability_bp.route('/practices')
@login_required
def practices():
    """View all sustainable practices"""
    # Get practices categorized by type
    soil_practices = SustainablePractice.query.filter_by(
        category='soil', 
        active=True
    ).all()
    
    water_practices = SustainablePractice.query.filter_by(
        category='water', 
        active=True
    ).all()
    
    biodiversity_practices = SustainablePractice.query.filter_by(
        category='biodiversity', 
        active=True
    ).all()
    
    integrated_practices = SustainablePractice.query.filter_by(
        category='integrated', 
        active=True
    ).all()
    
    climate_practices = SustainablePractice.query.filter_by(
        category='climate', 
        active=True
    ).all()
    
    # Get user implemented practices
    user_practices = {
        p.practice_id: p for p in UserSustainablePractice.query.filter_by(
            user_id=current_user.id
        ).all()
    }
    
    return render_template(
        'sustainability/practices.html',
        soil_practices=soil_practices,
        water_practices=water_practices,
        biodiversity_practices=biodiversity_practices,
        integrated_practices=integrated_practices,
        climate_practices=climate_practices,
        user_practices=user_practices
    )

@sustainability_bp.route('/practices/<int:practice_id>')
@login_required
def practice_detail(practice_id):
    """View details of a sustainable practice"""
    practice = SustainablePractice.query.get_or_404(practice_id)
    
    # Check if user has implemented this practice
    user_practice = UserSustainablePractice.query.filter_by(
        user_id=current_user.id,
        practice_id=practice_id
    ).first()
    
    # Find related practices in the same category
    related_practices = SustainablePractice.query.filter(
        SustainablePractice.category == practice.category,
        SustainablePractice.id != practice.id,
        SustainablePractice.active == True
    ).limit(3).all()
    
    # Find challenges that include this practice
    challenges = SustainabilityChallenge.query.filter(
        SustainabilityChallenge.id.in_(
            db.session.query(ChallengePractice.challenge_id).filter_by(
                practice_id=practice_id
            )
        )
    ).all()
    
    return render_template(
        'sustainability/practice_detail.html',
        practice=practice,
        user_practice=user_practice,
        related_practices=related_practices,
        challenges=challenges
    )

@sustainability_bp.route('/practices/<int:practice_id>/implement', methods=['POST'])
@login_required
def implement_practice(practice_id):
    """Mark a practice as implemented"""
    practice = SustainablePractice.query.get_or_404(practice_id)
    
    # Check if already implemented
    existing = UserSustainablePractice.query.filter_by(
        user_id=current_user.id,
        practice_id=practice_id
    ).first()
    
    if existing:
        if existing.status == 'implemented':
            flash('You have already marked this practice as implemented.', 'info')
        elif existing.status == 'verified':
            flash('This practice has already been verified.', 'info')
        elif existing.status == 'rejected':
            # Allow re-implementation if previously rejected
            existing.status = 'implemented'
            
            # Update basic fields
            existing.notes = request.form.get('notes', '')
            existing.updated_at = datetime.utcnow()
            
            # Update location information
            existing.farm_area_name = request.form.get('farm_area_name', '')
            existing.area_size = float(request.form.get('area_size', 0)) if request.form.get('area_size') else None
            existing.latitude = float(request.form.get('latitude', 0)) if request.form.get('latitude') else None
            existing.longitude = float(request.form.get('longitude', 0)) if request.form.get('longitude') else None
            
            # Update resource information
            existing.resources_used = request.form.get('resources_used', '')
            existing.cost = float(request.form.get('cost', 0)) if request.form.get('cost') else None
            existing.labor_hours = float(request.form.get('labor_hours', 0)) if request.form.get('labor_hours') else None
            
            # Process new photos if provided
            photos = request.files.getlist('photos')
            if photos and any(photo.filename for photo in photos):
                impact_images = handle_implementation_photos(photos, current_user.id, practice_id)
                if impact_images:
                    existing.impact_images = impact_images
            
            # Calculate carbon impact if area_size is provided
            if existing.area_size and existing.area_size > 0:
                existing.calculate_carbon_impact()
                
            db.session.commit()
            flash('You have re-implemented this sustainable practice.', 'success')
        return redirect(url_for('sustainability.practice_detail', practice_id=practice_id))
    
    # Process photo uploads
    photos = request.files.getlist('photos')
    impact_images = handle_implementation_photos(photos, current_user.id, practice_id)
    
    # Create new implementation
    implementation = UserSustainablePractice(
        user_id=current_user.id,
        practice_id=practice_id,
        status='implemented',
        notes=request.form.get('notes', ''),
        implementation_date=datetime.utcnow(),
        
        # Location information
        farm_area_name=request.form.get('farm_area_name', ''),
        area_size=float(request.form.get('area_size', 0)) if request.form.get('area_size') else None,
        latitude=float(request.form.get('latitude', 0)) if request.form.get('latitude') else None,
        longitude=float(request.form.get('longitude', 0)) if request.form.get('longitude') else None,
        
        # Resource information
        resources_used=request.form.get('resources_used', ''),
        cost=float(request.form.get('cost', 0)) if request.form.get('cost') else None,
        labor_hours=float(request.form.get('labor_hours', 0)) if request.form.get('labor_hours') else None,
        
        # Implementation photos
        impact_images=impact_images
    )
    
    db.session.add(implementation)
    db.session.commit()
    
    # Calculate carbon impact if area_size is provided
    if implementation.area_size and implementation.area_size > 0:
        implementation.calculate_carbon_impact()
        db.session.commit()
    
    flash('You have marked this practice as implemented. It will be verified soon.', 'success')
    return redirect(url_for('sustainability.practice_detail', practice_id=practice_id))

@sustainability_bp.route('/challenges')
@login_required
def challenges():
    """View all sustainability challenges"""
    # Get active challenges
    active_challenges = SustainabilityChallenge.query.filter_by(
        active=True
    ).all()
    
    # Get user challenges
    user_challenges = {
        c.challenge_id: c for c in UserChallenge.query.filter_by(
            user_id=current_user.id
        ).all()
    }
    
    return render_template(
        'sustainability/challenges.html',
        active_challenges=active_challenges,
        user_challenges=user_challenges
    )

@sustainability_bp.route('/challenges/<int:challenge_id>')
@login_required
def challenge_detail(challenge_id):
    """View details of a sustainability challenge"""
    challenge = SustainabilityChallenge.query.get_or_404(challenge_id)
    
    # Check if user is participating in this challenge
    user_challenge = UserChallenge.query.filter_by(
        user_id=current_user.id,
        challenge_id=challenge_id
    ).first()
    
    # Get required practices for this challenge
    practices = SustainablePractice.query.filter(
        SustainablePractice.id.in_(
            db.session.query(ChallengePractice.practice_id).filter_by(
                challenge_id=challenge_id
            )
        )
    ).all()
    
    # Check which practices the user has implemented
    implemented_practices = set(
        p.practice_id for p in UserSustainablePractice.query.filter(
            UserSustainablePractice.user_id == current_user.id,
            UserSustainablePractice.practice_id.in_([p.id for p in practices]),
            UserSustainablePractice.status.in_(['implemented', 'verified'])
        ).all()
    )
    
    return render_template(
        'sustainability/challenge_detail.html',
        challenge=challenge,
        user_challenge=user_challenge,
        practices=practices,
        implemented_practices=implemented_practices
    )

@sustainability_bp.route('/challenges/<int:challenge_id>/join', methods=['POST'])
@login_required
def join_challenge(challenge_id):
    """Join a sustainability challenge"""
    challenge = SustainabilityChallenge.query.get_or_404(challenge_id)
    
    # Check if already participating
    existing = UserChallenge.query.filter_by(
        user_id=current_user.id,
        challenge_id=challenge_id
    ).first()
    
    if existing:
        if existing.status == 'in_progress':
            flash('You are already participating in this challenge.', 'info')
        elif existing.status == 'completed':
            flash('You have already completed this challenge.', 'info')
        return redirect(url_for('sustainability.challenge_detail', challenge_id=challenge_id))
    
    # Join the challenge
    user_challenge = UserChallenge(
        user_id=current_user.id,
        challenge_id=challenge_id,
        status='in_progress',
        start_date=datetime.utcnow()
    )
    
    db.session.add(user_challenge)
    db.session.commit()
    
    flash('You have joined this sustainability challenge!', 'success')
    return redirect(url_for('sustainability.challenge_detail', challenge_id=challenge_id))

@sustainability_bp.route('/quests')
@login_required
def quests():
    """View all sustainability quests"""
    # Get active quests
    active_quests = SustainabilityQuest.query.filter_by(
        active=True
    ).all()
    
    # Get user quests
    user_quests = {
        q.quest_id: q for q in UserQuest.query.filter_by(
            user_id=current_user.id
        ).all()
    }
    
    return render_template(
        'sustainability/quests.html',
        active_quests=active_quests,
        user_quests=user_quests
    )

@sustainability_bp.route('/quests/<int:quest_id>')
@login_required
def quest_detail(quest_id):
    """View details of a sustainability quest"""
    quest = SustainabilityQuest.query.get_or_404(quest_id)
    
    # Check if user is participating in this quest
    user_quest = UserQuest.query.filter_by(
        user_id=current_user.id,
        quest_id=quest_id
    ).first()
    
    # Get steps for this quest
    steps = QuestStep.query.filter_by(
        quest_id=quest_id
    ).order_by(
        QuestStep.step_number
    ).all()
    
    # Get user progress on each step
    user_step_progress = {}
    if user_quest:
        progress_entries = UserQuestProgress.query.filter_by(
            user_quest_id=user_quest.id
        ).all()
        user_step_progress = {
            p.step_id: p for p in progress_entries
        }
    
    return render_template(
        'sustainability/quest_detail.html',
        quest=quest,
        user_quest=user_quest,
        steps=steps,
        user_step_progress=user_step_progress,
        now=datetime.utcnow()
    )

@sustainability_bp.route('/quests/<int:quest_id>/start', methods=['POST'])
@login_required
def start_quest(quest_id):
    """Start a sustainability quest"""
    quest = SustainabilityQuest.query.get_or_404(quest_id)
    
    # Check if already participating
    existing = UserQuest.query.filter_by(
        user_id=current_user.id,
        quest_id=quest_id
    ).first()
    
    if existing:
        if existing.status == 'in_progress':
            flash('You are already participating in this quest.', 'info')
        elif existing.status == 'completed':
            flash('You have already completed this quest.', 'info')
        return redirect(url_for('sustainability.quest_detail', quest_id=quest_id))
    
    # Start the quest
    user_quest = UserQuest(
        user_id=current_user.id,
        quest_id=quest_id,
        status='in_progress',
        start_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=quest.time_limit_days)
    )
    
    db.session.add(user_quest)
    db.session.commit()
    
    flash('You have started this sustainability quest!', 'success')
    return redirect(url_for('sustainability.quest_detail', quest_id=quest_id))
    
@sustainability_bp.route('/quests/<int:quest_id>/steps/<int:step_id>/complete', methods=['POST'])
@login_required
def complete_step(quest_id, step_id):
    """Mark a quest step as completed"""
    quest = SustainabilityQuest.query.get_or_404(quest_id)
    step = QuestStep.query.get_or_404(step_id)
    
    # Check if user is participating in this quest
    user_quest = UserQuest.query.filter_by(
        user_id=current_user.id,
        quest_id=quest_id
    ).first()
    
    if not user_quest or user_quest.status != 'in_progress':
        flash('You must start this quest before completing steps.', 'warning')
        return redirect(url_for('sustainability.quest_detail', quest_id=quest_id))
    
    # Check if this step is already completed
    existing_progress = UserQuestProgress.query.filter_by(
        user_quest_id=user_quest.id,
        step_id=step_id
    ).first()
    
    if existing_progress:
        if existing_progress.status == 'completed':
            flash('You have already completed this step.', 'info')
        return redirect(url_for('sustainability.quest_detail', quest_id=quest_id))
    
    # Create new progress entry or update existing
    if existing_progress:
        existing_progress.status = 'completed'
        existing_progress.notes = request.form.get('notes', '')
        existing_progress.completion_date = datetime.utcnow()
    else:
        progress = UserQuestProgress(
            user_quest_id=user_quest.id,
            step_id=step_id,
            status='completed',
            notes=request.form.get('notes', ''),
            completion_date=datetime.utcnow()
        )
        db.session.add(progress)
    
    # Update user quest progress percentage
    total_steps = QuestStep.query.filter_by(quest_id=quest_id).count()
    completed_steps = UserQuestProgress.query.filter_by(
        user_quest_id=user_quest.id,
        status='completed'
    ).count() + (0 if existing_progress else 1)  # Add 1 if this is a new completion
    
    progress_percentage = int((completed_steps / total_steps) * 100) if total_steps > 0 else 0
    user_quest.progress_percentage = progress_percentage
    
    # Check if all steps are completed
    if progress_percentage == 100:
        user_quest.status = 'completed'
        user_quest.completion_date = datetime.utcnow()
        user_quest.points_earned = quest.points_awarded
        
        # Award points to user
        award_points(current_user.id, quest.points_awarded, 'sustainability', f"Completed quest: {quest.title}")
        
        # Check if badge should be awarded
        if quest.badge_awarded:
            user_quest.badge_earned = True
            check_achievement_eligibility(current_user.id)
            
        flash(f'Congratulations! You have completed the quest "{quest.title}" and earned {quest.points_awarded} points!', 'success')
    else:
        flash('Step completed successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('sustainability.quest_detail', quest_id=quest_id))