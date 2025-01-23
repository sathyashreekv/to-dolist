import streamlit as st

# Initialize session state
if "task_lists" not in st.session_state:
    st.session_state.task_lists = {"Default": []}
if "editing_task" not in st.session_state:
    st.session_state.editing_task = None  # To track the task being edited

# Sidebar for list selection and creation
st.sidebar.title("📂 Task Lists")
list_names = list(st.session_state.task_lists.keys())
selected_list = st.sidebar.selectbox("Select a list", list_names)

# Add a new list
with st.sidebar.form("Add List"):
    new_list_name = st.text_input("New list name", "")
    submitted_list = st.form_submit_button("Create List")
    if submitted_list and new_list_name.strip():
        if new_list_name.strip() not in st.session_state.task_lists:
            st.session_state.task_lists[new_list_name.strip()] = []
            st.success(f"List '{new_list_name.strip()}' created!")
        else:
            st.warning(f"List '{new_list_name.strip()}' already exists!")

# Title
st.title(f"📝 To-Do List: {selected_list}")

# Input form for new tasks
with st.form("Add Task"):
    new_task = st.text_input("Enter a task", "")
    due_date = st.date_input("Due date (optional)")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    submitted_task = st.form_submit_button("Add Task")
    if submitted_task and new_task.strip():
        st.session_state.task_lists[selected_list].append(
            {"task": new_task.strip(), "due_date": due_date, "priority": priority}
        )
        st.success(f"Task added to '{selected_list}'!")

# Display tasks
st.subheader(f"Tasks in '{selected_list}':")
if st.session_state.task_lists[selected_list]:
    for i, task in enumerate(st.session_state.task_lists[selected_list]):
        if st.session_state.editing_task == i:
            # Edit form
            with st.form(f"Edit Task {i}"):
                edited_task = st.text_input("Edit task", task["task"])
                edited_due_date = st.date_input("Edit due date", task["due_date"])
                edited_priority = st.selectbox(
                    "Edit priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task["priority"])
                )
                submitted_edit = st.form_submit_button("Save Changes")
                cancel_edit = st.form_submit_button("Cancel")
                if submitted_edit:
                    st.session_state.task_lists[selected_list][i] = {
                        "task": edited_task.strip(),
                        "due_date": edited_due_date,
                        "priority": edited_priority,
                    }
                    st.success("Task updated successfully!")
                    st.session_state.editing_task = None  # Reset editing state
                    st.rerun()
                if cancel_edit:
                    st.session_state.editing_task = None  # Cancel editing
                    st.rerun()
        else:
            # Display task
            col1, col2, col3, col4 = st.columns([0.6, 0.6, 0.6, 0.6])
            with col1:
                st.write(f"{i + 1}. {task['task']} (Due: {task['due_date']}, Priority: {task['priority']})")
            with col2:
                if st.button("Edit", key=f"edit_{selected_list}_{i}"):
                    st.session_state.editing_task = i  # Set the task being edited
                    st.rerun()
            with col3:
                if st.button("Remove", key=f"remove_{selected_list}_{i}"):
                    st.session_state.task_lists[selected_list].pop(i)
                    st.rerun()
            with col4:
                if st.checkbox("Done", key=f"done_{selected_list}_{i}"):
                    task["task"] = f"~~{task['task']}~~ (Done)"
                    st.rerun()
else:
    st.info("No tasks yet! Add one above.")

# Clear all tasks in the current list
if st.button(f"Clear All Tasks in '{selected_list}'"):
    st.session_state.task_lists[selected_list] = []
    st.success(f"All tasks in '{selected_list}' cleared!")

# Delete a list
if selected_list != "Default":
    if st.sidebar.button(f"Delete '{selected_list}'"):
        del st.session_state.task_lists[selected_list]
        st.rerun()
