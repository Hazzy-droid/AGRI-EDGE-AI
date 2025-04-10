"""
Seed script for populating sustainability-related data
"""
import logging
from datetime import datetime, timedelta
from app import db
from models import (
    SustainablePractice, SustainabilityChallenge, 
    SustainabilityQuest, QuestStep, ChallengePractice,
    Achievement
)

logger = logging.getLogger(__name__)

def seed_sustainable_practices():
    """Seed the database with sustainable farming practices"""
    
    # Check if data already exists
    if SustainablePractice.query.count() > 0:
        logger.info("Sustainable practices data already exists")
        return

    logger.info("Seeding sustainable practices...")
    
    practices = [
        # Soil Health Practices
        {
            'name': 'Cover Cropping',
            'description': 'Grow specific plants to cover and protect the soil during periods when regular crops are not being grown. Cover crops improve soil health by adding organic matter, reducing erosion, suppressing weeds, and enhancing biodiversity.',
            'category': 'soil',
            'difficulty': 2,
            'impact_level': 4,
            'points_awarded': 150,
            'implementation_steps': '''
                <ol>
                    <li>Select appropriate cover crop species for your region and soil conditions.</li>
                    <li>Prepare the soil after harvesting your main crop.</li>
                    <li>Sow cover crop seeds at the recommended rate and depth.</li>
                    <li>Allow the cover crop to grow until it's time to plant your next main crop.</li>
                    <li>Terminate the cover crop by rolling, mowing, or incorporating it into the soil.</li>
                </ol>
            ''',
            'benefits': 'Reduces soil erosion|Improves soil structure|Adds organic matter|Suppresses weeds|Increases biodiversity|Reduces fertilizer needs',
            'challenges': 'Requires timing and planning|May need specialized equipment|Seed cost|Learning curve for proper management',
            'resources': '''
                <ul>
                    <li><a href="#">Cover Crop Selection Tool</a></li>
                    <li><a href="#">Cover Crop Management Guide</a></li>
                    <li><a href="#">Regional Cover Crop Calculator</a></li>
                </ul>
            ''',
            'active': True
        },
        {
            'name': 'No-Till Farming',
            'description': 'Growing crops without disturbing the soil through tillage. No-till farming increases soil organic matter, reduces erosion, improves soil structure, and saves time and fuel costs.',
            'category': 'soil',
            'difficulty': 3,
            'impact_level': 5,
            'points_awarded': 200,
            'implementation_steps': '''
                <ol>
                    <li>Invest in or access appropriate no-till planting equipment.</li>
                    <li>Develop an effective weed management plan.</li>
                    <li>Adjust your fertilizer application strategy.</li>
                    <li>Plant directly into crop residue or cover crops.</li>
                    <li>Monitor and adapt your approach based on results.</li>
                </ol>
            ''',
            'benefits': 'Reduces soil erosion|Improves soil structure|Increases soil organic matter|Saves fuel and labor costs|Reduces carbon emissions|Enhances soil biodiversity',
            'challenges': 'Requires specialized equipment|Different weed management approaches|Soil may take time to adjust|May need more careful nutrient management initially',
            'active': True
        },
        {
            'name': 'Crop Rotation',
            'description': 'Growing different types of crops in the same area across a sequence of growing seasons. This practice helps manage soil fertility, soil-borne diseases, and pest cycles in an environmentally friendly way.',
            'category': 'soil',
            'difficulty': 2,
            'impact_level': 4,
            'points_awarded': 150,
            'active': True
        },
        {
            'name': 'Integrated Soil Fertility Management',
            'description': 'Combining organic and inorganic fertilizers with improved germplasm and local knowledge to increase productivity while maintaining soil health.',
            'category': 'soil',
            'difficulty': 3,
            'impact_level': 4,
            'points_awarded': 180,
            'active': True
        },
        
        # Water Conservation Practices
        {
            'name': 'Drip Irrigation',
            'description': 'A micro-irrigation system that saves water and nutrients by allowing water to drip slowly to the roots of plants through a network of valves, pipes, tubing, and emitters.',
            'category': 'water',
            'difficulty': 3,
            'impact_level': 5,
            'points_awarded': 200,
            'implementation_steps': '''
                <ol>
                    <li>Design your drip irrigation system based on your farm layout and water source.</li>
                    <li>Purchase necessary components: mainline, sub-main lines, drip lines, filters, pressure regulators, etc.</li>
                    <li>Install the main water source connection and filtering system.</li>
                    <li>Lay out the mainlines and sub-main lines according to your design.</li>
                    <li>Connect drip lines and emitters to deliver water to your crops.</li>
                    <li>Test the system and make adjustments as needed.</li>
                    <li>Implement a maintenance routine for cleaning filters and checking for leaks.</li>
                </ol>
            ''',
            'benefits': 'Reduces water usage by 30-50%|Decreases weed growth|Minimizes fertilizer leaching|Improves crop quality and yield|Reduces energy costs|Allows precise water application',
            'challenges': 'Initial installation cost|Requires regular maintenance|Potential clogging of emitters|Needs filtering system|May require technical knowledge',
            'active': True
        },
        {
            'name': 'Rainwater Harvesting',
            'description': 'Collecting and storing rainwater for agricultural use, reducing dependence on groundwater and other water sources.',
            'category': 'water',
            'difficulty': 2,
            'impact_level': 4,
            'points_awarded': 160,
            'active': True
        },
        {
            'name': 'Mulching',
            'description': 'Covering the soil surface with organic or inorganic materials to conserve soil moisture, suppress weeds, and improve soil conditions.',
            'category': 'water',
            'difficulty': 1,
            'impact_level': 3,
            'points_awarded': 100,
            'active': True
        },
        {
            'name': 'Water-Efficient Crop Selection',
            'description': 'Growing drought-resistant or water-efficient crop varieties that require less irrigation while maintaining productivity.',
            'category': 'water',
            'difficulty': 2,
            'impact_level': 4,
            'points_awarded': 150,
            'active': True
        },
        
        # Biodiversity Practices
        {
            'name': 'Agroforestry',
            'description': 'Integrating trees with crop production and/or livestock farming to create environmental, economic, and social benefits.',
            'category': 'biodiversity',
            'difficulty': 4,
            'impact_level': 5,
            'points_awarded': 250,
            'implementation_steps': '''
                <ol>
                    <li>Assess your land and determine the appropriate agroforestry system (alley cropping, silvopasture, forest farming, etc.).</li>
                    <li>Select compatible tree and crop/livestock species based on your climate and goals.</li>
                    <li>Design your planting layout considering spacing, orientation, and future growth.</li>
                    <li>Prepare the land and establish tree seedlings or saplings.</li>
                    <li>Implement management practices for both trees and crops/livestock.</li>
                    <li>Monitor interactions between components and adjust as needed.</li>
                    <li>Develop long-term maintenance and harvest plans.</li>
                </ol>
            ''',
            'benefits': 'Increases biodiversity|Improves soil health|Enhances carbon sequestration|Provides multiple income sources|Creates wildlife habitat|Reduces erosion|Improves water quality',
            'challenges': 'Requires long-term planning|Initial establishment costs|Potential competition between trees and crops|Complexity of management|May reduce area for crop production initially',
            'active': True
        },
        {
            'name': 'Pollinator Habitat Creation',
            'description': 'Establishing areas with native flowering plants to support bees, butterflies, and other pollinators essential for crop production.',
            'category': 'biodiversity',
            'difficulty': 2,
            'impact_level': 4,
            'points_awarded': 150,
            'active': True
        },
        {
            'name': 'Beneficial Insect Habitats',
            'description': 'Creating environments that attract and sustain insects that prey on crop pests, reducing the need for chemical pesticides.',
            'category': 'biodiversity',
            'difficulty': 3,
            'impact_level': 4,
            'points_awarded': 180,
            'active': True
        },
        {
            'name': 'Native Ecosystem Preservation',
            'description': 'Protecting and maintaining areas of native vegetation within or adjacent to farmland to support local biodiversity.',
            'category': 'biodiversity',
            'difficulty': 3,
            'impact_level': 4,
            'points_awarded': 200,
            'active': True
        },
        
        # Integrated Systems
        {
            'name': 'Integrated Pest Management (IPM)',
            'description': 'A holistic approach to pest control that uses a combination of biological, cultural, physical, and chemical methods to minimize economic, health, and environmental risks.',
            'category': 'integrated',
            'difficulty': 3,
            'impact_level': 4,
            'points_awarded': 200,
            'implementation_steps': '''
                <ol>
                    <li>Learn to identify common pests and beneficial insects in your area.</li>
                    <li>Establish monitoring systems to regularly check for pest presence and population levels.</li>
                    <li>Determine economic thresholds for when pest control action is necessary.</li>
                    <li>Implement preventive cultural practices (crop rotation, resistant varieties, etc.).</li>
                    <li>Use biological controls when possible (beneficial insects, microbial products).</li>
                    <li>Apply physical and mechanical controls as needed (traps, barriers).</li>
                    <li>Use targeted chemical controls only when other methods are insufficient.</li>
                    <li>Evaluate results and adjust strategies accordingly.</li>
                </ol>
            ''',
            'benefits': 'Reduces pesticide use|Minimizes environmental impact|Preserves beneficial organisms|Prevents pest resistance|Improves long-term pest control|Reduces chemical residues in food',
            'challenges': 'Requires knowledge and training|More time-intensive initially|Needs regular monitoring|May have slower immediate results than conventional pest control',
            'active': True
        },
        {
            'name': 'Integrated Crop-Livestock Systems',
            'description': 'Combining crop and livestock production in a way that the outputs from one component serve as inputs for the other, creating a more efficient and sustainable farm system.',
            'category': 'integrated',
            'difficulty': 4,
            'impact_level': 5,
            'points_awarded': 250,
            'active': True
        },
        {
            'name': 'Precision Agriculture',
            'description': 'Using technology to optimize inputs (seeds, fertilizers, water) by applying the right amount at the right time and place, improving efficiency and reducing waste.',
            'category': 'integrated',
            'difficulty': 4,
            'impact_level': 4,
            'points_awarded': 230,
            'active': True
        },
        {
            'name': 'Permaculture Design',
            'description': 'A whole-systems approach to land management that adopts patterns observed in natural ecosystems to create sustainable and self-sufficient agricultural systems.',
            'category': 'integrated',
            'difficulty': 4,
            'impact_level': 5,
            'points_awarded': 250,
            'active': True
        },
        
        # Climate Resilience
        {
            'name': 'Climate-Smart Crop Selection',
            'description': 'Growing crop varieties that are adapted to changing climate conditions, including heat and drought tolerance, pest resistance, and varying maturity dates.',
            'category': 'climate',
            'difficulty': 3,
            'impact_level': 5,
            'points_awarded': 200,
            'implementation_steps': '''
                <ol>
                    <li>Assess current and projected climate changes for your region.</li>
                    <li>Identify climate-related risks to your current farming system.</li>
                    <li>Research crop varieties that show resilience to these specific conditions.</li>
                    <li>Consider diversifying with multiple varieties to spread risk.</li>
                    <li>Source quality seeds from reputable suppliers or community seed banks.</li>
                    <li>Test new varieties on small plots before large-scale implementation.</li>
                    <li>Document performance under different weather conditions.</li>
                    <li>Adjust planting schedules based on changing seasonal patterns.</li>
                </ol>
            ''',
            'benefits': 'Reduces vulnerability to climate extremes|Stabilizes yields during variable conditions|Decreases crop failure risk|Potential for better market adaptation|Enhances farm sustainability|Provides food security',
            'challenges': 'Limited availability of climate-adapted varieties|May require new farming techniques|Uncertain performance in extreme conditions|Possible yield trade-offs|Seed cost for improved varieties',
            'active': True
        },
        {
            'name': 'Conservation Agriculture',
            'description': 'A farming system that promotes minimum soil disturbance, permanent soil cover, and crop rotation to improve soil health and resilience to climate change.',
            'category': 'climate',
            'difficulty': 3,
            'impact_level': 5,
            'points_awarded': 220,
            'active': True
        },
        {
            'name': 'Diversified Farming Systems',
            'description': 'Growing multiple types of crops and/or integrating livestock to reduce risk and enhance resilience to climate-related failures of individual farm components.',
            'category': 'climate',
            'difficulty': 3,
            'impact_level': 4,
            'points_awarded': 180,
            'active': True
        },
        {
            'name': 'Carbon Farming',
            'description': 'Implementing practices that capture carbon in soil and vegetation, reducing greenhouse gas emissions while improving soil health and productivity.',
            'category': 'climate',
            'difficulty': 4,
            'impact_level': 5,
            'points_awarded': 250,
            'active': True
        }
    ]
    
    # Add practices to database
    for practice_data in practices:
        practice = SustainablePractice(**practice_data)
        db.session.add(practice)
    
    db.session.commit()
    logger.info(f"Added {len(practices)} sustainable practices")

