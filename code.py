import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPA & CGPA Calculator", layout="centered")

st.title("🎓 GPA & CGPA Calculator (4 Semesters)")

st.write("""
This app helps you calculate GPA for each of the 4 semesters and 
the **CGPA (Cumulative GPA) after each semester** using your marks and credit hours.
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
    num_subjects = st.number_input(
        f"Enter number of subjects for Semester {sem}",
        min_value=1, max_value=10, key=f"num_{sem}"
    )
    
    subjects = []
    for i in range(int(num_subjects)):
        st.subheader(f"Subject {i+1}")
        marks = st.number_input(
            f"Enter Marks for Subject {i+1}",
            min_value=0, max_value=100, key=f"marks_{sem}_{i}"
        )
        credits = st.number_input(
            f"Enter Credit Hours for Subject {i+1}",
            min_value=1, max_value=5, key=f"credit_{sem}_{i}"
        )
        subjects.append({"marks": marks, "credits": credits})
    semester_data[sem] = subjects


if st.button("Calculate GPA & CGPA"):
    results = []
    total_points = 0
    total_credits = 0

    for sem in semesters:
        gpa = calculate_gpa(semester_data[sem])
        results.append({"Semester": sem, "GPA": round(gpa, 2)})

        # Add to total for CGPA calculation
        total_points += sum([marks_to_gpa(s['marks']) * s['credits'] for s in semester_data[sem]])
        total_credits += sum([s['credits'] for s in semester_data[sem]])

        cgpa = total_points / total_credits if total_credits > 0 else 0
        results[-1]["CGPA (Cumulative)"] = round(cgpa, 2)

    st.success("✅ Calculation Complete!")
    st.subheader("📊 Semester-wise GPA & Cumulative CGPA:")
    st.dataframe(pd.DataFrame(results))

    st.subheader("🏆 Final CGPA (after 4 Semesters):")
    st.write(f"**{results[-1]['CGPA (Cumulative)']:.2f}**")

    st.caption("Formula: CGPA = Total Grade Points Earned ÷ Total Credit Hours Taken")
