import streamlit as st
from ApiClient import ApiClient
from auth_libs.Users import check_auth_status
from components.agent_selector import agent_selector
from components.verify_backend import verify_backend
from components.docs import agixt_docs

verify_backend()


st.set_page_config(
    page_title="Tasks",
    page_icon=":bookmark:",
    layout="wide",
)

agixt_docs()
# check_auth_status()


st.title("Manage Tasks")
agent_name = agent_selector()

if agent_name:
    smart_task_toggle = st.checkbox("Enable Smart Task")
    task_objective = st.text_area("Enter the task objective")
    existing_tasks = ApiClient.get_tasks(agent_name=agent_name)
    status = ApiClient.get_task_status(agent_name=agent_name)
    agent_status = "Not Running" if status == False else "Running"
    load_task = st.selectbox(
        "Load Task",
        options=[""] + existing_tasks,
        index=0,
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        columns = st.columns([3, 2])
        if status == False:
            if st.button("Start Task", key=f"start_{agent_name}"):
                if agent_name and (task_objective or load_task):
                    task = ApiClient.start_task_agent(
                        agent_name=agent_name, objective=task_objective
                    )
                    st.experimental_rerun()
                else:
                    columns[0].error("Agent name and task objective are required.")
        else:
            if st.button("Stop Task", key=f"stop_{agent_name}"):
                # This actually toggles to stop it if you try to run while it is running.
                task = ApiClient.start_task_agent(agent_name=agent_name, objective="")
                st.experimental_rerun()

    with col2:
        st.markdown(f"**Status:** {agent_status}")
