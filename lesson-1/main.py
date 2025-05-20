"""
Main script to run the agent manually
"""
from dotenv import load_dotenv

_ = load_dotenv()

from src.agent import Agent
from src.prompt import prompt
from src.actions import average_dog_weight

agent = Agent(prompt)

while True:
  try:
    user_input = input("User: ")
    
    if user_input.strip().lower() == "exit":
      break
    elif user_input.strip() == "1":
      result = agent("How much does a Bulldog weigh?")

      print("Assistant:", result)

      next_prompt = "Observation: {}".format(result)

      next_result = agent(next_prompt)

      print("Finally:", next_result)
    elif user_input.strip() == "2":
      result = agent("""I have 2 dogs, a border collie and a scottish terrier. What is their combined weight?""")

      print("Assistant:", result)

      next_prompt = "Observation: {}".format(average_dog_weight("Border Collie"))

      next_result = agent(next_prompt)

      print(next_result)

      next_prompt = "Observation: {}".format(average_dog_weight("Scottish Terrier"))

      next_result = agent(next_prompt)

      print(next_result)

      next_prompt = "Observation: {}".format(eval("37 + 20"))

      last_result = agent(next_prompt)

      print("Finally:", last_result)
    
    print(f"\nMessages:\n{agent.messages}")
  except KeyboardInterrupt:
    break
