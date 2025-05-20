"""
The same script as main.py but to run automatically
"""
from src.agent import query


if __name__ == "__main__":
  question = """I have 2 dogs, a border collie and a scottish terrier. What is their combined weight?"""

  query(question)