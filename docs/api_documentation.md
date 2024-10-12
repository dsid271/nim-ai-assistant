# NIM AI Assistant API Documentation

## Endpoints

### POST /chat

Send a message to the AI assistant and receive a response.

Request body:
```json
{
  "message": "string"
}
```

Response body:
```json
{
  "response": "string"
}
```

### POST /finetune

Fine-tune the model with a custom dataset.

Request body:
```json
{
  "dataset": [
    {
      "input": "string",
      "output": "string"
    }
  ]
}
```

Response body:
```json
{
  "message": "string"
}
```

### POST /few-shot

Generate a response using few-shot learning.

Request body:
```json
{
  "prompt": "string",
  "examples": [
    {
      "input": "string",
      "output": "string"
    }
  ]
}
```

Response body:
```json
{
  "response": "string"
}
```

## Error Handling

All endpoints may return a 500 Internal Server Error with a detail message if an exception occurs during processing.
