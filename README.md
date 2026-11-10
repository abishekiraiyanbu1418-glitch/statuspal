# Status Pal

An AI assistant that explains PayPal payment statuses in plain language, and is honest about what it doesn't know.

Built for the PayPal AI Hackathon. This is an independent project and not an official PayPal product.

## The problem

Payments show up as "pending", "on hold", or "declined" with little explanation. Users don't know whether to wait, act, or worry, and often end up in support queues.

## What it does

- Reads a payment's status and details.
- Explains in plain language what the status means and what to do next.
- Labels every point as either **Confirmed by data** (literally present in the transaction fields) or **Common cause, not confirmed** (general knowledge).
- Says "I can't tell from this data" when the data doesn't explain the status, instead of guessing.
- Streams the answer so text appears quickly.

## How it works

- **Live PayPal Sandbox tab:** creates a real test order through the PayPal Sandbox REST API (fake money), reads it back, shows the exact data the AI receives, and explains it.
- **Example statuses tab:** a dropdown of statuses (pending, on hold, declined, refunded) with typed-in data. These are examples and are not fetched from PayPal.
- **AI:** Google Gemini, with a system prompt that restricts the model to what the data supports. It tries a fast model first and falls back to a second model if the first is busy.
- **Frontend:** Streamlit.

## Limitations

- The Sandbox mostly produces orders in the `CREATED` state, so held and declined statuses are shown through the example tab.
- The explanations are guidance only. Status Pal cannot see PayPal's internal risk decisions.
- On the free Gemini tier, Google may use submitted content to improve its products, so use only test data.

## Setup

1. Install Python 3.10 or newer.
2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a file named `.env` in the project folder with these three lines, using your own keys:

   ```
   GEMINI_API_KEY=your-gemini-key
   PAYPAL_CLIENT_ID=your-paypal-sandbox-client-id
   PAYPAL_CLIENT_SECRET=your-paypal-sandbox-secret
   ```

   - Gemini key: https://aistudio.google.com (free tier)
   - PayPal Sandbox keys: https://developer.paypal.com (Dashboard, Sandbox, Apps & Credentials)

   Never commit your `.env` file.

4. Run the app:

   ```
   streamlit run app.py
   ```

## Project files

- `app.py`: the Streamlit interface
- `explainer.py`: the Gemini prompt, retry logic, and streaming
- `paypal_client.py`: PayPal Sandbox login, order creation, and order lookup

## License

MIT