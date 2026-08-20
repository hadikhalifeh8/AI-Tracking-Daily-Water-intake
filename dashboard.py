import streamlit as st
import pandas as pd
from datetime import datetime

from SRC.agent import WaterIntakeAgent
from SRC.database import log_water_intake, get_intake_history


# Initialize session state
if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False


# ============================================================
# Welcome Section
# ============================================================

if not st.session_state.tracker_started:

    st.title("💧 Welcome to the Water Intake Tracker")

    st.markdown("""
    Track your daily hydration with help from an AI Assistant.

    Log your water intake, get smart feedback, and stay healthy effortlessly.
    """)

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()


# ============================================================
# Dashboard
# ============================================================

else:

    st.title("💧 AI Water Intake Dashboard")

    # --------------------------------------------------------
    # Sidebar - Intake Input
    # --------------------------------------------------------

    st.sidebar.header("Log Your Water Intake")

    user_id = st.sidebar.text_input(
        "User ID",
        value="user_1"
    )

    intake_ml = st.sidebar.number_input(
        "Water Intake (ml)",
        min_value=0,
        step=100
    )

    if st.sidebar.button("Submit"):

        if user_id and intake_ml > 0:

            # Save water intake to database
            log_water_intake(
                user_id,
                intake_ml
            )

            st.success(
                f"Logged {intake_ml} ml of water for {user_id}"
            )

            # AI analysis
            agent = WaterIntakeAgent()

            feedback = agent.analyze_intake(
                intake_ml
            )

            st.info(
                f"🤖 AI Feedback: {feedback}"
            )

        else:

            st.warning(
                "Please enter a valid User ID and water intake."
            )


    # --------------------------------------------------------
    # Divider
    # --------------------------------------------------------

    st.markdown("---")


    # ========================================================
    # History Section
    # ========================================================

    st.header("⏮️ Your Water Intake History")

    if user_id:

        history = get_intake_history(user_id)

        if history:

            # history should look like:
            #
            # [
            #     (1500, "2026-08-15"),
            #     (2000, "2026-08-16"),
            #     (1800, "2026-08-17")
            # ]

            dates = [
                datetime.strptime(
                    row[1],
                    "%Y-%m-%d"
                )
                for row in history
            ]

            values = [
                row[0]
                for row in history
            ]


            # Create DataFrame
            df = pd.DataFrame({
                "Date": dates,
                "Water Intake (ml)": values
            })


            # Display table
            st.dataframe(
                df,
                use_container_width=True
            )


            # Display chart
            st.line_chart(
                df,
                x="Date",
                y="Water Intake (ml)"
            )


        else:

            st.warning(
                "No water intake data found for this user. "
                "Please log your intake."
            )