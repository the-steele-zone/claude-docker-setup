#!/usr/bin/env python3
"""
Claude Docker Application
Example application for running Claude with Docker
"""

import os
from anthropic import Anthropic

def main():
      """Main application entry point"""
      # Initialize Anthropic client
      api_key = os.environ.get("ANTHROPIC_API_KEY")
      if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")

      client = Anthropic(api_key=api_key)

    print("=== Claude Docker Application ===")
    print("Type your message and press Enter (type 'exit' to quit)\n")

    conversation_history = []

    while True:
              # Get user input
              user_input = input("You: ").strip()

        if user_input.lower() == 'exit':
                      print("Goodbye!")
                      break

        if not user_input:
                      continue

        # Add user message to history
        conversation_history.append({
                      "role": "user",
                      "content": user_input
        })

        # Call Claude API
        try:
                      response = client.messages.create(
                                        model="claude-sonnet-4-5-20250929",
                                        max_tokens=1024,
                                        messages=conversation_history
                      )

            # Extract and display response
                      assistant_message = response.content[0].text
                      print(f"\nClaude: {assistant_message}\n")

            # Add assistant message to history
                      conversation_history.append({
                          "role": "assistant",
                          "content": assistant_message
                      })

except Exception as e:
              print(f"Error: {e}")
              # Remove the last user message if API call failed
              conversation_history.pop()

if __name__ == "__main__":
      main()
