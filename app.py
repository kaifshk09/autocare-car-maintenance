import streamlit as st

from logic import calculate_prediction, default_payload, parse_form_data

st.set_page_config(page_title="AutoCare AI", page_icon="🚗", layout="wide")


def render_result(result):
    if not result:
        st.info("Submit the vehicle profile to generate a maintenance risk assessment.")
        return

    score = result["score"]
    tone = result["tone"]
    color = {
        "low": "#2ecc71",
        "medium": "#f39c12",
        "high": "#e74c3c",
    }.get(tone, "#2ecc71")

    st.markdown(f"<div style='padding:1rem 1.2rem; border-radius:12px; background:{color}; color:white; font-weight:700; text-align:center; margin-bottom:1rem;'>Risk Level: {result['level']}</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Maintenance Score", f"{score}/100")
    with col2:
        st.metric("Recommended Window", result["window"])

    st.subheader(result["action"])
    st.write("Recommended checks:")
    for item in result["advice"]:
        st.write(f"- {item}")


def main():
    data = default_payload()

    st.title("AutoCare AI")
    st.caption("Vehicle Maintenance Intelligence")

    with st.container():
        col1, col2 = st.columns([1.2, 1.1])

        with col1:
            st.subheader("Vehicle information")
            age = st.number_input("Car age (years)", min_value=0, max_value=50, value=data["age"])
            mileage = st.number_input("Current mileage (km)", min_value=0, value=data["mileage"])
            service = st.number_input("Distance since last service (km)", min_value=0, value=data["service"])
            fuel = st.selectbox("Fuel / power type", ["Petrol", "Diesel", "Hybrid", "Electric"], index=["Petrol", "Diesel", "Hybrid", "Electric"].index(data["fuel"]))
            usage = st.selectbox("Driving usage", ["Normal", "Moderate", "Heavy"], index=["Normal", "Moderate", "Heavy"].index(data["usage"]))
            warning = st.selectbox("Warning light", ["No", "Yes"], index=["No", "Yes"].index(data["warning"]))
            condition = st.selectbox("Overall condition", ["Good", "Average", "Poor"], index=["Good", "Average", "Poor"].index(data["condition"]))

        with col2:
            st.subheader("Prediction result")
            test_payload = {
                "age": age,
                "mileage": mileage,
                "service": service,
                "fuel": fuel,
                "usage": usage,
                "warning": warning,
                "condition": condition,
            }
            result = calculate_prediction(test_payload)
            render_result(result)

    st.markdown("---")
    st.subheader("System workflow")
    st.write("1. Collect vehicle inputs")
    st.write("2. Calculate weighted risk score")
    st.write("3. Classify low, medium or high maintenance risk")
    st.write("4. Deliver maintenance advice and service guidance")


if __name__ == "__main__":
    main()
