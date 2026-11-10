import streamlit as st
from explainer import explain_stream
from paypal_client import create_test_order, get_order

st.title("Status Pal")
st.write("Understand your PayPal payment status in plain language.")

tab_live, tab_examples = st.tabs(["Live PayPal Sandbox", "Example statuses"])

with tab_live:
    st.write("Creates a real test order in the PayPal Sandbox (fake money) and explains it.")
    live_amount = st.text_input("Amount", value="25.00", key="live_amount")

    if st.button("Create test order and explain"):
        try:
            with st.spinner("Asking PayPal..."):
                order_id = create_test_order(live_amount)
                order = get_order(order_id)

            amount_info = order["purchase_units"][0]["amount"]
            transaction = {
                "order_id": order["id"],
                "status": order["status"],
                "amount": amount_info["value"],
                "currency": amount_info["currency_code"],
                "intent": order.get("intent"),
            }

            with st.expander("What PayPal returned (the data the AI sees)"):
                st.json(transaction)

            st.write_stream(explain_stream(transaction))
        except Exception as e:
            st.error("Could not reach the PayPal Sandbox. Please try again.")
            print("PayPal error:", e)

with tab_examples:
    st.write("Pick an example status. These are typed in, not fetched from PayPal.")
    status = st.selectbox("Payment status", ["PENDING", "ON_HOLD", "DECLINED", "REFUNDED"])
    reason = st.text_input("Reason code (optional)", placeholder="e.g. ECHECK")
    amount = st.text_input("Amount", value="50.00", key="example_amount")

    if st.button("Explain my payment"):
        transaction = {"status": status, "amount": amount, "currency": "USD"}
        if reason:
            transaction["reason"] = reason
        st.write_stream(explain_stream(transaction))