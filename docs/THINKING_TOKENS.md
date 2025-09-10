# Chat Text Formatting and Thinking Tokens Management

This document explains how Open WebUI handles chat text formatting and thinking tokens (reasoning content) from AI models.

## Overview

Open WebUI automatically detects and formats "thinking" or "reasoning" content from AI models, displaying it as collapsible sections in the chat interface. This allows users to see the model's reasoning process without cluttering the main response.

## Architecture

### Backend Components

#### 1. Middleware Processing (`backend/open_webui/utils/middleware.py`)

The core thinking token processing happens in the middleware layer:

**Default Reasoning Tags** (Lines 114-123):
```python
DEFAULT_REASONING_TAGS = [
    ("<think>", "</think>"),
    ("<thinking>", "</thinking>"),
    ("<reason>", "</reason>"),
    ("<reasoning>", "</reasoning>"),
    ("<thought>", "</thought>"),
    ("<Thought>", "</Thought>"),
    ("<|begin_of_thought|>", "<|end_of_thought|>"),
    ("◁think▷", "◁/think▷"),
]
```

**Content Processing Flow**:
1. **Detection**: The middleware scans streaming responses for reasoning tags
2. **Block Creation**: Creates structured content blocks with type "reasoning"
3. **HTML Generation**: Converts blocks to HTML `<details>` tags with special attributes
4. **Display**: Frontend renders as collapsible sections

#### 2. Response Processing (`backend/open_webui/utils/response.py`)

Handles the extraction of thinking content from model responses:
- Line 85: `reasoning_content = ollama_response.get("message", {}).get("thinking", None)`
- Line 108: `reasoning_content = data.get("message", {}).get("thinking", None)`

### Frontend Components

#### 1. Content Renderer (`src/lib/components/chat/Messages/ContentRenderer.svelte`)

Main component that orchestrates content rendering:
- Integrates with the Markdown component
- Handles floating buttons and user interactions
- Manages content container and event handling

#### 2. Markdown Processing (`src/lib/components/chat/Messages/Markdown.svelte`)

Processes markdown content using marked.js with custom extensions:
- Uses `processResponseContent()` to clean and format content
- Applies token replacements for dynamic content
- Renders markdown tokens through `MarkdownTokens.svelte`

#### 3. Utility Functions (`src/lib/utils/index.ts`)

Key utility functions for content processing:

```typescript
// Main content processing
export const processResponseContent = (content: string) => {
    content = processChineseContent(content);
    return content.trim();
};

// Remove specific detail types
export const removeDetails = (content, types) => {
    for (const type of types) {
        content = content.replace(
            new RegExp(`<details\\s+type="${type}"[^>]*>.*?<\\/details>`, 'gis'),
            ''
        );
    }
    return content;
};

// Remove all detail tags
export const removeAllDetails = (content) => {
    content = content.replace(/<details[^>]*>.*?<\/details>/gis, '');
    return content;
};

// Process and convert detail tags
export const processDetails = (content) => {
    content = removeDetails(content, ['reasoning', 'code_interpreter']);
    // Additional processing for tool_calls...
    return content;
};
```

## How Thinking Tokens Work

### 1. Model Response Processing

When a model includes thinking content:

```
<thinking>
Let me analyze this step by step:
1. The user is asking about X
2. I need to consider Y
3. The best approach would be Z
</thinking>

Based on my analysis, here's the answer...
```

### 2. Backend Processing

The middleware:
1. Detects the `<thinking>` tags
2. Creates a content block:
```python
{
    "type": "reasoning",
    "start_tag": "<thinking>",
    "end_tag": "</thinking>",
    "content": "Let me analyze this step by step...",
    "started_at": timestamp,
    "ended_at": timestamp,
    "duration": calculated_duration
}
```

3. Converts to HTML:
```html
<details type="reasoning" done="true" duration="2">
<summary>Thought for 2 seconds</summary>
> Let me analyze this step by step:
> 1. The user is asking about X
> 2. I need to consider Y  
> 3. The best approach would be Z
</details>
```

### 3. Frontend Rendering

The frontend:
1. Processes the HTML details tags
2. Renders them as collapsible sections
3. Shows duration and thinking indicators
4. Allows users to expand/collapse reasoning

## Configuration

### Enabling/Disabling Reasoning Detection

Reasoning detection can be controlled via parameters:

```python
# In form_data params
"reasoning_tags": [["<think>", "</think>"]]  # Custom tags
"reasoning_tags": False  # Disable detection
```

### Custom Reasoning Tags

You can define custom reasoning tags:

```python
reasoning_tags = [
    ("<my_thinking>", "</my_thinking>"),
    ("◁reasoning▷", "◁/reasoning▷")
]
```

## Examples

### Basic Thinking Token

**Input from Model**:
```
<thinking>
The user wants me to explain quantum computing. I should start with the basics and build up to more complex concepts.
</thinking>

Quantum computing is a revolutionary approach to computation...
```

**Rendered Output**:
- Collapsible section: "Thought for 1 second"
- Main response: "Quantum computing is a revolutionary approach..."

### Multiple Reasoning Sections

**Input**:
```
<thinking>Initial analysis...</thinking>
Here's my first point.

<reasoning>Let me think about the implications...</reasoning>
And here's the deeper analysis.
```

**Result**: Two separate collapsible reasoning sections with the main content flowing between them.

### Streaming Reasoning

For streaming responses, reasoning content is built up incrementally and duration is calculated from start to finish.

## Troubleshooting

### Common Issues

1. **Reasoning tags not detected**: Check that tags match `DEFAULT_REASONING_TAGS`
2. **Content not collapsing**: Verify HTML structure and CSS
3. **Duration not showing**: Ensure timing calculations are working

### Debugging

Enable debug logging to see reasoning detection:
```python
log.debug(f"Reasoning block: {reasoning_block}")
```

## Development Guidelines

### Adding New Reasoning Tag Types

1. Add to `DEFAULT_REASONING_TAGS` in middleware.py
2. Test with various models and content types
3. Update documentation with examples

### Customizing Display

1. Modify HTML generation in middleware.py
2. Update CSS/styling in frontend components
3. Consider accessibility and mobile display

### Testing

Create test cases that cover:
- Single and multiple reasoning sections
- Nested content and edge cases
- Streaming and non-streaming responses
- Custom tag configurations

## Future Enhancements

Potential improvements:
- Visual indicators for reasoning quality/confidence
- Syntax highlighting within reasoning blocks
- User preferences for auto-expand/collapse
- Export functionality for reasoning content
- Integration with model evaluation metrics