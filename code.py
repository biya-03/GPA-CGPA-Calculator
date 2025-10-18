import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPA & CGPA Calculator", layout="centered")

st.title("🎓 GPA & CGPA Calculator (4 Semesters)")

st.write("""
This web app calculates GPA for each of 4 semesters and the Cumulative GPA (CGPA) after each one.
""")

# ---------- Function Definitions ----------

def marks_to_gpa(marks):
    if marks >= 85:
        return 4.00  # A
    elif marks >= 80:
        return 3.66  # A-
    elif marks >= 75:
        return 3.33  # B+
    elif marks >= 70:
        return 2.66  # B-
    elif marks >= 67:
        return 2.33  # C+
    elif marks >= 60:
        return 2.00  # C
    elif marks >= 50:
        return 1.00  # D
    else:
        return 0.00  # F

def calculate_gpa(subjects):
    total_points = sum([marks_to_gpa(s['marks']) * s['credits'] for s in subjects])
    total_credits = sum([s['credits'] for s in subjects])
    return total_points / total_credits if total_credits > 0 else 0


# ---------- Semester Inputs ----------

semesters = [1, 2, 3, 4]
semester_data = {}

for sem in semesters:
    st.header(f"📘 Semester {sem}")
    num_subjects = st.number_input(
        f"Enter number of subjects for Semester {sem}",
        min_value=1, max_value=10, key=f"num_{sem}"
    )

    subjects = []
    for i in range(int(num_subjects)):
        st.subheader(f"Subject {i+1}")
        marks = st.number_input(
            f"Enter Marks for Subject {i+1} (Semester {sem})",
            min_value=0, max_value=100, step=1, key=f"marks_{sem}_{i}"
        )
        credits = st.number_input(
            f"Enter Credit Hours for Subject {i+1} (Semester {sem})",
            min_value=1, max_value=5, step=1, key=f"credit_{sem}_{i}"
        )
        subjects.append({"marks": marks, "credits": credits})
    semester_data[sem] = subjects


# ---------- GPA & CGPA Button ----------

if st.button("Calculate GPA & CGPA"):
    results = []
    total_points = 0
    total_credits = 0

    for sem in semesters:
        gpa = calculate_gpa(semester_data[sem])
        results.append({"Semester": sem, "GPA": round(gpa, 2)})

        sem_points = sum([marks_to_gpa(s['marks']) * s['credits'] for s in semester_data[sem]])
        sem_credits = sum([s['credits'] for s in semester_data[sem]])

        total_points += sem_points
        total_credits += sem_credits

        cgpa = total_points / total_credits if total_credits > 0 else 0
        results[-1]["CGPA (Cumulative)"] = round(cgpa, 2)

    st.success("✅ Calculation Complete!")
    st.subheader("📊 Semester-wise GPA & Cumulative CGPA:")
    st.dataframe(pd.DataFrame(results))

    st.subheader("🏆 Final CGPA (after 4 Semesters):")
    st.write(f"**{results[-1]['CGPA (Cumulative)']:.2f}**")

    st.caption("Formula: CGPA = Total Grade Points Earned ÷ Total Credit Hours Taken")
