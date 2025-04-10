import logging
from datetime import datetime
from app import app, db
from models import (
    LearningModule, LearningLesson, LearningQuiz, QuizQuestion, 
    QuestionChoice, Achievement
)

logger = logging.getLogger(__name__)

def seed_learning_modules():
    """
    Create initial learning modules, lessons, quizzes, and achievements 
    for the learning platform
    """
    logger.info("Seeding learning modules data...")
    
    # Check if data already exists
    existing_modules = LearningModule.query.count()
    if existing_modules > 0:
        logger.info(f"Found {existing_modules} existing modules, skipping seeding")
        return
    
    # Create achievements
    achievements = [
        Achievement(
            name="First Module Completed",
            description="Complete your first learning module",
            category="learning",
            points_awarded=50,
            criteria="Complete any learning module by finishing all lessons and passing all quizzes",
            is_hidden=False
        ),
        Achievement(
            name="Quiz Master",
            description="Pass 10 quizzes with a score of 90% or higher",
            category="learning",
            points_awarded=100,
            criteria="Pass at least 10 different quizzes with a score of at least 90% each",
            is_hidden=False
        ),
        Achievement(
            name="Knowledge Seeker",
            description="Complete 5 learning modules",
            category="learning",
            points_awarded=150,
            criteria="Complete a total of 5 different learning modules",
            is_hidden=False
        ),
        Achievement(
            name="Learning Explorer",
            description="Complete 25 lessons across any modules",
            category="learning",
            points_awarded=100,
            criteria="Complete a total of 25 lessons across any number of modules",
            is_hidden=False
        ),
        Achievement(
            name="Perfect Score",
            description="Pass a quiz with a perfect score on your first attempt",
            category="learning",
            points_awarded=75,
            criteria="Score 100% on a quiz on your first attempt",
            is_hidden=False
        ),
        Achievement(
            name="Reached Level 5",
            description="Reach level 5 on the platform",
            category="progress",
            points_awarded=100,
            criteria="Accumulate enough points to reach level 5",
            is_hidden=False
        ),
        Achievement(
            name="Reached Level 10",
            description="Reach level 10 on the platform",
            category="progress",
            points_awarded=200,
            criteria="Accumulate enough points to reach level 10",
            is_hidden=False
        ),
    ]
    
    for achievement in achievements:
        db.session.add(achievement)
    
    # Create learning modules
    
    # Module 1: Soil Health Fundamentals
    module1 = LearningModule(
        title="Soil Health Fundamentals",
        description="Learn about soil composition, fertility, and management techniques that maintain and improve soil health for sustainable farming.",
        category="soil_management",
        difficulty_level=1,
        points_available=200,
        estimated_duration=60,
        prerequisites="",
        active=True
    )
    db.session.add(module1)
    db.session.flush()  # To get the module ID
    
    # Lessons for Module 1
    lessons1 = [
        LearningLesson(
            module_id=module1.id,
            title="Understanding Soil Composition",
            content="""
<h2>Understanding Soil Composition</h2>

<p>Soil is much more than just dirt—it's a complex living ecosystem that forms the foundation of agriculture. In this lesson, we'll explore the basic components of soil and why they matter for farming.</p>

<h3>What Makes Up Soil?</h3>

<p>Soil consists of four main components:</p>

<ul>
    <li><strong>Minerals (45-49%)</strong> - Broken down rock particles that vary in size from clay (smallest) to silt to sand (largest)</li>
    <li><strong>Organic Matter (1-5%)</strong> - Decomposed plant and animal materials that provide nutrients</li>
    <li><strong>Water (25%)</strong> - Essential for plant growth and nutrient transport</li>
    <li><strong>Air (25%)</strong> - Provides oxygen for root respiration and soil microorganisms</li>
</ul>

<h3>Soil Texture</h3>

<p>Soil texture refers to the proportion of sand, silt, and clay particles. This greatly affects how soil behaves:</p>

<ul>
    <li><strong>Sandy soil</strong> - Drains quickly, warms up fast, but doesn't hold nutrients well</li>
    <li><strong>Clay soil</strong> - Holds water and nutrients well, but can become compacted and poorly drained</li>
    <li><strong>Silt soil</strong> - Fertile and holds moisture well, but can form a crust when dry</li>
    <li><strong>Loam</strong> - A balanced mixture that is ideal for most crops</li>
</ul>

<h3>Soil Structure</h3>

<p>Structure refers to how the soil particles clump together to form aggregates. Good soil structure:</p>

<ul>
    <li>Creates pore spaces for air and water movement</li>
    <li>Allows root penetration</li>
    <li>Reduces erosion</li>
    <li>Supports soil life</li>
</ul>

<h3>The Living Soil</h3>

<p>A handful of healthy soil contains billions of organisms:</p>

<ul>
    <li>Bacteria and fungi that decompose organic matter</li>
    <li>Protozoa and nematodes that help cycle nutrients</li>
    <li>Arthropods and earthworms that improve soil structure</li>
</ul>

<p>These organisms form a soil food web that breaks down organic matter, cycles nutrients, and contributes to plant health.</p>

<h3>Why Soil Composition Matters for Farmers</h3>

<p>Understanding your soil composition helps you:</p>

<ul>
    <li>Choose appropriate crops for your soil type</li>
    <li>Apply the right amount of water</li>
    <li>Add appropriate amendments to improve soil fertility</li>
    <li>Prevent soil degradation</li>
    <li>Increase farm productivity and sustainability</li>
</ul>

<p>In the next lesson, we'll learn how to assess soil health on your farm.</p>
            """,
            order_index=1,
            media_type="text",
            points_awarded=15
        ),
        LearningLesson(
            module_id=module1.id,
            title="Assessing Soil Health",
            content="""
<h2>Assessing Soil Health</h2>

<p>Before making improvements to your soil, it's important to understand its current condition. This lesson covers simple methods to assess soil health on your farm.</p>

<h3>Visual Assessment</h3>

<p>Start with simple observations:</p>

<ul>
    <li><strong>Color</strong> - Darker soils generally contain more organic matter</li>
    <li><strong>Structure</strong> - Crumbly soil with visible aggregates is healthier than powdery or clumpy soil</li>
    <li><strong>Plant vigor</strong> - Areas with stunted or discolored plants may indicate soil problems</li>
    <li><strong>Erosion</strong> - Visible erosion signals soil degradation</li>
    <li><strong>Soil life</strong> - The presence of earthworms and other visible organisms is a positive sign</li>
</ul>

<h3>Simple Field Tests</h3>

<h4>1. The Jar Test (For Soil Texture)</h4>

<ol>
    <li>Fill a clear jar 1/3 with soil</li>
    <li>Add water until the jar is almost full</li>
    <li>Add a teaspoon of dish soap (helps separate particles)</li>
    <li>Shake vigorously and let settle for 24 hours</li>
    <li>Sand will settle at the bottom, followed by silt, then clay on top</li>
    <li>Measure the layers to determine your soil's texture</li>
</ol>

<h4>2. Infiltration Test (For Drainage)</h4>

<ol>
    <li>Remove a section of soil surface vegetation</li>
    <li>Push a hollow cylinder (like a can with both ends removed) into the soil</li>
    <li>Pour a measured amount of water into the cylinder</li>
    <li>Time how long it takes to drain</li>
    <li>Repeat in multiple locations</li>
</ol>

<p>Good soil should drain 1-2 inches per hour. Very fast or very slow drainage indicates potential problems.</p>

<h4>3. Soil Compaction Assessment</h4>

<ol>
    <li>Push a wire flag vertically into the soil</li>
    <li>Note where resistance increases</li>
    <li>If resistance occurs in the top 6-8 inches, compaction may be limiting root growth</li>
</ol>

<h3>Chemical Testing</h3>

<p>While simple tests can provide insights, laboratory soil testing gives the most accurate results for:</p>

<ul>
    <li>pH level (acidity/alkalinity)</li>
    <li>Nutrient levels (N, P, K, micronutrients)</li>
    <li>Organic matter content</li>
    <li>Cation exchange capacity (CEC)</li>
</ul>

<h4>Collecting Soil Samples:</h4>

<ol>
    <li>Take samples from multiple locations across your field</li>
    <li>Sample to the depth of the plant roots (usually 15-20 cm)</li>
    <li>Remove surface debris before sampling</li>
    <li>Mix samples from the same field to create a composite sample</li>
    <li>Send to a local agricultural testing laboratory</li>
</ol>

<h3>Biological Indicators</h3>

<p>Biological activity indicates healthy soil:</p>

<ul>
    <li><strong>Earthworm count</strong> - Dig a 30cm cube of soil and count the worms (10+ is excellent)</li>
    <li><strong>Residue decomposition</strong> - How quickly crop residues break down</li>
    <li><strong>Root development</strong> - Extensive, deep root systems indicate good soil health</li>
</ul>

<h3>Interpreting Your Results</h3>

<p>Use your assessment results to identify specific soil health issues:</p>

<ul>
    <li>Poor drainage may require improved structure or drainage systems</li>
    <li>Low organic matter suggests a need for cover crops or compost</li>
    <li>Compaction indicates a need for reduced tillage or targeted subsoiling</li>
    <li>Nutrient deficiencies or pH imbalances can be addressed with specific amendments</li>
</ul>

<p>Regular soil assessment helps you track improvements over time and make informed management decisions. In the next lesson, we'll explore strategies for improving soil fertility.</p>
            """,
            order_index=2,
            media_type="text",
            points_awarded=15
        ),
        LearningLesson(
            module_id=module1.id,
            title="Improving Soil Fertility",
            content="""
<h2>Improving Soil Fertility</h2>

<p>Maintaining and enhancing soil fertility is key to sustainable farming. This lesson explores practical approaches to improve your soil's ability to support healthy crop growth.</p>

<h3>Understanding Soil Fertility</h3>

<p>Soil fertility refers to the soil's ability to provide essential nutrients and a conducive environment for plant growth. It depends on:</p>

<ul>
    <li>Nutrient content and availability</li>
    <li>Soil structure and tilth</li>
    <li>Organic matter levels</li>
    <li>Soil biology</li>
    <li>pH balance</li>
    <li>Absence of harmful substances</li>
</ul>

<h3>Building Organic Matter</h3>

<p>Organic matter is the foundation of soil fertility. It:</p>

<ul>
    <li>Provides nutrients as it decomposes</li>
    <li>Improves soil structure</li>
    <li>Increases water-holding capacity</li>
    <li>Supports beneficial soil organisms</li>
    <li>Buffers against pH changes</li>
</ul>

<h4>Strategies to Increase Organic Matter:</h4>

<ol>
    <li><strong>Crop Residue Management</strong> - Leave crop residues in the field rather than burning or removing them</li>
    <li><strong>Compost Application</strong> - Add well-decomposed compost to provide stable organic matter</li>
    <li><strong>Cover Crops</strong> - Plant cover crops during off-seasons to add biomass and prevent erosion</li>
    <li><strong>Manure Application</strong> - Apply animal manure to add nutrients and organic material</li>
    <li><strong>Reduced Tillage</strong> - Minimize soil disturbance to slow organic matter decomposition</li>
</ol>

<h3>Balanced Nutrient Management</h3>

<p>Plants need 17 essential nutrients for growth. The most important macronutrients are:</p>

<ul>
    <li><strong>Nitrogen (N)</strong> - Critical for leaf and stem growth</li>
    <li><strong>Phosphorus (P)</strong> - Essential for root development and energy transfer</li>
    <li><strong>Potassium (K)</strong> - Important for overall plant health and stress resistance</li>
</ul>

<h4>Principles of Balanced Nutrient Management:</h4>

<ol>
    <li><strong>Test First</strong> - Base fertilization on soil test results</li>
    <li><strong>Right Source</strong> - Choose appropriate nutrient sources for your soil and crops</li>
    <li><strong>Right Rate</strong> - Apply only what crops can use</li>
    <li><strong>Right Time</strong> - Apply nutrients when crops need them</li>
    <li><strong>Right Place</strong> - Place nutrients where crops can access them</li>
</ol>

<h3>Managing Soil pH</h3>

<p>Soil pH affects nutrient availability and biological activity:</p>

<ul>
    <li>Most crops prefer a pH between 6.0-7.0</li>
    <li>Acidic soils (pH &lt; 6.0) can be amended with lime</li>
    <li>Alkaline soils (pH &gt; 7.5) can be amended with sulfur or gypsum</li>
    <li>pH adjustments should be made gradually</li>
</ul>

<h3>Biological Approaches to Soil Fertility</h3>

<p>Enhancing soil biology helps create self-sustaining fertility:</p>

<ul>
    <li><strong>Crop Rotation</strong> - Diverse crop sequences support diverse soil organisms</li>
    <li><strong>Legume Crops</strong> - Plants like beans and clover fix atmospheric nitrogen</li>
    <li><strong>Minimal Soil Disturbance</strong> - Preserves fungal networks and soil habitat</li>
    <li><strong>Inoculants</strong> - Microbial inoculants can enhance specific biological functions</li>
</ul>

<h3>Integrated Soil Fertility Management</h3>

<p>The most effective approach combines multiple strategies:</p>

<ol>
    <li>Start with soil assessment to identify limitations</li>
    <li>Address structural issues through appropriate tillage or no-till methods</li>
    <li>Build organic matter through residue management and organic inputs</li>
    <li>Use targeted mineral fertilizers to address specific deficiencies</li>
    <li>Implement supportive practices like crop rotation and cover cropping</li>
    <li>Monitor progress with regular soil testing and observation</li>
</ol>

<h3>Implementation at Different Scales</h3>

<p>Soil fertility approaches can be adapted for any farm size:</p>

<ul>
    <li><strong>Small Farms</strong> - Focus on compost, manure, and intensive crop rotation</li>
    <li><strong>Medium Farms</strong> - Combine organic inputs with targeted mineral fertilizers</li>
    <li><strong>Large Farms</strong> - Implement precision agriculture for efficient nutrient application</li>
</ul>

<p>Remember that building soil fertility is a long-term investment that pays dividends in crop quality, yield stability, and reduced input costs over time.</p>
            """,
            order_index=3,
            media_type="text",
            points_awarded=15
        )
    ]
    
    for lesson in lessons1:
        db.session.add(lesson)
    
    # Quiz for Module 1
    quiz1 = LearningQuiz(
        module_id=module1.id,
        title="Soil Health Assessment",
        description="Test your knowledge of soil health principles and assessment techniques.",
        order_index=4,
        passing_score=70,
        points_awarded=30,
        time_limit=15  # 15 minutes
    )
    db.session.add(quiz1)
    db.session.flush()  # To get the quiz ID
    
    # Questions for Quiz 1
    questions1 = [
        {
            "question": QuizQuestion(
                quiz_id=quiz1.id,
                question_text="Which of the following is NOT one of the four main components of soil?",
                question_type="multiple_choice",
                order_index=1,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Minerals", is_correct=False),
                QuestionChoice(choice_text="Organic matter", is_correct=False),
                QuestionChoice(choice_text="Fertilizer", is_correct=True, explanation="The four main components of soil are minerals, organic matter, water, and air. Fertilizer is an addition to soil, not a natural component."),
                QuestionChoice(choice_text="Air", is_correct=False)
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz1.id,
                question_text="Which soil texture typically has the best natural drainage?",
                question_type="multiple_choice",
                order_index=2,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Clay", is_correct=False),
                QuestionChoice(choice_text="Sand", is_correct=True, explanation="Sandy soils have large particles with large pore spaces between them, allowing water to drain quickly."),
                QuestionChoice(choice_text="Silt", is_correct=False),
                QuestionChoice(choice_text="Compacted loam", is_correct=False)
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz1.id,
                question_text="What does a darker soil color typically indicate?",
                question_type="multiple_choice",
                order_index=3,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Higher clay content", is_correct=False),
                QuestionChoice(choice_text="Better drainage", is_correct=False),
                QuestionChoice(choice_text="Higher organic matter content", is_correct=True, explanation="Darker soil typically indicates higher organic matter content, which is beneficial for soil health."),
                QuestionChoice(choice_text="Lower pH level", is_correct=False)
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz1.id,
                question_text="Which of the following is the most appropriate pH range for most crops?",
                question_type="multiple_choice",
                order_index=4,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="4.0 - 5.0", is_correct=False),
                QuestionChoice(choice_text="6.0 - 7.0", is_correct=True, explanation="Most crops grow best in slightly acidic to neutral soil with a pH between 6.0 and 7.0."),
                QuestionChoice(choice_text="8.0 - 9.0", is_correct=False),
                QuestionChoice(choice_text="9.0 - 10.0", is_correct=False)
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz1.id,
                question_text="What is the primary benefit of increasing soil organic matter?",
                question_type="multiple_choice",
                order_index=5,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="It eliminates the need for all fertilizers", is_correct=False),
                QuestionChoice(choice_text="It improves soil structure, water retention, and nutrient cycling", is_correct=True, explanation="Organic matter improves multiple aspects of soil health, including structure, water retention, and nutrient cycling."),
                QuestionChoice(choice_text="It kills all soil-borne pests and diseases", is_correct=False),
                QuestionChoice(choice_text="It makes soil more acidic", is_correct=False)
            ]
        }
    ]
    
    for q_data in questions1:
        db.session.add(q_data["question"])
        db.session.flush()  # To get the question ID
        
        for choice in q_data["choices"]:
            choice.question_id = q_data["question"].id
            db.session.add(choice)
    
    # Module 2: Water Conservation Techniques
    module2 = LearningModule(
        title="Water Conservation Techniques",
        description="Discover strategies to efficiently use water resources, minimize waste, and maintain crop productivity during drought conditions.",
        category="water_management",
        difficulty_level=2,
        points_available=200,
        estimated_duration=90,
        prerequisites=f"{module1.id}",  # Requires Soil Health Fundamentals
        active=True
    )
    db.session.add(module2)
    db.session.flush()  # To get the module ID
    
    # Lessons for Module 2
    lessons2 = [
        LearningLesson(
            module_id=module2.id,
            title="Understanding Water Needs",
            content="""
<h2>Understanding Water Needs</h2>

<p>Water is a precious resource in agriculture, especially in regions facing climate change challenges. This lesson focuses on understanding crop water requirements and the factors that influence them.</p>

<h3>The Importance of Water in Agriculture</h3>

<p>Water plays several crucial roles in plant growth:</p>

<ul>
    <li>Transports nutrients from soil to plant tissues</li>
    <li>Enables photosynthesis and other metabolic processes</li>
    <li>Maintains cell structure through turgor pressure</li>
    <li>Regulates plant temperature through transpiration</li>
    <li>Supports soil microorganisms that benefit plants</li>
</ul>

<p>Understanding these functions helps develop effective water management strategies.</p>

<h3>Crop Water Requirements</h3>

<p>Different crops have varying water needs based on:</p>

<h4>1. Plant Factors</h4>
<ul>
    <li><strong>Crop type</strong> - Deep-rooted crops like maize can access water from deeper soil layers than shallow-rooted crops like lettuce</li>
    <li><strong>Growth stage</strong> - Most crops have critical periods (like flowering) when water stress causes the greatest yield loss</li>
    <li><strong>Leaf area</strong> - Plants with larger leaf surfaces generally transpire more water</li>
</ul>

<h4>2. Environmental Factors</h4>
<ul>
    <li><strong>Temperature</strong> - Higher temperatures increase evapotranspiration rates</li>
    <li><strong>Wind</strong> - Increases water loss through transpiration</li>
    <li><strong>Humidity</strong> - Lower humidity increases the rate of water loss from plants</li>
    <li><strong>Solar radiation</strong> - More sunshine typically increases water use</li>
</ul>

<h4>3. Soil Factors</h4>
<ul>
    <li><strong>Soil texture</strong> - Affects water infiltration, drainage, and storage capacity</li>
    <li><strong>Soil structure</strong> - Influences how water moves through the soil profile</li>
    <li><strong>Organic matter</strong> - Increases water-holding capacity</li>
    <li><strong>Soil depth</strong> - Deeper soils can store more water</li>
</ul>

<h3>Measuring Crop Water Requirements</h3>

<p>Several methods can help determine how much water your crops need:</p>

<h4>1. Evapotranspiration (ET) Based Calculations</h4>
<p>ET combines water lost through soil evaporation and plant transpiration. Reference ET (ET₀) can be calculated using weather data, then adjusted with a crop coefficient (Kc) to determine crop-specific ET:</p>

<p>Crop Water Need = ET₀ × Kc</p>

<h4>2. Soil Moisture Monitoring</h4>
<ul>
    <li><strong>Feel method</strong> - Assessing soil moisture by hand (simple but requires experience)</li>
    <li><strong>Tensiometers</strong> - Measure soil water tension</li>
    <li><strong>Electrical conductivity sensors</strong> - Measure soil moisture by electrical resistance</li>
    <li><strong>Neutron probes</strong> - Provide accurate measurements throughout the soil profile</li>
</ul>

<h4>3. Plant-Based Monitoring</h4>
<ul>
    <li><strong>Visual symptoms</strong> - Leaf rolling, wilting, color changes</li>
    <li><strong>Infrared thermometry</strong> - Measures crop canopy temperature (water-stressed plants are warmer)</li>
    <li><strong>Pressure chamber</strong> - Measures leaf water potential</li>
</ul>

<h3>Water Budgeting</h3>

<p>Creating a water budget helps manage irrigation efficiently:</p>

<ol>
    <li>Determine available water supply for the season</li>
    <li>Estimate crop water requirements for each growth stage</li>
    <li>Account for effective rainfall (not all rain is usable by crops)</li>
    <li>Calculate irrigation needs: Irrigation = Crop water need - Effective rainfall</li>
    <li>Adjust for irrigation system efficiency (e.g., drip systems are more efficient than flood irrigation)</li>
</ol>

<h3>Critical Growth Stages</h3>

<p>If water is limited, prioritize irrigation during these critical periods:</p>

<ul>
    <li><strong>Maize/Corn</strong> - Tasseling and silk formation</li>
    <li><strong>Rice</strong> - Panicle initiation and flowering</li>
    <li><strong>Wheat</strong> - Booting, heading, and grain filling</li>
    <li><strong>Cotton</strong> - Flowering and boll development</li>
    <li><strong>Vegetables</strong> - Transplanting, flowering, and fruit development</li>
</ul>

<h3>Signs of Water Stress</h3>

<p>Monitor crops for indications of insufficient water:</p>

<ul>
    <li>Wilting during hot parts of the day</li>
    <li>Leaf rolling or folding</li>
    <li>Yellowing or premature leaf drop</li>
    <li>Delayed growth or development</li>
    <li>Smaller than normal fruit or grain</li>
</ul>

<p>Understanding water needs is the first step toward efficient water management. In the next lesson, we'll explore specific water conservation techniques that can be applied on farms of all sizes.</p>
            """,
            order_index=1,
            media_type="text",
            points_awarded=15
        ),
        LearningLesson(
            module_id=module2.id,
            title="Efficient Irrigation Systems",
            content="""
<h2>Efficient Irrigation Systems</h2>

<p>Selecting and operating the right irrigation system is crucial for water conservation. This lesson explores different irrigation methods and how to maximize their efficiency.</p>

<h3>Types of Irrigation Systems</h3>

<h4>1. Surface Irrigation</h4>
<p>Water is distributed across the land by gravity.</p>

<ul>
    <li><strong>Flood irrigation</strong> - Entire field is flooded
        <ul>
            <li>Advantages: Low initial cost, simple technology</li>
            <li>Disadvantages: Low efficiency (40-60%), requires level land</li>
            <li>Improvement strategies: Land leveling, surge flow, alternate furrow irrigation</li>
        </ul>
    </li>
    <li><strong>Furrow irrigation</strong> - Water flows through small channels between crop rows
        <ul>
            <li>Advantages: Lower water use than flood irrigation, suitable for row crops</li>
            <li>Disadvantages: Labor intensive, still relatively inefficient</li>
            <li>Improvement strategies: Proper furrow design, optimal flow rates, cutback technique</li>
        </ul>
    </li>
    <li><strong>Basin irrigation</strong> - Level plots surrounded by bunds
        <ul>
            <li>Advantages: Good for rice and tree crops, simple construction</li>
            <li>Disadvantages: High water use, waterlogging risk</li>
            <li>Improvement strategies: Precise leveling, controlled inlet flow</li>
        </ul>
    </li>
</ul>

<h4>2. Sprinkler Irrigation</h4>
<p>Water is sprayed through the air in droplets.</p>

<ul>
    <li><strong>Center pivot</strong> - Large rotating sprinkler system
        <ul>
            <li>Advantages: Moderate efficiency (75-85%), covers large areas</li>
            <li>Disadvantages: High initial cost, wind drift, not suitable for all crops</li>
            <li>Improvement strategies: Drop nozzles, pressure regulation, variable rate application</li>
        </ul>
    </li>
    <li><strong>Hand-move/portable sprinklers</strong> - Aluminum pipes with sprinklers
        <ul>
            <li>Advantages: Lower cost, adaptable to field shape</li>
            <li>Disadvantages: Labor intensive, less uniform coverage</li>
            <li>Improvement strategies: Proper spacing, operating during low-wind periods</li>
        </ul>
    </li>
    <li><strong>Micro-sprinklers</strong> - Small sprinklers operating at low pressure
        <ul>
            <li>Advantages: Higher efficiency (85%), suitable for orchards</li>
            <li>Disadvantages: Clogging risk, more maintenance</li>
            <li>Improvement strategies: Proper filtration, regular cleaning</li>
        </ul>
    </li>
</ul>

<h4>3. Drip/Micro Irrigation</h4>
<p>Water is applied directly to the soil surface or root zone.</p>

<ul>
    <li><strong>Surface drip</strong> - Emitters placed on soil surface
        <ul>
            <li>Advantages: High efficiency (90-95%), precise application, reduced disease</li>
            <li>Disadvantages: Higher initial cost, clogging risk, requires technical knowledge</li>
            <li>Improvement strategies: Good filtration, regular flushing, chemical treatment</li>
        </ul>
    </li>
    <li><strong>Subsurface drip</strong> - Drip lines buried below soil surface
        <ul>
            <li>Advantages: Highest efficiency, reduced evaporation, longer system life</li>
            <li>Disadvantages: Difficult to monitor, higher installation cost</li>
            <li>Improvement strategies: Proper depth placement, emitter selection for root intrusion prevention</li>
        </ul>
    </li>
</ul>

<h3>Irrigation System Selection Factors</h3>

<p>Consider these when choosing an irrigation system:</p>

<ul>
    <li><strong>Water availability</strong> - Limited water favors higher efficiency systems</li>
    <li><strong>Crop type</strong> - Row crops, orchards, and field crops have different needs</li>
    <li><strong>Soil characteristics</strong> - Infiltration rate and water-holding capacity</li>
    <li><strong>Field size and shape</strong> - Affects system suitability</li>
    <li><strong>Slope and topography</strong> - Steep or irregular lands limit certain systems</li>
    <li><strong>Energy availability</strong> - Pressurized systems require energy</li>
    <li><strong>Initial cost and labor</strong> - Investment capability and available labor</li>
    <li><strong>Water quality</strong> - Sediment, salts, and biological contaminants</li>
</ul>

<h3>Improving Irrigation Efficiency</h3>

<h4>1. Proper System Design</h4>
<ul>
    <li>Correct sizing of pipes, pumps, and application devices</li>
    <li>Appropriate operating pressures</li>
    <li>Field layout suited to the irrigation method</li>
    <li>Filtration appropriate to water quality and system type</li>
</ul>

<h4>2. Irrigation Scheduling</h4>
<ul>
    <li>Timing irrigation based on crop water needs, not fixed schedules</li>
    <li>Using soil moisture sensors to guide decisions</li>
    <li>Considering weather forecasts (avoiding irrigation before rain)</li>
    <li>Applying water during optimal times (usually early morning)</li>
</ul>

<h4>3. Maintenance</h4>
<ul>
    <li>Regular system inspections for leaks and clogs</li>
    <li>Cleaning filters and emitters</li>
    <li>Flushing drip lines</li>
    <li>Checking application uniformity</li>
    <li>Repairing or replacing damaged components</li>
</ul>

<h4>4. System Upgrades</h4>
<ul>
    <li>Pressure regulators to ensure optimal operation</li>
    <li>Flow meters to monitor water use</li>
    <li>Automated controls and timers</li>
    <li>Variable rate irrigation technologies</li>
    <li>Weather-based controllers</li>
</ul>

<h3>Case Studies: Irrigation Efficiency Success</h3>

<h4>Small-Scale Example:</h4>
<p>A vegetable farmer in Kenya switched from watering cans to a simple gravity-fed drip system. This reduced labor by 80% and water use by 60%, while increasing yields by 25% due to more consistent moisture levels.</p>

<h4>Medium-Scale Example:</h4>
<p>A cotton farm in India converted from flood to alternate furrow irrigation, installing soil moisture sensors to guide timing. Water use decreased by 30% while maintaining yields, and fertilizer efficiency improved.</p>

<h4>Large-Scale Example:</h4>
<p>A commercial maize operation in South Africa upgraded center pivots with drop nozzles, pressure regulators, and variable rate technology. These changes reduced water use by 20% and energy costs by 25%, while improving yield uniformity.</p>

<h3>Economic Considerations</h3>

<p>When evaluating irrigation systems, consider:</p>

<ul>
    <li>Initial investment vs. long-term returns</li>
    <li>Energy costs for system operation</li>
    <li>Labor requirements and availability</li>
    <li>Expected yield increases</li>
    <li>System lifespan and maintenance costs</li>
    <li>Available subsidies or financing options</li>
</ul>

<p>In the next lesson, we'll explore additional water conservation practices that complement efficient irrigation systems.</p>
            """,
            order_index=2,
            media_type="text",
            points_awarded=15
        ),
        LearningLesson(
            module_id=module2.id,
            title="Rainwater Harvesting",
            content="""
<h2>Rainwater Harvesting</h2>

<p>Capturing and storing rainwater provides a valuable supplemental water source for agriculture. This lesson explores techniques for harvesting rainwater effectively and safely.</p>

<h3>Benefits of Rainwater Harvesting</h3>

<p>Implementing rainwater harvesting systems offers multiple advantages:</p>

<ul>
    <li>Reduces dependence on groundwater and external water sources</li>
    <li>Provides water during dry periods</li>
    <li>Decreases erosion and flooding by capturing runoff</li>
    <li>Generally provides good quality water (low salt content)</li>
    <li>Often requires less energy than pumping groundwater</li>
    <li>Can recharge groundwater when designed for infiltration</li>
    <li>Builds resilience against climate variability</li>
</ul>

<h3>Basic Principles</h3>

<p>Effective rainwater harvesting systems include:</p>

<ol>
    <li><strong>Catchment area</strong> - The surface where rain falls and is collected</li>
    <li><strong>Conveyance system</strong> - Channels, gutters, pipes that transport water</li>
    <li><strong>Storage facility</strong> - Where water is retained for future use</li>
    <li><strong>Distribution system</strong> - Methods to transfer water to crops</li>
    <li><strong>Treatment</strong> - If needed, depending on water use and quality</li>
</ol>

<h3>Rainwater Harvesting Methods</h3>

<h4>1. Rooftop Harvesting</h4>

<p>Collecting rain from building roofs:</p>

<ul>
    <li><strong>Components:</strong>
        <ul>
            <li>Catchment (roof)</li>
            <li>Gutters and downspouts</li>
            <li>First flush diverter (redirects initial dirty runoff)</li>
            <li>Storage tank or cistern</li>
            <li>Overflow system</li>
        </ul>
    </li>
    <li><strong>Best practices:</strong>
        <ul>
            <li>Use clean roofing materials (metal, tile, etc.)</li>
            <li>Install screens to keep out debris and insects</li>
            <li>Size storage based on rainfall patterns and water needs</li>
            <li>Ensure tank is light-proof to prevent algae growth</li>
            <li>Incorporate adequate overflow management</li>
        </ul>
    </li>
    <li><strong>Suitable applications:</strong>
        <ul>
            <li>Greenhouse irrigation</li>
            <li>Small vegetable gardens</li>
            <li>Nurseries</li>
            <li>Supplemental livestock water</li>
        </ul>
    </li>
</ul>

<h4>2. Surface Runoff Harvesting</h4>

<p>Collecting water that flows across the land:</p>

<ul>
    <li><strong>Farm ponds:</strong>
        <ul>
            <li>Excavated depressions to collect runoff</li>
            <li>Can be lined to prevent seepage or unlined to allow infiltration</li>
            <li>Often require pumping for irrigation use</li>
            <li>May include sediment traps to improve water quality</li>
        </ul>
    </li>
    <li><strong>Check dams:</strong>
        <ul>
            <li>Small barriers across water courses to slow flow and trap water</li>
            <li>Causes sediment deposition and enhances infiltration</li>
            <li>Can be constructed from earth, stone, or concrete</li>
            <li>Creates small reservoirs of water for direct use or groundwater recharge</li>
        </ul>
    </li>
    <li><strong>Contour bunds/ridges:</strong>
        <ul>
            <li>Earth embankments built along contour lines</li>
            <li>Intercepts runoff flowing down slopes</li>
            <li>Increases infiltration and soil moisture</li>
            <li>Reduces erosion and nutrient loss</li>
        </ul>
    </li>
</ul>

<h4>3. In-Field Rainwater Harvesting</h4>

<p>Techniques that capture water directly in cropping areas:</p>

<ul>
    <li><strong>Planting basins/Zai pits:</strong>
        <ul>
            <li>Small pits dug in fields to concentrate water and nutrients</li>
            <li>Often filled with organic matter to improve water retention</li>
            <li>Seeds planted directly in pits</li>
            <li>Widely used in semi-arid regions of Africa</li>
        </ul>
    </li>
    <li><strong>Half-moon structures:</strong>
        <ul>
            <li>Semi-circular earth bunds that capture runoff</li>
            <li>Typically arranged in staggered patterns</li>
            <li>Allows planting in concentrated moisture zones</li>
            <li>Effective in rehabilitating degraded land</li>
        </ul>
    </li>
    <li><strong>Tied ridges:</strong>
        <ul>
            <li>Field ridges with cross-ties to create small water-holding basins</li>
            <li>Prevents water from flowing down furrows</li>
            <li>Creates mini-reservoirs throughout the field</li>
            <li>Can double cereal yields in semi-arid regions</li>
        </ul>
    </li>
</ul>

<h3>Planning Considerations</h3>

<p>When implementing rainwater harvesting, consider:</p>

<h4>1. Rainfall Analysis</h4>
<ul>
    <li>Annual rainfall amount and reliability</li>
    <li>Seasonal distribution pattern</li>
    <li>Intensity (affects runoff potential)</li>
    <li>Dry spell frequency (storage needs)</li>
</ul>

<h4>2. Site Assessment</h4>
<ul>
    <li>Catchment area and runoff coefficient</li>
    <li>Slope and topography</li>
    <li>Soil type and infiltration capacity</li>
    <li>Existing drainage patterns</li>
    <li>Available space for storage</li>
</ul>

<h4>3. Water Requirement</h4>
<ul>
    <li>Crop water needs during different growth stages</li>
    <li>Total area to be irrigated</li>
    <li>Other water uses (livestock, processing, etc.)</li>
    <li>Existing water sources and their reliability</li>
</ul>

<h4>4. Technical Capacity</h4>
<ul>
    <li>Available construction materials</li>
    <li>Construction and maintenance skills</li>
    <li>Local knowledge and preferences</li>
    <li>Budget constraints</li>
</ul>

<h3>Calculating Storage Requirements</h3>

<p>A basic formula for estimating potential harvest:</p>

<p>Harvested Water = Catchment Area × Rainfall × Runoff Coefficient</p>

<p>Where:</p>
<ul>
    <li>Catchment Area is in square meters</li>
    <li>Rainfall is in meters (annual or seasonal)</li>
    <li>Runoff Coefficient accounts for losses (roof: 0.7-0.9, land: 0.1-0.5)</li>
    <li>Result is in cubic meters (1 m³ = 1,000 liters)</li>
</ul>

<h3>Maintenance and Management</h3>

<ul>
    <li>Regularly clean gutters, screens, and collection surfaces</li>
    <li>Inspect for and repair leaks in tanks and conveyance systems</li>
    <li>Desilt ponds and check dams after major storms</li>
    <li>Maintain vegetative cover on earthen structures</li>
    <li>Monitor water quality, especially if used for sensitive crops</li>
    <li>Have a plan for overflow during heavy rainfall events</li>
</ul>

<h3>Safety and Health Considerations</h3>

<ul>
    <li>Cover tanks to prevent mosquito breeding and contamination</li>
    <li>Ensure children cannot fall into storage structures</li>
    <li>Test water quality periodically if used for washing produce</li>
    <li>Ensure earthen structures are stable and won't collapse</li>
    <li>Consider treatment options for specific agricultural uses</li>
</ul>

<p>In the next lesson, we'll explore drought-resistant farming techniques that complement water harvesting to create comprehensive water management strategies.</p>
            """,
            order_index=3,
            media_type="text",
            points_awarded=15
        )
    ]
    
    for lesson in lessons2:
        db.session.add(lesson)
    
    # Quiz for Module 2
    quiz2 = LearningQuiz(
        module_id=module2.id,
        title="Water Management Quiz",
        description="Test your knowledge about water conservation techniques and efficient irrigation systems.",
        order_index=4,
        passing_score=70,
        points_awarded=30,
        time_limit=15  # 15 minutes
    )
    db.session.add(quiz2)
    db.session.flush()  # To get the quiz ID
    
    # Questions for Quiz 2
    questions2 = [
        {
            "question": QuizQuestion(
                quiz_id=quiz2.id,
                question_text="Which irrigation system typically has the highest water-use efficiency?",
                question_type="multiple_choice",
                order_index=1,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Flood irrigation", is_correct=False),
                QuestionChoice(choice_text="Furrow irrigation", is_correct=False),
                QuestionChoice(choice_text="Sprinkler irrigation", is_correct=False),
                QuestionChoice(choice_text="Drip irrigation", is_correct=True, explanation="Drip irrigation delivers water directly to the root zone, minimizing evaporation and runoff losses, making it the most efficient system with 90-95% efficiency.")
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz2.id,
                question_text="Which of the following is NOT a benefit of rainwater harvesting?",
                question_type="multiple_choice",
                order_index=2,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Reduces dependence on groundwater", is_correct=False),
                QuestionChoice(choice_text="Provides water during dry periods", is_correct=False),
                QuestionChoice(choice_text="Eliminates the need for irrigation scheduling", is_correct=True, explanation="Rainwater harvesting provides a supplemental water source but does not eliminate the need for proper irrigation scheduling based on crop water needs."),
                QuestionChoice(choice_text="Decreases erosion by capturing runoff", is_correct=False)
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz2.id,
                question_text="When is the critical period for water in maize/corn production?",
                question_type="multiple_choice",
                order_index=3,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Germination and seedling stage", is_correct=False),
                QuestionChoice(choice_text="Tasseling and silk formation", is_correct=True, explanation="Tasseling and silk formation are the most critical periods for water in corn production, as water stress during this time can dramatically reduce pollination success and yield."),
                QuestionChoice(choice_text="Vegetative growth", is_correct=False),
                QuestionChoice(choice_text="Late grain filling", is_correct=False)
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz2.id,
                question_text="What is the main advantage of subsurface drip irrigation over surface drip?",
                question_type="multiple_choice",
                order_index=4,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Lower initial cost", is_correct=False),
                QuestionChoice(choice_text="Easier maintenance", is_correct=False),
                QuestionChoice(choice_text="Reduced evaporation losses", is_correct=True, explanation="Subsurface drip irrigation places water directly in the root zone below the soil surface, significantly reducing evaporation losses compared to surface drip systems."),
                QuestionChoice(choice_text="Better for all soil types", is_correct=False)
            ]
        },
        {
            "question": QuizQuestion(
                quiz_id=quiz2.id,
                question_text="Which of the following is an example of an in-field rainwater harvesting technique?",
                question_type="multiple_choice",
                order_index=5,
                points=10
            ),
            "choices": [
                QuestionChoice(choice_text="Rooftop collection systems", is_correct=False),
                QuestionChoice(choice_text="Farm ponds", is_correct=False),
                QuestionChoice(choice_text="Zai pits", is_correct=True, explanation="Zai pits are small planting basins dug directly in fields to collect rainwater and concentrate it at the plant roots, making them an in-field rainwater harvesting technique."),
                QuestionChoice(choice_text="Large storage tanks", is_correct=False)
            ]
        }
    ]
    
    for q_data in questions2:
        db.session.add(q_data["question"])
        db.session.flush()  # To get the question ID
        
        for choice in q_data["choices"]:
            choice.question_id = q_data["question"].id
            db.session.add(choice)
    
    # Commit all changes
    db.session.commit()
    logger.info("Learning module data seeded successfully")

if __name__ == "__main__":
    with app.app_context():
        seed_learning_modules()