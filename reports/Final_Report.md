# Final Report: Fintech Review Analytics

## 1. Executive Summary
This report synthesizes the sentiment and thematic analysis of 1,181 Google Play Store reviews for three major Ethiopian banking applications: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank. The objective is to uncover key satisfaction drivers and prominent pain points to inform actionable product recommendations.

## 2. Insights: Drivers & Pain Points

### Commercial Bank of Ethiopia (CBE)
- **Satisfaction Drivers**:
  - *Accessibility*: High volume of positive reviews mentioning "easy to use" and "convenient" for basic balance checking.
  - *Trust*: Long-term customers frequently express trust in the institution's reliability for large transfers.
- **Pain Points**:
  - *App Performance*: Significant volume of negative sentiment clustered around "crashing during updates" and "slow loading screens."
  - *Account Access*: Users report frequent lockouts and failed OTP deliveries during registration.

### Bank of Abyssinia (BOA)
- **Satisfaction Drivers**:
  - *UI & Design*: The most frequent positive theme for BOA is its modern interface and smooth navigation.
  - *Transaction Speed*: Users highlight fast peer-to-peer transfer speeds compared to competitors.
- **Pain Points**:
  - *Customer Support*: Negative reviews often cite unhelpful branch support when digital issues arise.
  - *Network Errors*: Spikes in negative sentiment correlate with localized network timeout errors during peak hours.

### Dashen Bank
- **Satisfaction Drivers**:
  - *Feature Richness*: High ratings are driven by the diverse "SuperApp" functionality (bill payments, lifestyle services).
  - *Reliable Transfers*: Consistent positive feedback regarding successful inter-bank transfers.
- **Pain Points**:
  - *Complex Navigation*: The abundance of features leads to a steep learning curve; users report struggling to find basic settings.
  - *Fee Transparency*: Negative sentiment surrounds unexpected charges for certain SuperApp micro-transactions.

## 3. Dimensional Comparison

* **Overall Sentiment**: BOA maintains the highest ratio of positive to negative sentiment, driven by strong UI scores. CBE has the highest volume of reviews but a larger proportion of negative sentiment linked to app stability.
* **Average Rating**: The distribution of star ratings mirrors the sentiment scores, with BOA seeing a tighter cluster of 4- and 5-star ratings, while CBE exhibits a bimodal distribution (many 1s and 5s).
* **Dominant Themes**: 
  - *CBE*: Dominated by "App Performance" and "Account Access".
  - *BOA*: Dominated by "UI & Design" and "Transactions".
  - *Dashen*: Dominated by "Transactions" and "Customer Support".

## 4. Product Recommendations

**CBE**:
1.  *Optimize Load Times*: Invest in backend infrastructure to reduce API latency, directly addressing the "slow loading" pain point.
2.  *Revamp OTP Delivery*: Implement an alternative authentication method (e.g., authenticator app integration or WhatsApp OTP) to bypass unreliable SMS delivery.

**BOA**:
1.  *In-App Support Chat*: Implement an integrated AI chatbot or live agent feature to reduce reliance on branch visits for digital issues.
2.  *Offline Mode*: Introduce limited offline functionality (e.g., checking cached balances) to mitigate frustration during network timeouts.

**Dashen Bank**:
1.  *Customizable Dashboard*: Allow users to pin their most-used features to the home screen to simplify navigation within the SuperApp.
2.  *Fee Preview Interface*: Add a mandatory, high-visibility confirmation screen detailing all fees *before* a transaction is executed.

## 5. Visualizations
*(Note: To view the actual generated plots, run `python scripts/visualize.py` in your environment.)*

*   **[Sentiment Distribution]** - A stacked bar chart illustrating the proportion of positive, neutral, and negative sentiment across the three banks.
    *`![Sentiment Distribution](figures/sentiment_distribution.png)`*
*   **[Star Rating Distribution]** - A comparative visualization of star ratings, highlighting the bimodal distribution in older apps.
    *`![Rating Distribution](figures/rating_distribution.png)`*
*   **[Dominant Themes]** - A horizontal bar chart detailing the most frequent conversational themes per bank.
    *`![Theme Frequency](figures/theme_frequency.png)`*
*   **[Sentiment Trend]** - A 7-day rolling average line chart mapping sentiment changes over time.
    *`![Sentiment Trend](figures/sentiment_trend.png)`*

## 6. Ethics and Bias Considerations
When interpreting these results, several critical biases must be acknowledged:
*   **Negativity Bias**: App store reviews inherently skew negative. Users are significantly more motivated to leave a review after a frustrating experience (e.g., a failed transfer) than after a seamless one.
*   **Sampling Bias**: The dataset is limited to the most recent 400 English-language reviews per bank. This excludes users who review in local languages (Amharic, Oromo, etc.) and may not represent the historical sentiment or the entire demographic base.
*   **Digital Divide**: The data only reflects the opinions of smartphone users with reliable internet access, entirely excluding USSD or offline banking customers.
