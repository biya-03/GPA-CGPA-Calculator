import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPA & CGPA Calculator", layout="centered")

st.title("🎓 GPA & CGPA Calculator (4 Semesters)")

st.write("""
This app helps you calculate GPA for each of the 4 semesters and 
the **CGPA up to the 3rd semester** using your marks and credit hours.
""")

# Grade scale function
def marks_to_gpa(marks):
    if marks >= 85:
        return 4.0
    elif marks >= 80:
        return 3.7
    elif marks >= 75:
        return 3.3
    elif marks >= 70:
        return 3.0
    elif marks >= 65:
        return 2.7
    elif marks >= 61:
        return 2.3
    elif marks >= 58:
        return 2.0
    elif marks >= 55:
        return 1.7
    elif marks >= 50:
        return 1.0
    else:
        return 0.0


# GPA calculation
def calculate_gpa(subjects):
    total_points = sum([marks_to_gpa(s['marks']) * s['credits'] for s in subjects])
    total_credits = sum([s['credits'] for s in subjects])
    return total_points / total_credits if total_credits > 0 else 0


# Main input section
semesters = [1, 2, 3, 4]
semester_data = {}

for sem in semesters:
    st.header(f"📘 Semester {sem}")
    num_subjects = st.number_input(f"Enter number of subjects for Semester {sem}", min_value=1, max_value=10, key=f"num_{sem}")
    
    subjects = []
    for i in range(int(num_subjects)):
        st.subheader(f"Subject {i+1}")
        name = st.text_input(f"Name of Subject {i+1}", key=f"name_{sem}_{i}")
        marks = st.number_input(f"Enter Marks for {name or f'Subject {i+1}'}", min_value=0, max_value=100, key=f"marks_{sem}_{i}")
        credits = st.number_input(f"Enter Credit Hours for {name or f'Subject {i+1}'}", min_value=1, max_value=5, key=f"credit_{sem}_{i}")
        subjects.append({"name": name, "marks": marks, "credits": credits})
    semester_data[sem] = subjects


if st.button("Calculate GPA & CGPA"):
    results = []
    total_points = 0
    total_credits = 0

    for sem in semesters:
        gpa = calculate_gpa(semester_data[sem])
        results.append({"Semester": sem, "GPA": round(gpa, 2)})
        if sem <= 3:
            total_points += sum([marks_to_gpa(s['marks']) * s['credits'] for s in semester_data[sem]])
            total_credits += sum([s['credits'] for s in semester_data[sem]])

    cgpa_3 = total_points / total_credits if total_credits > 0 else 0

    st.success("✅ Calculation Complete!")
    st.subheader("📊 Semester-wise GPA:")
    st.dataframe(pd.DataFrame(results))

    st.subheader("🏆 CGPA (up to 3rd Semester):")
    st.write(f"**{cgpa_3:.2f}**")

    st.caption("Formula: CGPA = Total Grade Points Earned ÷ Total Credit Hours Taken")
