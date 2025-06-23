import streamlit as st

@st.cache_resource
def get_travel_agent():
    from Travel_Agent import TRAVEL_AGENT
    return TRAVEL_AGENT

st.title("AI Travel Planner & Expense Estimator")

with st.form("travel_form"):
    destination = st.text_input("Destination City", "London")
    days = st.number_input("Number of Days", min_value=1, value=5)
    budget = st.number_input("Hotel Budget per Night (USD)", min_value=1, value=100)
    currency = st.text_input("Your Currency", "INR")
    interests = st.text_area("Interests/Preferences", "Local food, public transportation")
    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    st.info("Generating your travel plan. Please wait...")
    agent = get_travel_agent()
    user_input = (
        f"Hi, I want to take a {days}-day trip to {destination} next month. "
        f"My hotel budget is around ${budget} per night. "
        f"I would like to know what the weather will be like, what places I can visit, "
        f"and how much the whole trip might cost. I will be paying in {currency}. "
        f"Also, I prefer {interests}. Can you plan it all for me?"
    )
    output = agent.invoke({"messages": [user_input]})
    final_message = None
    for m in output["messages"]:
        if hasattr(m, "content") and m.content and ("Travel Plan" in m.content or "Itinerary" in m.content):
            final_message = m.content
            break
        if isinstance(m, dict) and "content" in m and m["content"] and ("Travel Plan" in m["content"] or "Itinerary" in m["content"]):
            final_message = m["content"]
            break
    if final_message is None:
        last = output["messages"][-1]
        final_message = getattr(last, "content", str(last))

    st.markdown(final_message)