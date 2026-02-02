curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5-nano",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant. Use tools when appropriate."
      },
      {
        "role": "user",
        "content": "What is the current weather in Munich?"
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get the current weather for a city",
          "parameters": {
            "type": "object",
            "properties": {
              "city": {
                "type": "string",
                "description": "Name of the city"
              }
            },
            "required": ["city"]
          }
        }
      }
    ]
  }'
