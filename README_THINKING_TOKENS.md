# Chat Text Formatting and Thinking Tokens - Code Location Guide

This README provides a quick reference for developers looking to understand where the code for chat text formatting and thinking tokens is located in the Open WebUI codebase.

## 🗂️ File Structure Overview

```
open-webui/
├── backend/
│   └── open_webui/
│       └── utils/
│           ├── middleware.py          # 🧠 Core thinking token processing
│           └── response.py            # 📥 Response handling utilities
├── src/
│   └── lib/
│       ├── components/
│       │   └── chat/
│       │       ├── Messages/
│       │       │   ├── ContentRenderer.svelte  # 🎨 Main content rendering
│       │       │   ├── Markdown.svelte         # 📝 Markdown processing
│       │       │   └── Markdown/
│       │       │       └── MarkdownTokens.svelte  # 🔤 Token rendering
│       │       └── Messages.svelte              # 💬 Message container
│       └── utils/
│           └── index.ts               # 🛠️ Content processing utilities
├── docs/
│   └── THINKING_TOKENS.md            # 📚 Comprehensive documentation
├── test_thinking_tokens.py           # 🧪 Test suite
├── thinking_tokens_demo.py           # 🎮 Interactive demo
└── README_THINKING_TOKENS.md         # 📖 This file
```

## 🎯 Key Components

### Backend (Python)

#### 1. `backend/open_webui/utils/middleware.py`
**The heart of thinking token processing**

- **Lines 114-123**: `DEFAULT_REASONING_TAGS` - Defines supported thinking tags
- **Lines 1920-1940**: Reasoning content detection in streaming responses
- **Lines 1605-1632**: HTML generation for reasoning blocks
- **Lines 2120-2170**: Real-time processing of reasoning content

```python
DEFAULT_REASONING_TAGS = [
    ("<think>", "</think>"),
    ("<thinking>", "</thinking>"),
    # ... more tags
]
```

#### 2. `backend/open_webui/utils/response.py`  
**Response processing utilities**

- **Lines 85, 108**: Extraction of `thinking` content from model responses

### Frontend (Svelte/TypeScript)

#### 1. `src/lib/components/chat/Messages/ContentRenderer.svelte`
**Main content rendering orchestrator**

- Integrates Markdown processing
- Handles user interactions with content
- Manages floating buttons and selection

#### 2. `src/lib/components/chat/Messages/Markdown.svelte`
**Markdown processing with thinking tokens**

- Uses `marked.js` with custom extensions
- Calls `processResponseContent()` for content cleaning
- Renders tokens through `MarkdownTokens.svelte`

#### 3. `src/lib/utils/index.ts`
**Content processing utilities**

Key functions:
- `processResponseContent()` - Main content processing
- `removeDetails()` - Remove specific detail types
- `removeAllDetails()` - Remove all detail tags
- `processDetails()` - Process and convert detail tags

```typescript
export const removeDetails = (content, types) => {
    for (const type of types) {
        content = content.replace(
            new RegExp(`<details\\s+type="${type}"[^>]*>.*?<\\/details>`, 'gis'),
            ''
        );
    }
    return content;
};
```

## 🔄 Processing Flow

1. **Model Output** → Contains thinking tags (e.g., `<thinking>...</thinking>`)
2. **Middleware Detection** → `middleware.py` detects and parses tags
3. **Block Creation** → Creates structured content blocks
4. **HTML Generation** → Converts to `<details>` HTML elements
5. **Frontend Rendering** → Svelte components render as collapsible sections

## 🛠️ Development Quick Start

### Adding New Thinking Tag Types

1. **Backend**: Add to `DEFAULT_REASONING_TAGS` in `middleware.py`
2. **Test**: Add test cases in `test_thinking_tokens.py`
3. **Documentation**: Update `docs/THINKING_TOKENS.md`

### Customizing Display

1. **HTML Structure**: Modify serialization in `middleware.py` (lines 1605-1632)
2. **Styling**: Update CSS in Svelte components
3. **Behavior**: Modify `ContentRenderer.svelte` for interactions

### Testing Changes

```bash
# Run thinking tokens tests
python test_thinking_tokens.py

# Try the interactive demo
python thinking_tokens_demo.py

# Run frontend linting
npm run lint:frontend

# Run frontend tests (if available)
npm run test:frontend
```

## 🎮 Trying It Out

### Demo Script
```bash
python thinking_tokens_demo.py
```

### Test Model Output
Try sending this to a model that supports thinking:
```
<thinking>
Let me analyze this request step by step:
1. The user wants to understand X
2. I should explain Y first
3. Then provide examples
</thinking>

Based on my analysis, here's the explanation...
```

## 🔧 Configuration Options

### Enabling/Disabling
```python
# In request parameters
"reasoning_tags": [["<think>", "</think>"]]  # Custom tags
"reasoning_tags": False                       # Disable detection
```

### Custom Tags
```python
reasoning_tags = [
    ("<my_thinking>", "</my_thinking>"),
    ("◁reasoning▷", "◁/reasoning▷")
]
```

## 📖 Further Reading

- **Complete Documentation**: `docs/THINKING_TOKENS.md`
- **Test Examples**: `test_thinking_tokens.py`
- **Interactive Demo**: `thinking_tokens_demo.py`

## 🤝 Contributing

When modifying thinking token functionality:

1. **Update Tests**: Add test cases for new functionality
2. **Document Changes**: Update this README and main documentation
3. **Test Thoroughly**: Verify with various content types and edge cases
4. **Consider Performance**: Test with large content and streaming responses

## 🐛 Troubleshooting

| Issue | Check Location | Solution |
|-------|----------------|----------|
| Tags not detected | `middleware.py` line 114 | Verify tag in `DEFAULT_REASONING_TAGS` |
| HTML not rendering | Frontend components | Check CSS and component structure |
| Performance issues | `utils/index.ts` | Optimize regex patterns |
| Streaming problems | `middleware.py` lines 2120+ | Debug streaming logic |

---

**💡 Pro Tip**: Use the demo script to quickly test how different thinking tag formats will be processed without setting up the full application.