import time
import matplotlib.pyplot as plt
import sys
import traceback

print("Starting the program...")

try:
    print("Importing modules...")
    questions = [
        {"text": "Hey {name}, do you feel energized when spending time with others?", "trait": "extroversion"},
        {"text": "Do you prefer spending time alone to recharge after social activities?", "trait": "introversion"},
        {"text": "{name}, do you like to make detailed plans before starting a project?", "trait": "conscientiousness"},
        {"text": "Do you often make decisions based on your gut feeling?", "trait": "spontaneity"},
        {"text": "Can you easily understand and share other people's feelings, {name}?", "trait": "empathy"},
        {"text": "Do you prefer making decisions based on facts and data?", "trait": "logic"},
        {"text": "Do you enjoy trying new and different experiences?", "trait": "openness"},
        {"text": "{name}, do you prefer following a regular daily routine?", "trait": "stability"},
        {"text": "Do you remain calm and composed in stressful situations?", "trait": "emotional_stability"},
        {"text": "Do you often feel anxious about future events, {name}?", "trait": "anxiety"}
    ]

    print("Questions defined successfully")

    scores = {
        "extroversion": 0,
        "introversion": 0,
        "conscientiousness": 0,
        "spontaneity": 0,
        "empathy": 0,
        "logic": 0,
        "openness": 0,
        "stability": 0,
        "emotional_stability": 0,
        "anxiety": 0
    }

    print("Scores dictionary created")

    def chatbot_say(message, delay=1):
        print("🤖:", message)
        time.sleep(delay)

    print("Starting the conversation...")
    
    chatbot_say("Hi there! I'm your friendly AI assistant.")
    name = input("👤 What should I call you? ")
    chatbot_say(f"Nice to meet you, {name}! Let's explore your personality together.")
    chatbot_say("Please answer each question with 'yes' or 'no'.\n")

    for q in questions:
        while True:
            try:
                question_text = q["text"].format(name=name)
                chatbot_say(question_text, delay=0.8)
                ans = input("Your answer (yes/no): ").lower().strip()
                if ans in ['yes', 'y']:
                    scores[q["trait"]] += 1
                    chatbot_say("Got it! ✅\n", delay=0.5)
                    break
                elif ans in ['no', 'n']:
                    chatbot_say("Got it! ✅\n", delay=0.5)
                    break
                else:
                    chatbot_say("Please answer with 'yes' or 'no'.")
            except Exception as e:
                chatbot_say("Hmm, something went wrong. Try again!")

    print("All questions answered")

    chatbot_say("Thanks for your answers! Calculating your personality insights... 🧠", delay=2)

    chatbot_say(f"\n🔍 Here's what I learned about you, {name}:")

    if scores["extroversion"] > scores["introversion"]:
        chatbot_say("You're more extroverted — you feel energized around others.")
    else:
        chatbot_say("You're more introverted — you recharge with quiet time.")

    if scores["conscientiousness"] > scores["spontaneity"]:
        chatbot_say("You're a planner who values order and organization.")
    else:
        chatbot_say("You're spontaneous and embrace the moment!")

    if scores["empathy"] > scores["logic"]:
        chatbot_say("You lean toward empathy and emotional understanding.")
    else:
        chatbot_say("You value logic and thoughtful analysis.")

    if scores["openness"] > scores["stability"]:
        chatbot_say("You love new experiences and exploring the unknown.")
    else:
        chatbot_say("You find comfort in routine and structure.")

    if scores["emotional_stability"] > scores["anxiety"]:
        chatbot_say("You handle stress well and stay calm.")
    else:
        chatbot_say("You might experience more anxiety or worry than average.")

    print("Generating graph...")
    chatbot_say("\n📊 Now visualizing your personality traits...")

    plt.figure(figsize=(10, 6))
    plt.bar(scores.keys(), scores.values(), color='skyblue')
    plt.xticks(rotation=45)
    plt.ylabel("Trait Score")
    plt.title(f"{name}'s Personality Trait Graph")
    plt.tight_layout()
    plt.show()

    chatbot_say(f"That's a wrap, {name}! Hope you enjoyed the personality deep dive. 🌟")

except Exception as e:
    print("\nAn error occurred!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nFull error traceback:")
    traceback.print_exc()
    print("\nPlease make sure you have all required packages installed.")
    print("You can install them using: pip install matplotlib")
    input("Press Enter to exit...") 