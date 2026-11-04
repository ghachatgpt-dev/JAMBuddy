import streamlit as st
import sqlite3
from pathlib import Path
from datetime import datetime

# ============================================================
# JAMBUDDY — Student guidance, JAMB preparation and global
# university discovery in one Streamlit application.
# ============================================================

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "jambuddy_history.db"

st.set_page_config(
    page_title="JAMBUDDY | Your Friendly Guide to University Success",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Styling ----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root { --ink:#20352c; --green:#276749; --mint:#eaf4ed; --cream:#fbfaf5; --gold:#c49a4a; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:var(--cream); color:var(--ink); }
[data-testid="stSidebar"] { background:#edf4ee; border-right:1px solid #dce8de; }
h1,h2,h3 { color:var(--ink); }
.hero {
  background:linear-gradient(120deg,#e8f3e9 0%,#fbf6e9 100%);
  border:1px solid #dce9dc; border-radius:24px; padding:32px 34px;
  margin-bottom:18px;
}
.hero h1 { font-family:'Playfair Display',serif; font-size:2.65rem; margin:0; color:#245b42; }
.hero p { color:#52695b; font-size:1.04rem; margin:8px 0 0 0; }
.eyebrow { color:#a17b35; font-weight:700; letter-spacing:2px; font-size:.76rem; text-transform:uppercase; }
.info-card {
 background:white; border:1px solid #e3e9e1; border-radius:17px;
 padding:18px 20px; height:100%;
}
.info-card h3 { margin-top:0; color:#276749; font-size:1.08rem; }
.small-note { color:#65776c; font-size:.86rem; }
.pill { display:inline-block; padding:4px 10px; background:#edf5ee; color:#276749;
 border-radius:99px; font-size:.78rem; font-weight:700; margin:2px 4px 2px 0; }
div.stButton > button {
 border-radius:12px; border:1px solid #c9ddce; font-weight:700;
}
div.stButton > button[kind="primary"] { background:#276749; border-color:#276749; }
[data-testid="stMetric"] { background:white; border:1px solid #e4eae2; padding:15px; border-radius:15px; }
hr { border-color:#e4e9e1; }
</style>
""", unsafe_allow_html=True)

# ----------------------------- Database ---------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student TEXT NOT NULL,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                date_taken TEXT NOT NULL
            )
        """)
        conn.commit()

def save_result(student, subject, score, total):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO quiz_history(student, subject, score, total, date_taken) VALUES(?,?,?,?,?)",
            (student.strip() or "Guest", subject, score, total, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()

def get_history(student=None):
    with sqlite3.connect(DB_PATH) as conn:
        if student:
            return conn.execute(
                "SELECT subject, score, total, date_taken FROM quiz_history WHERE student=? ORDER BY id DESC LIMIT 30",
                (student,)
            ).fetchall()
        return conn.execute(
            "SELECT student, subject, score, total, date_taken FROM quiz_history ORDER BY id DESC LIMIT 30"
        ).fetchall()

init_db()

# ----------------------------- Data -------------------------
# Built-in starter directory, designed to be searchable in-app.
# This is a curated sample, not a complete worldwide register.
UNIVERSITIES = [
    ("University of Lagos", "Nigeria", "Africa", ["Computer Science","Medicine","Law","Economics","Accounting","Engineering","Mass Communication"]),
    ("University of Ibadan", "Nigeria", "Africa", ["Medicine","Law","Computer Science","Pharmacy","Economics","Agriculture"]),
    ("Ahmadu Bello University", "Nigeria", "Africa", ["Engineering","Medicine","Law","Computer Science","Agriculture","Economics"]),
    ("Obafemi Awolowo University", "Nigeria", "Africa", ["Medicine","Law","Computer Science","Engineering","Architecture","Economics"]),
    ("University of Ghana", "Ghana", "Africa", ["Computer Science","Business","Law","Medicine","Engineering","Psychology"]),
    ("University of Cape Town", "South Africa", "Africa", ["Computer Science","Medicine","Law","Engineering","Business","Environmental Science"]),
    ("University of Nairobi", "Kenya", "Africa", ["Medicine","Law","Engineering","Computer Science","Business","Agriculture"]),
    ("Cairo University", "Egypt", "Africa", ["Medicine","Engineering","Law","Computer Science","Business"]),
    ("University of Oxford", "United Kingdom", "Europe", ["Law","Medicine","Computer Science","Economics","Engineering","Politics","English"]),
    ("University of Cambridge", "United Kingdom", "Europe", ["Medicine","Engineering","Computer Science","Law","Economics","Natural Sciences"]),
    ("Imperial College London", "United Kingdom", "Europe", ["Engineering","Medicine","Computer Science","Mathematics","Business"]),
    ("University College London", "United Kingdom", "Europe", ["Architecture","Medicine","Law","Computer Science","Psychology","Economics"]),
    ("University of Edinburgh", "United Kingdom", "Europe", ["Computer Science","Medicine","Law","Business","Engineering","Psychology"]),
    ("Sorbonne University", "France", "Europe", ["Mathematics","Medicine","Physics","Computer Science","Humanities"]),
    ("ETH Zurich", "Switzerland", "Europe", ["Engineering","Computer Science","Mathematics","Physics","Architecture"]),
    ("Technical University of Munich", "Germany", "Europe", ["Engineering","Computer Science","Business","Physics","Medicine"]),
    ("University of Amsterdam", "Netherlands", "Europe", ["Psychology","Law","Business","Computer Science","Economics"]),
    ("University of Toronto", "Canada", "North America", ["Computer Science","Medicine","Engineering","Business","Law","Psychology"]),
    ("McGill University", "Canada", "North America", ["Medicine","Law","Engineering","Computer Science","Arts","Business"]),
    ("University of British Columbia", "Canada", "North America", ["Computer Science","Forestry","Medicine","Business","Engineering"]),
    ("Harvard University", "United States", "North America", ["Law","Medicine","Business","Computer Science","Economics","Government"]),
    ("Massachusetts Institute of Technology", "United States", "North America", ["Engineering","Computer Science","Physics","Mathematics","Economics"]),
    ("Stanford University", "United States", "North America", ["Computer Science","Engineering","Business","Medicine","Law","Psychology"]),
    ("University of California, Berkeley", "United States", "North America", ["Computer Science","Engineering","Business","Law","Economics"]),
    ("New York University", "United States", "North America", ["Business","Law","Medicine","Arts","Computer Science","Film"]),
    ("University of Melbourne", "Australia", "Oceania", ["Medicine","Law","Engineering","Business","Computer Science","Education"]),
    ("Australian National University", "Australia", "Oceania", ["Politics","Law","Computer Science","Science","Economics"]),
    ("University of Sydney", "Australia", "Oceania", ["Medicine","Engineering","Business","Law","Computer Science","Architecture"]),
    ("University of Auckland", "New Zealand", "Oceania", ["Engineering","Medicine","Law","Business","Computer Science"]),
    ("University of Tokyo", "Japan", "Asia", ["Engineering","Medicine","Computer Science","Law","Economics","Science"]),
    ("Kyoto University", "Japan", "Asia", ["Science","Engineering","Medicine","Law","Economics"]),
    ("National University of Singapore", "Singapore", "Asia", ["Computer Science","Business","Law","Medicine","Engineering"]),
    ("Nanyang Technological University", "Singapore", "Asia", ["Engineering","Computer Science","Business","Education","Science"]),
    ("University of Hong Kong", "Hong Kong", "Asia", ["Medicine","Law","Business","Computer Science","Engineering"]),
    ("Seoul National University", "South Korea", "Asia", ["Engineering","Medicine","Business","Law","Computer Science"]),
    ("Tsinghua University", "China", "Asia", ["Engineering","Computer Science","Architecture","Business","Science"]),
    ("University of Delhi", "India", "Asia", ["Commerce","Economics","Law","Computer Science","Political Science"]),
    ("Indian Institute of Technology Bombay", "India", "Asia", ["Engineering","Computer Science","Mathematics","Design"]),
    ("University of the Philippines", "Philippines", "Asia", ["Medicine","Law","Engineering","Business","Computer Science"]),
    ("American University of Beirut", "Lebanon", "Asia", ["Medicine","Engineering","Business","Architecture","Computer Science"]),
    ("University of São Paulo", "Brazil", "South America", ["Medicine","Law","Engineering","Business","Computer Science"]),
    ("University of Chile", "Chile", "South America", ["Medicine","Law","Engineering","Economics","Computer Science"]),
    ("University of Buenos Aires", "Argentina", "South America", ["Medicine","Law","Engineering","Psychology","Economics"]),
]

CAREER_DATA = {
    "Technology & Computing": {
        "courses": ["Computer Science", "Software Engineering", "Information Technology", "Cybersecurity", "Data Science"],
        "careers": ["Software Developer", "Data Analyst", "Cybersecurity Analyst", "Cloud Engineer", "UX Designer"],
        "strengths": "Problem-solving, logical thinking, creativity and curiosity about technology."
    },
    "Health & Life Sciences": {
        "courses": ["Medicine", "Nursing", "Pharmacy", "Medical Laboratory Science", "Biochemistry", "Public Health"],
        "careers": ["Doctor", "Nurse", "Pharmacist", "Medical Laboratory Scientist", "Public Health Officer"],
        "strengths": "Care for people, patience, attention to detail and interest in biology."
    },
    "Business & Finance": {
        "courses": ["Accounting", "Economics", "Business Administration", "Banking and Finance", "Marketing"],
        "careers": ["Accountant", "Financial Analyst", "Entrepreneur", "Business Manager", "Marketing Strategist"],
        "strengths": "Numeracy, communication, organisation and decision-making."
    },
    "Law & Society": {
        "courses": ["Law", "Political Science", "International Relations", "Sociology", "Criminology"],
        "careers": ["Lawyer", "Diplomat", "Policy Analyst", "Human Rights Advocate", "Researcher"],
        "strengths": "Reading, writing, critical thinking, fairness and persuasive communication."
    },
    "Engineering & Design": {
        "courses": ["Civil Engineering", "Mechanical Engineering", "Electrical Engineering", "Architecture", "Industrial Design"],
        "careers": ["Civil Engineer", "Mechanical Engineer", "Architect", "Product Designer", "Project Engineer"],
        "strengths": "Mathematics, creativity, spatial thinking and practical problem-solving."
    },
    "Arts, Media & Communication": {
        "courses": ["Mass Communication", "English", "Film Studies", "Graphic Design", "Theatre Arts"],
        "careers": ["Journalist", "Writer", "Content Creator", "Public Relations Officer", "Film Producer"],
        "strengths": "Creativity, storytelling, confidence and strong communication."
    },
    "Education & Research": {
        "courses": ["Education", "Educational Psychology", "Mathematics", "Biology", "Chemistry"],
        "careers": ["Teacher", "Lecturer", "Education Consultant", "Academic Researcher", "Learning Designer"],
        "strengths": "Curiosity, patience, explaining ideas and helping others learn."
    },
}

SUBJECT_COMBINATIONS = {
    "Medicine and Surgery": ["Use of English", "Biology", "Chemistry", "Physics"],
    "Nursing": ["Use of English", "Biology", "Chemistry", "Physics"],
    "Pharmacy": ["Use of English", "Biology", "Chemistry", "Physics"],
    "Computer Science": ["Use of English", "Mathematics", "Physics", "One of Biology, Chemistry, Agricultural Science or Economics"],
    "Engineering": ["Use of English", "Mathematics", "Physics", "Chemistry"],
    "Law": ["Use of English", "Literature in English", "One Arts subject", "One other Arts or Social Science subject"],
    "Accounting": ["Use of English", "Mathematics", "Economics", "One other relevant subject"],
    "Economics": ["Use of English", "Mathematics", "Economics", "One other relevant subject"],
    "Mass Communication": ["Use of English", "Literature in English", "One Arts subject", "One Social Science subject"],
    "Architecture": ["Use of English", "Mathematics", "Physics", "One of Chemistry, Geography or Technical Drawing"],
    "Agriculture": ["Use of English", "Chemistry", "Biology or Agricultural Science", "Mathematics or Physics"],
    "Biochemistry": ["Use of English", "Biology", "Chemistry", "Physics"],
}

QUIZ_BANK = {
    "Use of English": [
        ("Choose the word closest in meaning to 'abundant'.", ["Scarce", "Plentiful", "Tiny", "Empty"], 1, "'Abundant' means existing in large quantities; plentiful is the closest synonym."),
        ("Choose the correctly spelt word.", ["Accomodation", "Acommodation", "Accommodation", "Acomodation"], 2, "Accommodation is spelt with double c and double m."),
        ("Identify the noun in: 'The curious student asked a question.'", ["Curious", "Student", "Asked", "A"], 1, "'Student' names a person, so it is a noun."),
        ("Choose the correct option: 'Neither of the boys ___ present.'", ["are", "were", "is", "have"], 2, "'Neither' is singular in this construction, so it takes 'is'."),
        ("The opposite of 'expand' is:", ["Extend", "Contract", "Increase", "Enlarge"], 1, "'Contract' means to become smaller, the opposite of expand."),
    ],
    "Mathematics": [
        ("If 3x + 5 = 20, find x.", ["3", "5", "7", "8"], 1, "3x = 15, therefore x = 5."),
        ("Find 15% of 240.", ["24", "30", "36", "40"], 2, "0.15 × 240 = 36."),
        ("Simplify 2(3x − 4) + x.", ["7x − 8", "6x − 8", "7x + 8", "5x − 4"], 0, "Expand to get 6x − 8 + x = 7x − 8."),
        ("The mean of 4, 6, 8 and 10 is:", ["6", "7", "8", "9"], 1, "(4 + 6 + 8 + 10) ÷ 4 = 7."),
        ("A triangle has angles 55° and 65°. Find the third angle.", ["50°", "60°", "70°", "80°"], 1, "Angles in a triangle add up to 180°. 180 − 120 = 60°."),
    ],
    "Biology": [
        ("Which organelle is mainly responsible for aerobic respiration?", ["Ribosome", "Mitochondrion", "Vacuole", "Golgi body"], 1, "Mitochondria are the main site of aerobic respiration and ATP production."),
        ("The basic structural and functional unit of life is the:", ["Tissue", "Organ", "Cell", "System"], 2, "The cell is the basic unit of living organisms."),
        ("Which blood cells help the body fight infection?", ["Red blood cells", "White blood cells", "Platelets", "Plasma"], 1, "White blood cells defend the body against pathogens."),
        ("Photosynthesis mainly takes place in the:", ["Nucleus", "Chloroplast", "Mitochondrion", "Cell wall"], 1, "Chloroplasts contain chlorophyll, which captures light energy."),
        ("The male reproductive part of a flower is the:", ["Stigma", "Ovary", "Stamen", "Sepal"], 2, "The stamen is the male reproductive structure of a flower."),
    ],
    "Chemistry": [
        ("The atomic number of an element is the number of:", ["Neutrons", "Protons", "Shells", "Molecules"], 1, "Atomic number equals the number of protons in the nucleus."),
        ("Which gas is produced when an acid reacts with a reactive metal?", ["Oxygen", "Nitrogen", "Hydrogen", "Chlorine"], 2, "Acid + reactive metal generally produces a salt and hydrogen gas."),
        ("A solution with pH 3 is:", ["Acidic", "Neutral", "Alkaline", "Always salty"], 0, "A pH below 7 is acidic."),
        ("What is the chemical formula for water?", ["CO₂", "H₂O", "NaCl", "O₂"], 1, "A water molecule contains two hydrogen atoms and one oxygen atom."),
        ("Which method is most suitable for separating an insoluble solid from a liquid?", ["Filtration", "Distillation", "Chromatography", "Crystallisation"], 0, "Filtration traps the insoluble solid while the liquid passes through."),
    ],
}

# ----------------------------- Helpers ----------------------
def hero(title, subtitle, eyebrow="WELCOME TO JAMBUDDY"):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{eyebrow}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True
    )

def card(title, body):
    st.markdown(f'<div class="info-card"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)

def get_student():
    return st.session_state.get("student_name", "").strip() or "Guest"

# ----------------------------- Sidebar ----------------------
with st.sidebar:
    st.markdown("## 🎓 JAMBUDDY")
    st.caption("Your Friendly Guide to University Success")
    st.divider()
    student_name = st.text_input("Your name or nickname (optional)", key="student_name_input", placeholder="e.g. Ada")
    st.session_state["student_name"] = student_name
    page = st.radio(
        "Explore JAMBUDDY",
        ["Home", "Global University Finder", "Career & Course Adviser", "JAMB Study Centre", "Practice Quiz", "My Progress", "About"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Study Smart. Choose Right. Get Ahead.")

# ----------------------------- Home -------------------------
if page == "Home":
    hero("Your future starts with a choice.", "Explore your interests, discover universities around the world and prepare for your next academic step.")
    st.markdown("### Welcome to JAMBUDDY 👋")
    st.write("One friendly space for career exploration, course guidance, university discovery and JAMB practice.")
    cols = st.columns(3)
    with cols[0]:
        card("🌍 Global universities", "Explore a built-in directory of universities across Africa, Europe, Asia, the Americas and Oceania.")
    with cols[1]:
        card("🧭 Career direction", "Connect your interests and strengths to possible courses and career paths.")
    with cols[2]:
        card("📚 JAMB preparation", "Review subject-combination guidance, study tips and original practice questions.")
    st.markdown("### Start exploring")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Find a university", use_container_width=True):
            st.session_state["nav_target"] = "Global University Finder"
            st.rerun()
    with c2:
        if st.button("Explore careers", use_container_width=True):
            st.session_state["nav_target"] = "Career & Course Adviser"
            st.rerun()
    with c3:
        if st.button("Practise for JAMB", use_container_width=True):
            st.session_state["nav_target"] = "Practice Quiz"
            st.rerun()
    st.info("Tip: Use the navigation menu on the left to open any section. Your quiz results can be saved on this device.")

# ----------------------------- University Finder ------------
elif page == "Global University Finder":
    hero("Find your university.", "Discover institutions in different countries and explore the courses listed in our directory.", "GLOBAL UNIVERSITY FINDER")
    st.info("This is an in-app starter directory. It is not a complete worldwide university register, and course availability can change. Use it to explore options and make a shortlist.")
    countries = sorted({u[1] for u in UNIVERSITIES})
    continents = ["All regions"] + sorted({u[2] for u in UNIVERSITIES})
    f1, f2, f3 = st.columns([1, 1, 1.3])
    with f1:
        region = st.selectbox("Continent / region", continents)
    with f2:
        country_options = ["All countries"] + countries
        country = st.selectbox("Country", country_options)
    with f3:
        search_term = st.text_input("University or course", placeholder="e.g. Toronto, medicine, engineering")
    filtered = []
    for name, nation, continent, courses in UNIVERSITIES:
        if region != "All regions" and continent != region:
            continue
        if country != "All countries" and nation != country:
            continue
        haystack = " ".join([name, nation, continent] + courses).lower()
        if search_term.strip() and search_term.strip().lower() not in haystack:
            continue
        filtered.append((name, nation, continent, courses))
    st.markdown(f"**{len(filtered)} universities found**")
    if filtered:
        for start in range(0, len(filtered), 2):
            pair = st.columns(2)
            for col, item in zip(pair, filtered[start:start+2]):
                name, nation, continent, courses = item
                with col:
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown(f"### 🏛️ {name}")
                    st.markdown(f"**{nation}** · {continent}")
                    st.markdown("**Courses in this directory**")
                    st.write(", ".join(courses))
                    st.caption("Course list is illustrative; check the institution's current official prospectus before applying.")
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No match in the built-in directory. Try a broader search or another country/region.")
    st.markdown("---")
    st.markdown("### Build your shortlist")
    st.write("Use the filters to compare countries and course options. JAMBUDDY does not open Google or send you to another website.")

# ----------------------------- Career Adviser ---------------
elif page == "Career & Course Adviser":
    hero("Discover what suits you.", "Your interests and strengths can help you explore possible courses and career directions.", "CAREER & COURSE ADVISER")
    st.write("Choose the area that sounds most interesting to you. You can explore more than one area by changing your selection.")
    area = st.selectbox("Which area interests you most?", list(CAREER_DATA.keys()))
    data = CAREER_DATA[area]
    st.markdown(f"## {area}")
    st.write(f"**Strengths that may help:** {data['strengths']}")
    a, b = st.columns(2)
    with a:
        card("🎓 Courses to explore", "<ul>" + "".join(f"<li>{x}</li>" for x in data["courses"]) + "</ul>")
    with b:
        card("💼 Possible careers", "<ul>" + "".join(f"<li>{x}</li>" for x in data["careers"]) + "</ul>")
    st.markdown("### Tell us a little more")
    interests = st.multiselect("What do you enjoy?", ["Solving problems", "Helping people", "Creating things", "Working with numbers", "Writing and speaking", "Exploring technology", "Understanding society", "Designing and building"])
    strengths = st.multiselect("Which strengths describe you?", ["Creative", "Analytical", "Patient", "Organised", "Curious", "Confident communicator", "Practical", "Empathetic"])
    if st.button("Create my reflection", type="primary"):
        if not interests and not strengths:
            st.warning("Choose at least one interest or strength to create your reflection.")
        else:
            st.success("Your reflection")
            st.write("You selected: " + (", ".join(interests + strengths) if interests or strengths else "No selections"))
            st.write(f"Consider researching **{area}** and comparing the courses above with your favourite subjects, grades and long-term goals.")
            st.caption("This is an exploration tool, not a psychological assessment or a guaranteed career prediction.")

# ----------------------------- JAMB Study Centre ------------
elif page == "JAMB Study Centre":
    hero("Prepare with confidence.", "A simple study space for JAMB subject guidance, revision habits and exam-day preparation.", "JAMB STUDY CENTRE")
    tab1, tab2, tab3, tab4 = st.tabs(["Subject combinations", "Study plan", "Exam tips", "JAMB basics"])
    with tab1:
        st.markdown("### Explore a course's typical subject combination")
        course = st.selectbox("Choose a course", list(SUBJECT_COMBINATIONS.keys()))
        st.write("**Subjects shown in this guide:**")
        for subject in SUBJECT_COMBINATIONS[course]:
            st.markdown(f"- {subject}")
        st.warning("Important: These are general study-guide examples, not an official or universal subject-combination ruling. Requirements may differ by institution, course and admission year. Confirm the current combination with the relevant admissions authority before registration.")
    with tab2:
        st.markdown("### A simple weekly revision routine")
        plan = [
            ("Monday", "Revise topic notes and make short summaries."),
            ("Tuesday", "Practise questions in your most challenging subject."),
            ("Wednesday", "Review English comprehension, vocabulary and grammar."),
            ("Thursday", "Work through calculations and show every step."),
            ("Friday", "Attempt a timed mixed-subject practice session."),
            ("Saturday", "Mark your work and revise mistakes."),
            ("Sunday", "Rest, organise materials and plan the next week."),
        ]
        for day, task in plan:
            st.markdown(f"**{day}:** {task}")
        st.caption("Adjust the routine to your school timetable and personal study needs.")
    with tab3:
        tips = [
            "Read each question carefully before selecting an answer.",
            "Practise with a timer so you become comfortable working under time limits.",
            "Review every incorrect answer and understand why it was wrong.",
            "Do not spend too long on one difficult question; return to it if time allows.",
            "Sleep well, eat properly and prepare your materials ahead of exam day.",
            "Use reliable, current information when checking registration and examination updates.",
        ]
        for tip in tips:
            st.markdown(f"- {tip}")
    with tab4:
        st.markdown("### What is JAMB?")
        st.write("JAMB is Nigeria's Joint Admissions and Matriculation Board. It administers the Unified Tertiary Matriculation Examination (UTME), which is used by participating institutions as part of their admission process.")
        st.markdown("### What should you prepare?")
        st.write("Understand your intended course, check the required UTME subjects, revise the relevant topics, practise questions and keep track of official registration and examination announcements.")
        st.info("JAMBUDDY keeps this learning guidance inside the app. It does not redirect you to the JAMB website or IBASS. For real registration, official results or binding admission decisions, always rely on current official announcements and your chosen institution.")

# ----------------------------- Practice Quiz ----------------
elif page == "Practice Quiz":
    hero("Practise. Learn. Improve.", "Try original practice questions, get explanations and save your score to your progress page.", "PRACTICE QUIZ")
    subject = st.selectbox("Choose a subject", list(QUIZ_BANK.keys()))
    questions = QUIZ_BANK[subject]
    quiz_key = f"answers_{subject}"
    if st.session_state.get("active_quiz_subject") != subject:
        st.session_state["active_quiz_subject"] = subject
        st.session_state[quiz_key] = {}
        st.session_state["quiz_submitted"] = False
    if st.session_state.get("quiz_submitted", False):
        st.info("You have submitted this quiz. Select another subject or click **Start again** to try it again.")
        if st.button("Start again"):
            st.session_state[quiz_key] = {}
            st.session_state["quiz_submitted"] = False
            st.rerun()
    else:
        with st.form(f"quiz_form_{subject}"):
            chosen = {}
            for i, (question, options, correct, explanation) in enumerate(questions):
                st.markdown(f"**{i+1}. {question}**")
                chosen[i] = st.radio("Select one answer", options, key=f"{subject}_{i}", index=None, label_visibility="collapsed")
                st.divider()
            submitted = st.form_submit_button("Submit my answers", type="primary", use_container_width=True)
        if submitted:
            unanswered = [i for i, val in chosen.items() if val is None]
            if unanswered:
                st.warning(f"Please answer all {len(questions)} questions before submitting.")
            else:
                score = sum(1 for i, val in chosen.items() if val == questions[i][1][questions[i][2]])
                st.session_state["quiz_score"] = score
                st.session_state["quiz_submitted"] = True
                save_result(get_student(), subject, score, len(questions))
                st.rerun()
    if st.session_state.get("quiz_submitted", False):
        score = st.session_state.get("quiz_score", 0)
        st.metric("Your score", f"{score}/{len(questions)}", f"{round(score/len(questions)*100)}%")
        if score == len(questions):
            st.success("Excellent work! You got every question correct.")
        elif score >= 3:
            st.success("Good effort! Review the explanations and keep practising.")
        else:
            st.info("Every attempt is progress. Review the explanations and try again.")
        for i, (question, options, correct, explanation) in enumerate(questions):
            st.markdown(f"**{i+1}. {question}**")
            st.write(f"Correct answer: **{options[correct]}**")
            st.caption(explanation)
        st.caption("These are original practice questions created for JAMBUDDY. They are not official JAMB past questions.")

# ----------------------------- Progress ---------------------
elif page == "My Progress":
    hero("Your progress matters.", "Review saved practice scores and see how your preparation is developing.", "MY PROGRESS")
    student = get_student()
    history = get_history(student)
    if history:
        total_attempts = len(history)
        avg = sum((r[1] / r[2]) * 100 for r in history) / total_attempts
        c1, c2 = st.columns(2)
        c1.metric("Saved attempts", total_attempts)
        c2.metric("Average score", f"{avg:.0f}%")
        st.markdown("### Recent quiz attempts")
        st.dataframe(
            [{"Subject": r[0], "Score": f"{r[1]}/{r[2]}", "Percentage": f"{(r[1]/r[2])*100:.0f}%", "Date": r[3]} for r in history],
            use_container_width=True,
            hide_index=True
        )
        st.caption("Scores are stored locally in the app's SQLite database on this computer.")
    else:
        st.info("No saved results yet. Complete a practice quiz and your results will appear here.")
    st.markdown("### A reminder")
    st.write("Progress is more than one score. Notice the topics you understand, revisit the ones you find difficult and keep a steady study routine.")

# ----------------------------- About ------------------------
elif page == "About":
    hero("A little about JAMBUDDY.", "A friendly academic companion for students exploring their next steps.", "ABOUT THE APP")
    st.markdown("### Our purpose")
    st.write("JAMBUDDY helps students explore possible careers, discover university options around the world and prepare for JAMB using learning resources contained within the app.")
    st.markdown("### What makes it useful?")
    st.markdown("- A built-in university directory with country, region and course filters.\n- Career and course exploration based on interests and strengths.\n- In-app JAMB subject guidance and study tips.\n- Original practice questions with explanations.\n- Local quiz history to help students reflect on progress.")
    st.markdown("### Important information")
    st.write("JAMBUDDY is an educational guidance project. It is not affiliated with JAMB or any university, and it does not process applications, register candidates or guarantee admission. The university directory is a curated starter list, not a complete global database. Course availability and entry requirements can change, so students should confirm details before making application decisions.")
    st.caption("JAMBUDDY — Study Smart. Choose Right. Get Ahead.")