def seed_sustainability_challenges():
    """Seed the database with sustainability challenges"""
    
    # Check if data already exists
    if SustainabilityChallenge.query.count() > 0:
        logger.info("Sustainability challenges data already exists")
        return

    logger.info("Seeding sustainability challenges...")
    
    # Create achievements first if needed
    if Achievement.query.count() == 0:
        logger.info("Creating necessary achievements first...")
        achievements = [
            {
                'name': 'Soil Guardian',
                'description': 'Earned by completing the Soil Health Challenge',
                'category': 'sustainability',
                'points_required': 0,
                'image_url': '/static/images/achievements/soil_guardian.png',
                'hidden': False
            },
            {
                'name': 'Water Steward',
                'description': 'Earned by completing the Water Conservation Challenge',
                'category': 'sustainability',
                'points_required': 0,
                'image_url': '/static/images/achievements/water_steward.png',
                'hidden': False
            },
            {
                'name': 'Biodiversity Champion',
                'description': 'Earned by completing the Biodiversity Enhancement Challenge',
                'category': 'sustainability',
                'points_required': 0,
                'image_url': '/static/images/achievements/biodiversity_champion.png',
                'hidden': False
            },
            {
                'name': 'Climate Innovator',
                'description': 'Earned by completing the Climate Resilience Challenge',
                'category': 'sustainability',
                'points_required': 0,
                'image_url': '/static/images/achievements/climate_innovator.png',
                'hidden': False
            },
            {
                'name': 'Integrated Farming Master',
                'description': 'Earned by completing the Integrated Farming Systems Challenge',
                'category': 'sustainability',
                'points_required': 0,
                'image_url': '/static/images/achievements/integrated_master.png',
                'hidden': False
            }
        ]
        
        for achievement_data in achievements:
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
        
        db.session.commit()
        logger.info(f"Added {len(achievements)} achievements")
    
    # Get achievement IDs
    soil_badge = Achievement.query.filter_by(name='Soil Guardian').first()
    water_badge = Achievement.query.filter_by(name='Water Steward').first()
    biodiversity_badge = Achievement.query.filter_by(name='Biodiversity Champion').first()
    climate_badge = Achievement.query.filter_by(name='Climate Innovator').first()
    integrated_badge = Achievement.query.filter_by(name='Integrated Farming Master').first()
    
    # Define challenges
    now = datetime.utcnow()
    challenges = [
        {
            'title': 'Soil Health Challenge',
            'description': 'Improve your soil quality and health by implementing a set of sustainable soil management practices. This challenge will help you build soil organic matter, reduce erosion, and create a better growing environment for your crops.',
            'category': 'individual',
            'difficulty': 2,
            'points_awarded': 500,
            'badge_awarded': soil_badge.id if soil_badge else None,
            'start_date': now,
            'end_date': now + timedelta(days=90),
            'image_url': '/static/images/challenges/soil_health.jpg',
            'active': True
        },
        {
            'title': 'Water Conservation Challenge',
            'description': 'Implement water-saving techniques to reduce water usage on your farm while maintaining or improving crop yields. This challenge focuses on efficient water management practices suitable for your local conditions.',
            'category': 'individual',
            'difficulty': 3,
            'points_awarded': 600,
            'badge_awarded': water_badge.id if water_badge else None,
            'start_date': now,
            'end_date': now + timedelta(days=120),
            'image_url': '/static/images/challenges/water_conservation.jpg',
            'active': True
        },
        {
            'title': 'Biodiversity Enhancement Challenge',
            'description': 'Increase the biodiversity on your farm by creating habitats for beneficial organisms and integrating diverse plant species. This challenge will help you build a more resilient and balanced farm ecosystem.',
            'category': 'community',
            'difficulty': 3,
            'points_awarded': 650,
            'badge_awarded': biodiversity_badge.id if biodiversity_badge else None,
            'start_date': now,
            'end_date': now + timedelta(days=180),
            'image_url': '/static/images/challenges/biodiversity.jpg',
            'active': True
        },
        {
            'title': 'Climate Resilience Challenge',
            'description': 'Make your farm more resilient to climate change impacts by implementing adaptive practices. This challenge focuses on techniques that help your farm withstand extreme weather events and changing climate patterns.',
            'category': 'regional',
            'difficulty': 4,
            'points_awarded': 800,
            'badge_awarded': climate_badge.id if climate_badge else None,
            'start_date': now,
            'end_date': now + timedelta(days=365),
            'image_url': '/static/images/challenges/climate_resilience.jpg',
            'active': True
        },
        {
            'title': 'Integrated Farming Systems Challenge',
            'description': 'Transform your farm into an integrated system where multiple components work together synergistically. This advanced challenge will help you build a more efficient, productive, and sustainable farming operation.',
            'category': 'individual',
            'difficulty': 5,
            'points_awarded': 1000,
            'badge_awarded': integrated_badge.id if integrated_badge else None,
            'start_date': now,
            'end_date': now + timedelta(days=180),
            'image_url': '/static/images/challenges/integrated_farming.jpg',
            'active': True
        }
    ]
    
    # Add challenges to database and link to required practices
    for challenge_data in challenges:
        challenge = SustainabilityChallenge(**challenge_data)
        db.session.add(challenge)
    
    db.session.commit()
    logger.info(f"Added {len(challenges)} sustainability challenges")
    
    # Now link challenges to required practices
    soil_challenge = SustainabilityChallenge.query.filter_by(title='Soil Health Challenge').first()
    water_challenge = SustainabilityChallenge.query.filter_by(title='Water Conservation Challenge').first()
    biodiversity_challenge = SustainabilityChallenge.query.filter_by(title='Biodiversity Enhancement Challenge').first()
    climate_challenge = SustainabilityChallenge.query.filter_by(title='Climate Resilience Challenge').first()
    integrated_challenge = SustainabilityChallenge.query.filter_by(title='Integrated Farming Systems Challenge').first()
    
    # Get practice IDs by name
    cover_crop = SustainablePractice.query.filter_by(name='Cover Cropping').first()
    no_till = SustainablePractice.query.filter_by(name='No-Till Farming').first()
    crop_rotation = SustainablePractice.query.filter_by(name='Crop Rotation').first()
    soil_fertility = SustainablePractice.query.filter_by(name='Integrated Soil Fertility Management').first()
    drip_irrigation = SustainablePractice.query.filter_by(name='Drip Irrigation').first()
    rainwater = SustainablePractice.query.filter_by(name='Rainwater Harvesting').first()
    mulching = SustainablePractice.query.filter_by(name='Mulching').first()
    water_efficient = SustainablePractice.query.filter_by(name='Water-Efficient Crop Selection').first()
    agroforestry = SustainablePractice.query.filter_by(name='Agroforestry').first()
    pollinator = SustainablePractice.query.filter_by(name='Pollinator Habitat Creation').first()
    beneficial_insects = SustainablePractice.query.filter_by(name='Beneficial Insect Habitats').first()
    native_ecosystem = SustainablePractice.query.filter_by(name='Native Ecosystem Preservation').first()
    ipm = SustainablePractice.query.filter_by(name='Integrated Pest Management (IPM)').first()
    crop_livestock = SustainablePractice.query.filter_by(name='Integrated Crop-Livestock Systems').first()
    precision_ag = SustainablePractice.query.filter_by(name='Precision Agriculture').first()
    permaculture = SustainablePractice.query.filter_by(name='Permaculture Design').first()
    climate_crops = SustainablePractice.query.filter_by(name='Climate-Smart Crop Selection').first()
    conservation_ag = SustainablePractice.query.filter_by(name='Conservation Agriculture').first()
    diversified = SustainablePractice.query.filter_by(name='Diversified Farming Systems').first()
    carbon_farming = SustainablePractice.query.filter_by(name='Carbon Farming').first()
    
    # Link challenges to practices
    challenge_practices = []
    
    # Soil Health Challenge
    if soil_challenge and cover_crop:
        challenge_practices.append(ChallengePractice(challenge_id=soil_challenge.id, practice_id=cover_crop.id))
    if soil_challenge and no_till:
        challenge_practices.append(ChallengePractice(challenge_id=soil_challenge.id, practice_id=no_till.id))
    if soil_challenge and crop_rotation:
        challenge_practices.append(ChallengePractice(challenge_id=soil_challenge.id, practice_id=crop_rotation.id))
    if soil_challenge and soil_fertility:
        challenge_practices.append(ChallengePractice(challenge_id=soil_challenge.id, practice_id=soil_fertility.id))
    
    # Water Conservation Challenge
    if water_challenge and drip_irrigation:
        challenge_practices.append(ChallengePractice(challenge_id=water_challenge.id, practice_id=drip_irrigation.id))
    if water_challenge and rainwater:
        challenge_practices.append(ChallengePractice(challenge_id=water_challenge.id, practice_id=rainwater.id))
    if water_challenge and mulching:
        challenge_practices.append(ChallengePractice(challenge_id=water_challenge.id, practice_id=mulching.id))
    if water_challenge and water_efficient:
        challenge_practices.append(ChallengePractice(challenge_id=water_challenge.id, practice_id=water_efficient.id))
    
    # Biodiversity Enhancement Challenge
    if biodiversity_challenge and agroforestry:
        challenge_practices.append(ChallengePractice(challenge_id=biodiversity_challenge.id, practice_id=agroforestry.id))
    if biodiversity_challenge and pollinator:
        challenge_practices.append(ChallengePractice(challenge_id=biodiversity_challenge.id, practice_id=pollinator.id))
    if biodiversity_challenge and beneficial_insects:
        challenge_practices.append(ChallengePractice(challenge_id=biodiversity_challenge.id, practice_id=beneficial_insects.id))
    if biodiversity_challenge and native_ecosystem:
        challenge_practices.append(ChallengePractice(challenge_id=biodiversity_challenge.id, practice_id=native_ecosystem.id))
    
    # Climate Resilience Challenge
    if climate_challenge and climate_crops:
        challenge_practices.append(ChallengePractice(challenge_id=climate_challenge.id, practice_id=climate_crops.id))
    if climate_challenge and conservation_ag:
        challenge_practices.append(ChallengePractice(challenge_id=climate_challenge.id, practice_id=conservation_ag.id))
    if climate_challenge and diversified:
        challenge_practices.append(ChallengePractice(challenge_id=climate_challenge.id, practice_id=diversified.id))
    if climate_challenge and carbon_farming:
        challenge_practices.append(ChallengePractice(challenge_id=climate_challenge.id, practice_id=carbon_farming.id))
    
    # Integrated Farming Systems Challenge
    if integrated_challenge and ipm:
        challenge_practices.append(ChallengePractice(challenge_id=integrated_challenge.id, practice_id=ipm.id))
    if integrated_challenge and crop_livestock:
        challenge_practices.append(ChallengePractice(challenge_id=integrated_challenge.id, practice_id=crop_livestock.id))
    if integrated_challenge and precision_ag:
        challenge_practices.append(ChallengePractice(challenge_id=integrated_challenge.id, practice_id=precision_ag.id))
    if integrated_challenge and permaculture:
        challenge_practices.append(ChallengePractice(challenge_id=integrated_challenge.id, practice_id=permaculture.id))
    
    # Add all challenge-practice links
    for cp in challenge_practices:
        db.session.add(cp)
    
    db.session.commit()
    logger.info(f"Added {len(challenge_practices)} challenge-practice relationships")

