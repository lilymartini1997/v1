# Gemini LLM Support

This repository now supports Google's Gemini LLM via the `google-generativeai` package.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install google-generativeai
    ```

2.  **Get an API Key:**
    Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/).

## Usage

You can run the campaign using Gemini by specifying the provider and your API key.

### Basic Usage (Uses Gemini 3 Pro Preview by default)

```bash
python main.py --mode CREATE_CAMPAIGN --input_file your_input.json \
  --llm_provider gemini \
  --gemini_api_key YOUR_API_KEY
```

### Specifying a Model

You can choose a different model (e.g., for cheaper testing) using the `--model` flag.

**For Testing (Cheapest):**
```bash
python main.py --mode CREATE_CAMPAIGN --input_file your_input.json \
  --llm_provider gemini \
  --gemini_api_key YOUR_API_KEY \
  --model gemini-2.0-flash
```

**Supported Models (Verified):**
- `gemini-3-pro-preview` (Default, High Quality)
- `gemini-2.0-flash` (Fast/Cheap)
- `gemini-flash-latest`
- `gemini-pro-latest`

*Note: `gemini-1.5-pro` appears to be unavailable in the current API environment.*

## Testing

A test script `test_gemini_workflow.py` is included to verify the integration.

```bash
export GEMINI_API_KEY=your_key_here
python test_gemini_workflow.py
```

*Note: If you encounter 429 Quota Exceeded errors, the system will automatically retry a few times. If it persists, you may have exhausted your free tier quota.*
