import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def calculate_priority(task_data):
    points = 0
    if task_data['grade_type'] == "Perform Grade":
        points = 36
    elif task_data['grade_type'] == "Rehearse Grade":
        points = 30
    elif task_data['grade_type'] == "Prepare Grade":
        points = 15

    due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d')
    days_until_due = (due_date - datetime.now()).days
    points += max(0, 50 - days_until_due)

    return points

def load_data_from_txt_file(file_path):
    tasks = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            task_data = eval(line.strip())
            tasks.append(task_data)
    return tasks

def main():
    st.title("🏫 📅 School Work Scheduling App")

    file_path = st.text_input("Enter the path to the .txt file:")
    if st.button("Load Data"):
        try:
            tasks = load_data_from_txt_file(file_path)
            st.session_state.tasks = tasks
            st.success("Data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading data: {e}")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    save_data = st.checkbox("Save Data to File")
    if save_data:
        with open("saved_tasks.txt", "w") as file:
            for task_data in st.session_state.tasks:
                file.write(str(task_data) + "\n")
        st.success("Data saved to file 'saved_tasks.txt'")

    tasks = st.text_input("Enter a task:")
    subject = st.selectbox("Select the subject:", ["Math", "Science", "History", "Language"])
    grade_type = st.radio("Select grade type:", ["Perform Grade", "Rehearse Grade", "Prepare Grade"])
    due_date = st.date_input("Select the due date:")

    if st.button("Add Task"):
        task_data = {
            "task": tasks,
            "subject": subject,
            "grade_type": grade_type,
            "due_date": due_date.strftime('%Y-%m-%d'),
            "completed": False
        }
        st.session_state.tasks.append(task_data)
        st.success("Task added!")

    if st.button("Clear All Tasks"):
        st.session_state.tasks = []
        st.info("All tasks cleared!")

    st.write("## Task List")

    if len(st.session_state.tasks) == 0:
        st.warning("No work to do.")
    else:
        task_table = []
        for i, task_data in enumerate(st.session_state.tasks):
            task_data['priority'] = calculate_priority(task_data)
            task_table.append(task_data)

        sorted_tasks = sorted(task_table, key=lambda x: x['priority'], reverse=True)
        df = pd.DataFrame(sorted_tasks, columns=["task", "subject", "grade_type", "due_date", "completed", "priority"])

        st.dataframe(df)

        for i, row in df.iterrows():
            completed = st.checkbox(f"Complete '{row['task']}'", key=f"checkbox_{i}")
            if completed:
                st.session_state.tasks[i]['completed'] = True

        if len(st.session_state.tasks) > 0:
            task_to_delete = st.number_input("Enter the index of completed task to delete:", min_value=0, max_value=len(st.session_state.tasks)-1)
            if st.button("Delete Completed Task"):
                if 0 <= task_to_delete < len(st.session_state.tasks):
                    st.session_state.tasks.pop(task_to_delete)
                    st.info("Task deleted!")

if __name__ == "__main__":
    main()