def seed_sustainability_quests():
    """Seed the database with sustainability quests and their steps"""
    
    # Check if data already exists
    if SustainabilityQuest.query.count() > 0:
        logger.info("Sustainability quests data already exists")
        return

    logger.info("Seeding sustainability quests...")
    
    # Define quests
    now = datetime.utcnow()
    quests = [
        {
            'title': 'Introduction to Composting',
            'description': 'Learn how to create and maintain a successful composting system for your farm. This quest will guide you through the process of setting up a composting area, selecting materials, managing the compost pile, and applying finished compost to your crops.',
            'category': 'beginner',
            'time_limit_days': 14,
            'points_awarded': 300,
            'start_date': now,
            'end_date': now + timedelta(days=365),
            'image_url': '/static/images/quests/composting.jpg',
            'active': True,
            'steps': [
                {
                    'step_number': 1,
                    'title': 'Planning Your Compost System',
                    'description': 'Learn about different composting methods and choose one appropriate for your farm scale and resources.',
                    'instructions': '''
                        <h5>Types of Composting Systems</h5>
                        <ul>
                            <li><strong>Pile Method:</strong> Simple heap composting, requires manual turning</li>
                            <li><strong>Bin System:</strong> Uses containers to contain compost material</li>
                            <li><strong>Three-Bin System:</strong> Allows for different stages of composting</li>
                            <li><strong>Vermicomposting:</strong> Uses worms to break down organic matter</li>
                        </ul>
                        
                        <h5>Site Selection Considerations</h5>
                        <ol>
                            <li>Choose a level area with good drainage</li>
                            <li>Ensure partial shade to prevent excessive drying</li>
                            <li>Consider proximity to water source and material storage</li>
                            <li>Allow for equipment access if using machinery</li>
                        </ol>
                        
                        <p>Based on your farm size and resources, decide on a composting method and location. Document your decision and reasons.</p>
                    ''',
                    'resources': '''
                        <ul>
                            <li><a href="#">Composting Methods Comparison Guide</a></li>
                            <li><a href="#">Site Planning Worksheet</a></li>
                            <li><a href="#">Video: Compost System Design Basics</a></li>
                        </ul>
                    '''
                },
                {
                    'step_number': 2,
                    'title': 'Gathering Materials and Setting Up',
                    'description': 'Collect the necessary materials and build your compost system according to your plan.',
                    'instructions': '''
                        <h5>Materials Needed:</h5>
                        <ol>
                            <li>Building materials for your chosen system (lumber, wire mesh, pallets, etc.)</li>
                            <li>Tools for construction</li>
                            <li>Carbon-rich "browns" (dry leaves, straw, wood chips)</li>
                            <li>Nitrogen-rich "greens" (fresh plant material, food scraps, manure)</li>
                            <li>Water source</li>
                            <li>Thermometer (optional but recommended)</li>
                        </ol>
                        
                        <h5>Setting Up:</h5>
                        <ol>
                            <li>Clear and level the site</li>
                            <li>Construct your composting system</li>
                            <li>Ensure good drainage</li>
                            <li>Create signage to identify different materials or stages</li>
                        </ol>
                        
                        <p>Take photos of your materials and the completed setup.</p>
                    '''
                },
                {
                    'step_number': 3,
                    'title': 'Starting and Maintaining Your Compost',
                    'description': 'Learn how to build a proper compost pile with the right mix of materials and maintain it for optimal decomposition.',
                    'instructions': '''
                        <h5>Building the Pile:</h5>
                        <ol>
                            <li>Start with a 4-6 inch layer of coarse material (twigs, chopped corn stalks) for drainage</li>
                            <li>Add alternating layers of "browns" and "greens" (3:1 ratio by volume)</li>
                            <li>Moisten each layer as you build</li>
                            <li>Aim for a minimum pile size of 3ft x 3ft x 3ft</li>
                        </ol>
                        
                        <h5>Maintenance:</h5>
                        <ul>
                            <li>Monitor moisture (should feel like a wrung-out sponge)</li>
                            <li>Turn the pile every 1-2 weeks</li>
                            <li>Check internal temperature (135-150°F indicates active composting)</li>
                            <li>Add more browns if too wet or smelly</li>
                            <li>Add more greens and water if too dry or not heating up</li>
                        </ul>
                        
                        <p>Keep a log of your pile's temperature, moisture level, and turning schedule for at least one week.</p>
                    '''
                },
                {
                    'step_number': 4,
                    'title': 'Harvesting and Using Compost',
                    'description': 'Learn how to determine when compost is ready, how to harvest it, and the best ways to apply it to your crops.',
                    'instructions': '''
                        <h5>Signs of Finished Compost:</h5>
                        <ul>
                            <li>Dark brown or black color</li>
                            <li>Earthy smell</li>
                            <li>Original materials no longer recognizable</li>
                            <li>Temperature has cooled to ambient</li>
                            <li>Volume reduced by about 50%</li>
                        </ul>
                        
                        <h5>Harvesting Methods:</h5>
                        <ol>
                            <li>Screen finished compost to remove large pieces</li>
                            <li>Return unfinished materials to a new pile</li>
                            <li>Store finished compost in a covered area</li>
                        </ol>
                        
                        <h5>Application Rates:</h5>
                        <ul>
                            <li>Field crops: 2-5 tons per acre</li>
                            <li>Vegetable gardens: 1-3 inch layer worked into soil</li>
                            <li>Tree/shrub planting: Mix 1:3 with soil in planting hole</li>
                            <li>Potting mix: Blend 1:3 with soil</li>
                        </ul>
                        
                        <p>Apply compost to a test area and document the application method and rate used.</p>
                    '''
                }
            ]
        },
        {
            'title': 'Water Harvesting Basics',
            'description': 'Learn how to capture, store, and use rainwater efficiently on your farm. This quest will teach you how to implement simple rainwater harvesting techniques that can improve water security and reduce your dependence on other water sources.',
            'category': 'beginner',
            'time_limit_days': 21,
            'points_awarded': 350,
            'start_date': now,
            'end_date': now + timedelta(days=365),
            'image_url': '/static/images/quests/water_harvesting.jpg',
            'active': True,
            'steps': [
                {
                    'step_number': 1,
                    'title': 'Assessing Your Rainfall and Water Needs',
                    'description': 'Evaluate your local rainfall patterns and calculate your farm\'s water requirements.',
                    'instructions': '''
                        <h5>Rainfall Assessment:</h5>
                        <ol>
                            <li>Gather historical rainfall data for your area</li>
                            <li>Note seasonal variations and rainfall distribution</li>
                            <li>Calculate potential harvesting volume using the formula: Collection area (m²) × Rainfall (mm) × 0.8 = Water collected (liters)</li>
                        </ol>
                        
                        <h5>Water Needs Calculation:</h5>
                        <ol>
                            <li>List all water uses on your farm (irrigation, livestock, washing, etc.)</li>
                            <li>Estimate daily water requirements for each use</li>
                            <li>Calculate total monthly and seasonal water needs</li>
                            <li>Identify critical periods when rainfall doesn't meet needs</li>
                        </ol>
                        
                        <p>Create a simple chart showing monthly rainfall vs. water needs for your farm.</p>
                    '''
                },
                {
                    'step_number': 2,
                    'title': 'Designing a Basic Rainwater Collection System',
                    'description': 'Plan a rainwater harvesting system based on your needs assessment.',
                    'instructions': '''
                        <h5>System Components:</h5>
                        <ul>
                            <li><strong>Catchment surface:</strong> Roof, plastic sheet, or prepared ground area</li>
                            <li><strong>Conveyance system:</strong> Gutters, pipes, channels</li>
                            <li><strong>First flush diverter:</strong> Diverts initial dirty runoff</li>
                            <li><strong>Filtration:</strong> Screens, filters</li>
                            <li><strong>Storage:</strong> Tanks, ponds, cisterns</li>
                            <li><strong>Distribution:</strong> Pipes, pumps, irrigation systems</li>
                        </ul>
                        
                        <h5>Design Considerations:</h5>
                        <ol>
                            <li>Match storage capacity to rainfall patterns and water needs</li>
                            <li>Consider available space and topography</li>
                            <li>Plan for overflow management</li>
                            <li>Ensure system accessibility for maintenance</li>
                            <li>Account for water quality requirements</li>
                        </ol>
                        
                        <p>Create a simple diagram of your planned system showing all major components.</p>
                    '''
                },
                {
                    'step_number': 3,
                    'title': 'Constructing a Small-Scale Collection System',
                    'description': 'Build a simple rainwater harvesting system based on your design.',
                    'instructions': '''
                        <h5>Basic Construction Steps:</h5>
                        <ol>
                            <li>Prepare the catchment area (clean roof, install sheet, etc.)</li>
                            <li>Install or repair gutters/channels ensuring proper slope</li>
                            <li>Set up first flush diverter using simple pipe arrangement</li>
                            <li>Install mesh screens at downspouts to prevent debris entry</li>
                            <li>Position and secure storage container(s)</li>
                            <li>Connect all components ensuring watertight seals</li>
                            <li>Create overflow pathway to appropriate drainage area</li>
                            <li>Cover storage to prevent algae growth and mosquito breeding</li>
                        </ol>
                        
                        <h5>Materials Needed:</h5>
                        <ul>
                            <li>Storage container (tank, barrel, etc.)</li>
                            <li>Gutters and/or pipes</li>
                            <li>Wire mesh/screen</li>
                            <li>Connectors and fittings</li>
                            <li>Sealant</li>
                            <li>Basic tools</li>
                        </ul>
                        
                        <p>Build a simple water harvesting system and document with photos of each component.</p>
                    '''
                },
                {
                    'step_number': 4,
                    'title': 'System Maintenance and Efficient Water Use',
                    'description': 'Learn how to maintain your rainwater harvesting system and use the collected water efficiently.',
                    'instructions': '''
                        <h5>Regular Maintenance Tasks:</h5>
                        <ol>
                            <li>Clean gutters and catchment surfaces seasonally</li>
                            <li>Inspect and clean filters/screens monthly and after heavy storms</li>
                            <li>Empty and clean first flush diverter after each rainfall</li>
                            <li>Check for leaks, cracks, or damage regularly</li>
                            <li>Clean storage tanks annually</li>
                            <li>Monitor water quality periodically</li>
                        </ol>
                        
                        <h5>Efficient Water Use Strategies:</h5>
                        <ul>
                            <li>Install drip irrigation where appropriate</li>
                            <li>Apply water directly to plant roots</li>
                            <li>Add mulch to reduce evaporation</li>
                            <li>Time irrigation for early morning or evening</li>
                            <li>Prioritize water use during critical growth stages</li>
                            <li>Group plants with similar water needs</li>
                        </ul>
                        
                        <p>Create a maintenance schedule and implement at least one efficient water use technique.</p>
                    '''
                }
            ]
        },
        {
            'title': 'Creating Wildlife Habitats',
            'description': 'Learn how to enhance biodiversity on your farm by creating habitats for beneficial wildlife. This quest will guide you through designing and implementing features that attract pollinators, beneficial insects, birds, and other wildlife that contribute to a healthy farm ecosystem.',
            'category': 'intermediate',
            'time_limit_days': 30,
            'points_awarded': 450,
            'start_date': now,
            'end_date': now + timedelta(days=365),
            'image_url': '/static/images/quests/wildlife_habitats.jpg',
            'active': True,
            'steps': [
                {
                    'step_number': 1,
                    'title': 'Assessing Current Biodiversity',
                    'description': 'Evaluate the existing wildlife and habitat features on your farm.',
                    'instructions': '''
                        <h5>Conducting a Biodiversity Assessment:</h5>
                        <ol>
                            <li>Survey your land during different times of day</li>
                            <li>Record wildlife sightings (insects, birds, mammals, etc.)</li>
                            <li>Note existing habitat features (hedgerows, trees, water sources, etc.)</li>
                            <li>Identify areas lacking diversity or habitat</li>
                            <li>Map your observations on a simple farm sketch</li>
                        </ol>
                        
                        <h5>Key Questions to Answer:</h5>
                        <ul>
                            <li>What beneficial species are already present?</li>
                            <li>What problematic pests are affecting your crops?</li>
                            <li>What natural predators could help control these pests?</li>
                            <li>What pollinators visit your crops?</li>
                            <li>What habitat elements are missing?</li>
                        </ul>
                        
                        <p>Complete a biodiversity assessment form documenting your findings.</p>
                    '''
                },
                {
                    'step_number': 2,
                    'title': 'Designing Habitat Features',
                    'description': 'Plan specific wildlife habitat enhancements based on your assessment.',
                    'instructions': '''
                        <h5>Habitat Feature Options:</h5>
                        <ul>
                            <li><strong>Pollinator garden:</strong> Diverse flowering plants that bloom throughout the growing season</li>
                            <li><strong>Insect hotel:</strong> Structure with various materials offering nesting sites for beneficial insects</li>
                            <li><strong>Bird houses/perches:</strong> Nesting boxes and hunting perches for insect-eating birds</li>
                            <li><strong>Bat houses:</strong> Shelters for bats that control night-flying insects</li>
                            <li><strong>Hedgerows:</strong> Mixed native shrubs providing shelter, food, and travel corridors</li>
                            <li><strong>Beetle banks:</strong> Raised strips of perennial grasses for ground beetles and other beneficial insects</li>
                            <li><strong>Water features:</strong> Small ponds, basins, or puddles for wildlife hydration</li>
                        </ul>
                        
                        <h5>Design Considerations:</h5>
                        <ol>
                            <li>Select features targeting specific beneficial species</li>
                            <li>Choose appropriate locations considering sun, wind, and accessibility</li>
                            <li>Plan for year-round habitat needs (food, water, shelter, nesting sites)</li>
                            <li>Ensure features won't interfere with farm operations</li>
                            <li>Consider maintenance requirements</li>
                        </ol>
                        
                        <p>Create a habitat enhancement plan with at least three specific features, their locations, and target species.</p>
                    '''
                },
                {
                    'step_number': 3,
                    'title': 'Implementing Habitat Features',
                    'description': 'Build and install at least two habitat features from your plan.',
                    'instructions': '''
                        <h5>Feature Implementation Guidelines:</h5>
                        
                        <p><strong>Pollinator Garden:</strong></p>
                        <ol>
                            <li>Select a sunny location near crops needing pollination</li>
                            <li>Choose at least 5-7 different native flowering plants with diverse bloom times</li>
                            <li>Prepare soil and plant in groups for better visibility to pollinators</li>
                            <li>Add mulch to suppress weeds and retain moisture</li>
                            <li>Install signage identifying the garden and its purpose</li>
                        </ol>
                        
                        <p><strong>Insect Hotel:</strong></p>
                        <ol>
                            <li>Create a frame using untreated wood (recommended size: 2ft x 2ft)</li>
                            <li>Fill sections with various materials:
                                <ul>
                                    <li>Drilled hardwood blocks (3-10mm holes) for solitary bees</li>
                                    <li>Hollow stems/bamboo tubes for solitary wasps</li>
                                    <li>Pinecones and straw for lacewings and ladybugs</li>
                                    <li>Loose bark for beetles and spiders</li>
                                </ul>
                            </li>
                            <li>Install in a sunny, sheltered location at least 3ft off the ground</li>
                            <li>Add a slight roof overhang to protect from heavy rain</li>
                        </ol>
                        
                        <p><strong>Bird/Bat Houses:</strong></p>
                        <ol>
                            <li>Build or purchase appropriate houses for target species</li>
                            <li>Mount houses on poles or trees at recommended heights (10-15ft for most birds)</li>
                            <li>Face openings away from prevailing winds</li>
                            <li>Ensure protection from predators</li>
                        </ol>
                        
                        <p>Implement at least two habitat features and document with photos showing construction and installation.</p>
                    '''
                },
                {
                    'step_number': 4,
                    'title': 'Monitoring and Maintenance',
                    'description': 'Learn how to monitor wildlife response to your habitat enhancements and maintain these features over time.',
                    'instructions': '''
                        <h5>Monitoring Techniques:</h5>
                        <ol>
                            <li>Establish a regular monitoring schedule (weekly or biweekly)</li>
                            <li>Record wildlife sightings with dates, times, and weather conditions</li>
                            <li>Take photographs to document species presence</li>
                            <li>Note any plant growth, flowering, or habitat feature use</li>
                            <li>Track changes in pest populations on nearby crops</li>
                        </ol>
                        
                        <h5>Maintenance Tasks:</h5>
                        <ul>
                            <li><strong>Pollinator Gardens:</strong> Weed regularly, replace plants as needed, avoid pesticides</li>
                            <li><strong>Insect Hotels:</strong> Clean out old/unused sections annually, replace degraded materials</li>
                            <li><strong>Bird/Bat Houses:</strong> Clean out after nesting season, check for damage or pests</li>
                            <li><strong>Hedgerows:</strong> Prune selectively to maintain structure, remove invasive species</li>
                            <li><strong>Water Features:</strong> Ensure year-round availability, prevent mosquito breeding</li>
                        </ul>
                        
                        <p>Create a monitoring log with at least two weeks of observations and develop a seasonal maintenance schedule.</p>
                    '''
                }
            ]
        }
    ]
    
    # Add quests and their steps to the database
    for quest_data in quests:
        # Extract steps data before creating quest
        steps_data = quest_data.pop('steps', [])
        
        # Create and add quest
        quest = SustainabilityQuest(**quest_data)
        db.session.add(quest)
        db.session.flush()  # Generate ID without committing
        
        # Create and add steps for this quest
        for step_data in steps_data:
            step_data['quest_id'] = quest.id
            step = QuestStep(**step_data)
            db.session.add(step)
    
    db.session.commit()
    logger.info(f"Added {len(quests)} sustainability quests with their steps")

def run_all_seeding():
    """Run all seeding functions"""
    logger.info("Starting sustainability data seeding...")
    
    seed_sustainable_practices()
    seed_sustainability_challenges()
    seed_sustainability_quests()
    
    logger.info("Sustainability data seeding completed!")

if __name__ == "__main__":
    run_all_seeding()