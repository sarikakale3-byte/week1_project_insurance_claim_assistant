from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from utils.prompt_builder import FEW_SHOT_EXAMPLES, SYSTEM_PROMPT
from utils.model import IntentResult

from utils.tools import (
    classify_intent,
    detect_complaint,
    analyze_sentiment,
    decide_escalation
)

from utils.memory import get_chat_history, append_chat
from utils.memory import redis_client


# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# bind tools (hybrid)
llm_with_tools = llm.bind_tools([
    classify_intent,
    detect_complaint,
    analyze_sentiment,
    decide_escalation
])

# FINAL RESPONSE CHAIN
final_prompt = ChatPromptTemplate.from_template("""
You are a helpful insurance assistant.

Conversation:
{conversation}

User message:
{message}

Intent: {intent}
Sentiment: {sentiment}

Instructions:
- Keep your response SHORT (2–4 lines max)
- Be conversational and friendly
- Answer only what user asked
- Do NOT give long explanations
- Ask one follow-up question if needed
- Avoid bullet points unless necessary

Give a clear and concise response.
""")

parser = StrOutputParser()
final_chain = final_prompt | llm | parser


# HELPER
SHORT_REPLIES = ["yes", "no", "ok", "okay", "yes please", "sure"]

def is_short_reply(msg: str):
    return msg.strip().lower() in SHORT_REPLIES

# CHAT
def chat(session_id: str, message: str) -> str:

    #redis_client.set("debug_test_key", "HELLO_UPSTASH")
    #print("DEBUG WRITE DONE")


    try:
        #Load memory
        history = get_chat_history(session_id)

        history_text = ""
        last_assistant_msg = ""

        for msg in history:
            history_text += f"{msg['role']}: {msg['content']}\n"
            if msg["role"] == "assistant":
                last_assistant_msg = msg["content"]

        # 2.Tool decision (WITH CONTEXT)
        tool_prompt = f"""
You are an insurance assistant.

Conversation:
{history_text}

User message:
{message}

Call tools if needed to analyze intent, sentiment, complaint, escalation.
"""

        response = llm_with_tools.invoke(tool_prompt)

        print("TOOL CALLS:", getattr(response, "tool_calls", None))

        # 3.Execute tools
        tool_outputs = {}

        tool_map = {
            "classify_intent": classify_intent,
            "detect_complaint": detect_complaint,
            "analyze_sentiment": analyze_sentiment,
            "decide_escalation": decide_escalation
        }

        if hasattr(response, "tool_calls") and response.tool_calls:
            for call in response.tool_calls:
                tool_name = call["name"]
                tool_args = call["args"]

                result = tool_map[tool_name].invoke(tool_args)
                tool_outputs[tool_name] = result
        else:
            # fallback: run all tools
            tool_outputs["classify_intent"] = classify_intent.invoke({
                "customer_message": message
            })
            tool_outputs["detect_complaint"] = detect_complaint.invoke({
                "customer_message": message
            })
            tool_outputs["analyze_sentiment"] = analyze_sentiment.invoke({
                "customer_message": message
            })
            tool_outputs["decide_escalation"] = decide_escalation.invoke({
                "customer_message": message
            })


        # 4.Extract values safely
        def safe_val(obj, attr):
            return getattr(obj, attr, str(obj)) if obj else ""

        intent = safe_val(tool_outputs.get("classify_intent"), "intent")
        sentiment = safe_val(tool_outputs.get("analyze_sentiment"), "sentiment")

        # 5.Handle follow-ups
        if is_short_reply(message):
            message_for_llm = f"""
User is replying to previous message.

Previous assistant:
{last_assistant_msg}

User response:
{message}

Continue conversation naturally.
"""
        else:
            message_for_llm = message

    #6.FINAL RESPONSE
        
        bot_reply = final_chain.invoke({
            "conversation": history_text,
            "message": message_for_llm,
            "intent": intent,
            "sentiment": sentiment
        })


        # 7.HARD SAFETY (NO BLANK EVER)
        if not bot_reply or not bot_reply.strip():
            print("EMPTY RESPONSE FIXED")

            fallback = llm.invoke(f"Help user: {message}")
            bot_reply = getattr(fallback, "content", "").strip()

        if not bot_reply:
            bot_reply = "I'm here to help. Could you please tell me more?"

        # 8. Save memory
        append_chat(session_id, "user", message)
        append_chat(session_id, "assistant", bot_reply)

        return bot_reply

    except Exception as e:
        print("ERROR:", str(e))
        return f"Error: {str(e)}"

