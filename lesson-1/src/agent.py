from openai import OpenAI
import re
from src.prompt import prompt
from src.actions import known_actions


client = OpenAI()


class Agent:
  """
  Agent class
  """
  def __init__(self, system=""):
    self.system = system
    self.messages = []

    if self.system:
      self.messages.append({"role": "system", "content": system})
  
  def __call__(self, message):
    self.messages.append({"role": "user", "content": message})
    
    result = self.execute()
    
    self.messages.append({"role": "assistant", "content": result})
    
    return result
  
  def execute(self):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      temperature=0,
      messages=self.messages
    )
    
    return completion.choices[0].message.content


def query(question: str, max_turns: int = 5):
  """
  Query the agent with a question and run actions
  """
  action_re = re.compile(r"^Action: (\w+): (.*)$")

  i = 0

  agent = Agent(prompt)

  next_prompt = question

  print("User question:", question)

  while i < max_turns:
    i += 1

    result = agent(next_prompt)

    print(result)

    actions = [
      action_re.match(a)
      for a in result.split("\n")
      if action_re.match(a)
    ]

    if actions:
      # There is an action to run
      action_name, action_input = actions[0].groups()

      if action_name not in known_actions:
        raise Exception("Unknown action: {}: {}".format(action_name, action_input))

      print("Running action: {} with input: {}".format(action_name, action_input))

      # call the action
      observation = known_actions[action_name](action_input)

      print("Observation:", observation)

      next_prompt = "Observation: {}".format(observation)
    else:
      return