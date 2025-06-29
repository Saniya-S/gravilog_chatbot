# GraviLog Chatbot
This is a proactive AI-powered chatbot that helps expectant mothers understand their symptoms and assess potential pregnancy risks. The bot asks focused questions, uses a retrieval-augmented generation (RAG) approach to pull insights from a trusted knowledge base, and provides a structured risk level with suggestions.

## Problem Description
Many expectant mothers experience symptoms that can feel concerning but may not always require urgent care. GraviLog Bot aims to help by proactively triaging the situation through simple symptom-related questions, retrieving relevant information from trusted medical resources, and returning a clear risk assessment in a supportive, easy-to-understand manner.

The medical knowledge used to run this application is entirely from the official knowledge base provided by the GraviLog team.

## System Architecture
The chatbot is built using a straightforward RAG workflow:

1. Proactive Symptom Collection: The chatbot asks short questions about the user’s current symptoms.

2. RAG Backend: User responses are processed through LlamaIndex, which searches the indexed medical documents.

3. LLM Output: The relevant context is sent to Cohere’s LLM to generate a structured risk assessment.

4. Frontend: The conversation and results are displayed in an interactive Streamlit app.

## Example Queries and Outputs

The chatbot proactively asks a total of 11 questions. Apart from the first question, the order is shuffled for each session. Below is an example scenario with sample responses:

``` 
1. Can you tell me how many weeks pregnant you are right now? An estimate is fine if you’re not certain.

32 weeks

2. Do you feel any pressure or pain in your pelvic area?

I do not feel any pressure

3. Have you noticed sudden swelling in your hands, feet, or face?

Yes, in my feet and hands

4. Have you noticed any discharge with a bad or unusual smell?

None

5. Do you have pain in your lower back?

None

6. Have you had a fever recently?

Nope

7. Do you feel dizzy, faint, or lightheaded?

A slight lightheadedness

8. Are you experiencing any changes in your vision, like blurriness or spots?

No I am not

9. How does your baby’s movement today feel compared to yesterday? More, less, or about the same?

Less active than usual

10. Have you had any headaches that won’t go away?

Yes, since yesterday

11. Are you currently experiencing any unusual bleeding or spotting?

no

```

**Sample Structured Risk Assessment Output**

```
Risk Level: High 🔴

Explanation:
You are experiencing symptoms that could indicate preeclampsia and fetal distress, which are serious conditions. These symptoms include swelling in your hands and feet, a persistent headache, and reduced fetal movement. This combination of symptoms warrants immediate medical attention.
Suggestions:

    - Contact your healthcare provider or obstetrician right away. Describe your symptoms and concerns, especially the reduced fetal movement, persistent headache, and swelling.

    - Keep track of fetal movements and note any changes. This will help your healthcare provider assess the situation.

    - Stay hydrated and rest as much as possible. These measures can help manage symptoms and support your overall well-being.

Additional Notes

Remember, seeking medical attention is crucial to ensure the safety of both you and your baby. Your healthcare provider will assess your symptoms and provide appropriate guidance and care. Don't hesitate to reach out for support and advice.
```

The bot also supports simple follow-up questions, for example:
- “Why should I stay hydrated?”

- “What should I do if I feel dizzy later?”


**Example Follow-up**

If you ask:
```
What do you mean it could indicate preeclampsia?
```
The bot responds:
```
Preeclampsia is a pregnancy complication characterized by high blood pressure and signs of damage to other organs, often the kidneys. The symptoms you're experiencing, like swelling, headaches, and changes in fetal movement, can be indicators of this condition. It's a serious concern as it can affect both you and your baby's health. That's why it's crucial to get checked by your doctor as soon as possible. They will be able to monitor your blood pressure and run some tests to determine if you have preeclampsia and provide the necessary treatment.
```

*Note: All outputs shown here are actual responses from the GraviLog Bot*

## Additional Features
1. **Reset Button**: 
Users can clear their session at any point to restart the triage process with a fresh conversation.

2. **Simple Follow-up Capabilities**: After the initial risk assessment, users can ask follow-up questions to clarify any details or concerns.

## Instructions to Run Locally

1. Clone the Repository
```bash
git clone https://github.com/Saniya-S/gravilog_chatbot.git
cd gravilog_chatbot
```

2. Create a new Conda environment
```bash
conda create -n gravilog-env python=3.12.9
```
3. Activate the environment
```bash
conda activate gravilog-env
```
4. Install dependencies
```bash
pip install -r requirements.txt
```
5. Run the app
```bash
streamlit run ui_interface.py
```
5. Access the app
Open the local URL that Streamlit shows in your terminal


## Deployment Steps

1. Push your code to a public GitHub repository.

2. Create an account on a free hosting platform such as Streamlit Cloud.

3. Connect your repository and deploy the app directly.

4. Ensure your .env or secrets are configured securely.

5. Share your public URL.

## Notes

- The entire medical content powering this bot comes from GraviLog’s provided knowledge base.

- This is not a substitute for medical advice. Users should always consult their healthcare provider for urgent concerns.