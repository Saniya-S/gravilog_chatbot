import streamlit as st
import random
from main import get_structured_response

st.title("GraviLog Bot")
st.subheader("Let our bot triage your situation!")
st.divider()

#List of proactive questions
questions = [
    "Are you currently experiencing any unusual bleeding or spotting?",
    "How does your baby’s movement today feel compared to yesterday? More, less, or about the same?",
    "Have you had any headaches that won’t go away?",
    "Are you experiencing any changes in your vision, like blurriness or spots?",
    "Do you feel any pressure or pain in your pelvic area?",
    "Do you have pain in your lower back?",
    "Have you had a fever recently?",
    "Have you noticed any discharge with a bad or unusual smell?",
    "Have you noticed sudden swelling in your hands, feet, or face?",
    "Do you feel dizzy, faint, or lightheaded?"
]

# Function to display the risk assessment
def display_risk_assessment(report):
    
    with st.chat_message("assistant"):
        risk_level= report["risk_level"]
        risk_color= "🟢" if risk_level == "Low" else "🟡" if risk_level == "Medium" else "🔴"
        st.header(f"Risk Level: {risk_level} {risk_color}") 
        st.divider()

        st.subheader("Explanation:")        
        st.markdown(report["explanation"])

        st.subheader("Suggestions:")
        for s in report["suggestions"]:      
            st.markdown(f"- {s}") 
        st.divider()
        st.markdown("**Additional Notes**")  
        st.markdown(report["additional_notes"])

# initialise follow-up chat history for llm
if "follow_up_message" not in st.session_state:
    st.session_state.follow_up_message= []

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialise responses (Track responses)
if "responses" not in st.session_state:
    st.session_state.responses = []

# Initialise questions (Track asked question)
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = []

# Initialise has_analysed
if "has_analysed" not in st.session_state:
    st.session_state.has_analysed = False

# Initialise risk_analysis
if "risk_analysis" not in st.session_state:
    st.session_state.risk_analysis= {}

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["content"] == "risk_assessment":
        report_dict= {"risk_level": message["risk_level"], "explanation": message["explanation"], "suggestions": message["suggestions"], "additional_notes": message["additional_notes"]}
        display_risk_assessment(report_dict)
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



# Loading message
loading_message= "Thank you for answering the question. I will not triage the situation. Please wait..."

# Intitialise pending_question (run only once)
if "pending_question" not in st.session_state:
    st.session_state.pending_question = random.choice(questions)

    # Add instruction to the user
    intruction= """I’ll ask you a few short questions to understand how you’re feeling. Please answer in a sentence or two
                 — the more details you share, the better I can help."""
    # Display
    with st.chat_message("assistant"):
        st.markdown(f"*{intruction}*")
    # Add to chat history
    st.session_state.messages.append({"role":"assistant", "content": f"*{intruction}*"})

if st.session_state.pending_question:
    with st.chat_message("assistant"):
        st.markdown(st.session_state.pending_question)

if input := st.chat_input("Your response"):
    if st.session_state.pending_question:
        # Save the question and input in messages
        st.session_state.messages.append({"role":"assistant", "content": st.session_state.pending_question})
        st.session_state.messages.append({"role":"user", "content": input})

        #Save the input into responses
        st.session_state.responses.append({st.session_state.pending_question:input})

        #Display user input
        with st.chat_message("user"):
            st.markdown(input)
        
        # mark the pending_question as asked
        st.session_state.asked_questions.append(st.session_state.pending_question)

    # Remaining questions
    remaining_questions= [q for q in questions if q not in st.session_state.asked_questions]
    if remaining_questions:
        next_question= random.choice(remaining_questions) if remaining_questions else None
        st.session_state.pending_question = next_question
        st.rerun()
    else:
        if st.session_state.has_analysed == False:
            st.session_state.messages.append({"role":"assistant", "content": loading_message})
            # Change the session variable to None
            st.session_state.pending_question= None

            # Display loading message
            with st.chat_message("assistant"):
                st.markdown(loading_message) 

            
            # Convert the user_response into a single string
            user_report= "\n".join([f"{a} {b}" for question in st.session_state.responses for a, b in question.items()])
            # Getting structured risk assessment
            risk_assesment= get_structured_response(user_input=user_report, use_structure= True)

            # Save the risk_assesment to risk_analysis session variable
            st.session_state.risk_analysis= risk_assesment

            # Display the risk report
            display_risk_assessment(risk_assesment)
                

            # Append the risk assessment to the messages session variable
            st.session_state.messages.append({"role":"assistant", "content": "risk_assessment", "risk_level": risk_assesment["risk_level"],
                                            "explanation": risk_assesment["explanation"], "suggestions": risk_assesment["suggestions"],
                                            "additional_notes": risk_assesment["additional_notes"] })

                 
            st.session_state.has_analysed= True
        else:
            # Append the follow-up question by the user in chat history (for display on UI)
            st.session_state.messages.append({"role":"user", "content": input})  

            # Display to the user
            with st.chat_message("user"):
                st.markdown(input)

            # Convert the risk_analysis dict into a single string
            context_str= "\n".join([f"{a}:{b}," for a,b in st.session_state.risk_analysis.items()])

            # Concatenate only if there is past follow-up msgs
            if len(st.session_state.follow_up_message) > 0:
                context_str += "\n".join([f"{a}:{b}," for message in st.session_state.follow_up_message for a,b in message.items()])

            # Send the follow-up question from the user to the LLM
            llm_response= get_structured_response(user_input=input, context=context_str)

            # Append the follow-up question by the user in the follow-up (for context for LLM)
            st.session_state.follow_up_message.append({"role":"user", "content": input})
            print("")

             # Append the response by the LLM in the follow-up (for context for LLM)
            st.session_state.follow_up_message.append({"role":"assistant", "content": llm_response})
            
            # Append the LLM response to the session variable messages
            st.session_state.messages.append({"role":"assistant", "content": llm_response})

            # Display the LLM response to the user
            with st.chat_message("assistant"):
                st.markdown(llm_response)
            




    

    








