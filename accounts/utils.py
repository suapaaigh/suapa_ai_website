from companion.models import KnowledgeArea

def get_subjects_for_level(education_level, grade_level=None):
    """
    Get recommended subjects based on education level and grade.
    Based on the Ghanaian education curriculum.
    """
    if not education_level:
        return []

    subjects = KnowledgeArea.objects.filter(
        education_level=education_level,
        is_active=True
    )

    if grade_level:
        subjects = subjects.filter(grade_levels__contains=[grade_level])

    return subjects

def initialize_ghanaian_curriculum():
    """
    Initialize the database with Ghanaian curriculum subjects.
    """
    curriculum_data = {
        'nursery': {
            'core': [
                {
                    'name': 'Early Childhood Development',
                    'description': 'Foundation skills for early learners',
                    'topics': ['Play-based Learning', 'Social Skills', 'Basic Communication'],
                    'skills': ['Motor Skills', 'Social Interaction', 'Basic Literacy'],
                    'grade_levels': [1, 2, 3]
                }
            ]
        },
        'primary': {
            'core': [
                {
                    'name': 'English Language',
                    'description': 'English language skills development',
                    'topics': ['Reading', 'Writing', 'Speaking', 'Listening'],
                    'skills': ['Literacy', 'Communication', 'Comprehension'],
                    'grade_levels': [1, 2, 3, 4, 5, 6],
                    'curriculum_code': 'ENG_PRI'
                },
                {
                    'name': 'Mathematics',
                    'description': 'Basic mathematical concepts and problem-solving',
                    'topics': ['Numbers', 'Basic Operations', 'Geometry', 'Measurement'],
                    'skills': ['Numeracy', 'Problem Solving', 'Logical Thinking'],
                    'grade_levels': [1, 2, 3, 4, 5, 6],
                    'curriculum_code': 'MATH_PRI'
                },
                {
                    'name': 'Integrated Science',
                    'description': 'Introduction to scientific concepts',
                    'topics': ['Nature Study', 'Basic Physics', 'Health Education'],
                    'skills': ['Scientific Inquiry', 'Observation', 'Critical Thinking'],
                    'grade_levels': [1, 2, 3, 4, 5, 6],
                    'curriculum_code': 'SCI_PRI'
                },
                {
                    'name': 'Social Studies',
                    'description': 'Understanding society and environment',
                    'topics': ['Community', 'Culture', 'Geography', 'History'],
                    'skills': ['Social Awareness', 'Cultural Understanding', 'Civic Responsibility'],
                    'grade_levels': [1, 2, 3, 4, 5, 6],
                    'curriculum_code': 'SS_PRI'
                }
            ],
            'elective': [
                {
                    'name': 'Religious and Moral Education',
                    'description': 'Moral and ethical development',
                    'topics': ['Values', 'Ethics', 'Religious Studies'],
                    'skills': ['Moral Reasoning', 'Character Development'],
                    'grade_levels': [1, 2, 3, 4, 5, 6],
                    'curriculum_code': 'RME_PRI'
                },
                {
                    'name': 'Creative Arts',
                    'description': 'Artistic and creative expression',
                    'topics': ['Drawing', 'Music', 'Drama', 'Crafts'],
                    'skills': ['Creativity', 'Artistic Expression', 'Cultural Appreciation'],
                    'grade_levels': [1, 2, 3, 4, 5, 6],
                    'curriculum_code': 'CA_PRI'
                }
            ]
        },
        'jhs': {
            'core': [
                {
                    'name': 'English Language',
                    'description': 'Advanced English language skills',
                    'topics': ['Literature', 'Grammar', 'Composition', 'Oral Communication'],
                    'skills': ['Advanced Literacy', 'Critical Analysis', 'Communication'],
                    'grade_levels': [7, 8, 9],
                    'curriculum_code': 'ENG_JHS'
                },
                {
                    'name': 'Mathematics',
                    'description': 'Intermediate mathematics concepts',
                    'topics': ['Algebra', 'Geometry', 'Statistics', 'Number Theory'],
                    'skills': ['Mathematical Reasoning', 'Problem Solving', 'Data Analysis'],
                    'grade_levels': [7, 8, 9],
                    'curriculum_code': 'MATH_JHS'
                },
                {
                    'name': 'Integrated Science',
                    'description': 'Comprehensive science education',
                    'topics': ['Biology', 'Chemistry', 'Physics', 'Environmental Science'],
                    'skills': ['Scientific Method', 'Experimentation', 'Analysis'],
                    'grade_levels': [7, 8, 9],
                    'curriculum_code': 'SCI_JHS'
                },
                {
                    'name': 'Social Studies',
                    'description': 'Advanced social and environmental studies',
                    'topics': ['Government', 'Economics', 'Geography', 'History'],
                    'skills': ['Critical Thinking', 'Research', 'Civic Engagement'],
                    'grade_levels': [7, 8, 9],
                    'curriculum_code': 'SS_JHS'
                }
            ],
            'elective': [
                {
                    'name': 'Information and Communication Technology',
                    'description': 'Digital literacy and computer skills',
                    'topics': ['Computer Basics', 'Internet', 'Software Applications', 'Programming'],
                    'skills': ['Digital Literacy', 'Technology Skills', 'Problem Solving'],
                    'grade_levels': [7, 8, 9],
                    'curriculum_code': 'ICT_JHS'
                },
                {
                    'name': 'French',
                    'description': 'French language learning',
                    'topics': ['Basic French', 'Conversation', 'Grammar', 'Culture'],
                    'skills': ['Language Skills', 'Cultural Awareness', 'Communication'],
                    'grade_levels': [7, 8, 9],
                    'curriculum_code': 'FR_JHS'
                }
            ]
        },
        'shs': {
            'core': [
                {
                    'name': 'Core Mathematics',
                    'description': 'Essential mathematics for all students',
                    'topics': ['Algebra', 'Calculus', 'Statistics', 'Trigonometry'],
                    'skills': ['Advanced Mathematical Thinking', 'Problem Solving', 'Analytical Skills'],
                    'grade_levels': [10, 11, 12],
                    'curriculum_code': 'MATH_SHS_CORE'
                },
                {
                    'name': 'English Language',
                    'description': 'Advanced English proficiency',
                    'topics': ['Literature Analysis', 'Academic Writing', 'Critical Reading'],
                    'skills': ['Advanced Communication', 'Literary Analysis', 'Academic Writing'],
                    'grade_levels': [10, 11, 12],
                    'curriculum_code': 'ENG_SHS'
                },
                {
                    'name': 'Integrated Science',
                    'description': 'Foundation science for all students',
                    'topics': ['Scientific Principles', 'Research Methods', 'Environmental Issues'],
                    'skills': ['Scientific Literacy', 'Research Skills', 'Critical Analysis'],
                    'grade_levels': [10, 11, 12],
                    'curriculum_code': 'SCI_SHS'
                },
                {
                    'name': 'Social Studies',
                    'description': 'Advanced social studies concepts',
                    'topics': ['Governance', 'Development', 'International Relations', 'Research Methods'],
                    'skills': ['Research', 'Analysis', 'Critical Thinking', 'Civic Knowledge'],
                    'grade_levels': [10, 11, 12],
                    'curriculum_code': 'SS_SHS'
                }
            ],
            'elective': [
                {
                    'name': 'Physics',
                    'description': 'Advanced physics concepts',
                    'topics': ['Mechanics', 'Thermodynamics', 'Electricity', 'Modern Physics'],
                    'skills': ['Scientific Analysis', 'Mathematical Application', 'Experimentation'],
                    'grade_levels': [10, 11, 12],
                    'curriculum_code': 'PHYS_SHS'
                },
                {
                    'name': 'Chemistry',
                    'description': 'Advanced chemistry concepts',
                    'topics': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry'],
                    'skills': ['Chemical Analysis', 'Laboratory Skills', 'Problem Solving'],
                    'grade_levels': [10, 11, 12],
                    'curriculum_code': 'CHEM_SHS'
                },
                {
                    'name': 'Biology',
                    'description': 'Advanced biological sciences',
                    'topics': ['Cell Biology', 'Genetics', 'Ecology', 'Human Biology'],
                    'skills': ['Biological Analysis', 'Research Methods', 'Scientific Communication'],
                    'grade_levels': [10, 11, 12],
                    'curriculum_code': 'BIO_SHS'
                }
            ]
        }
    }

    # Create or update KnowledgeArea objects
    for level, categories in curriculum_data.items():
        for category, subjects in categories.items():
            for subject_data in subjects:
                knowledge_area, created = KnowledgeArea.objects.get_or_create(
                    name=subject_data['name'],
                    education_level=level,
                    defaults={
                        'description': subject_data['description'],
                        'subject_category': category,
                        'grade_levels': subject_data['grade_levels'],
                        'topics': subject_data['topics'],
                        'skills_developed': subject_data['skills'],
                        'curriculum_code': subject_data.get('curriculum_code', ''),
                        'learning_objectives': [],
                        'assessment_criteria': []
                    }
                )
                if created:
                    print(f"Created: {knowledge_area}")
                else:
                    print(f"Exists: {knowledge_area}")

def get_learning_style_recommendations(learning_style):
    """
    Get content type recommendations based on learning style.
    """
    recommendations = {
        'visual': ['video', 'infographic', 'diagram', 'chart', 'image'],
        'auditory': ['audio', 'podcast', 'video', 'discussion', 'lecture'],
        'kinesthetic': ['interactive', 'simulation', 'project', 'experiment', 'game'],
        'reading': ['text', 'article', 'ebook', 'document', 'quiz'],
        'mixed': ['video', 'interactive', 'text', 'quiz', 'project']
    }

    return recommendations.get(learning_style, recommendations['mixed'])