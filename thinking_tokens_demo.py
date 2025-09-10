#!/usr/bin/env python3
"""
Thinking Tokens Demo Script

This script demonstrates how thinking tokens work in Open WebUI by showing
the transformation process from raw model output to formatted HTML.
"""

import re
import time
import json
from typing import Dict, List, Any


class ThinkingTokenProcessor:
    """
    Simplified version of the thinking token processing logic from Open WebUI.
    This demonstrates the core concepts without the full middleware complexity.
    """
    
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
    
    def __init__(self):
        self.content_blocks = []
    
    def detect_reasoning_tags(self, content: str) -> List[Dict[str, Any]]:
        """
        Detect reasoning tags in content and return structured blocks.
        """
        blocks = []
        
        for start_tag, end_tag in self.DEFAULT_REASONING_TAGS:
            # Simple pattern matching for demonstration
            pattern = rf"{re.escape(start_tag)}(.*?){re.escape(end_tag)}"
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                reasoning_content = match.group(1).strip() if match.group(1) else ""
                
                if reasoning_content:  # Only process non-empty reasoning
                    blocks.append({
                        "type": "reasoning",
                        "start_tag": start_tag,
                        "end_tag": end_tag,
                        "content": reasoning_content,
                        "started_at": time.time(),
                        "ended_at": time.time() + 1,  # Simulate 1 second thinking
                        "duration": 1,
                        "original_match": match.group(0)
                    })
        
        return blocks
    
    def process_content(self, content: str) -> Dict[str, Any]:
        """
        Process content and extract reasoning blocks.
        """
        reasoning_blocks = self.detect_reasoning_tags(content)
        
        # Remove reasoning tags from main content
        processed_content = content
        for block in reasoning_blocks:
            processed_content = processed_content.replace(block["original_match"], "")
        
        # Clean up extra whitespace
        processed_content = re.sub(r'\n\s*\n', '\n\n', processed_content).strip()
        
        return {
            "main_content": processed_content,
            "reasoning_blocks": reasoning_blocks,
            "total_reasoning_time": sum(block["duration"] for block in reasoning_blocks)
        }
    
    def generate_html_output(self, processed_data: Dict[str, Any]) -> str:
        """
        Generate HTML output similar to Open WebUI's format.
        """
        html_parts = []
        
        # Add reasoning blocks as collapsible details
        for block in processed_data["reasoning_blocks"]:
            duration = block["duration"]
            reasoning_content = block["content"]
            
            # Format reasoning content with blockquote-style indentation
            formatted_reasoning = "\n".join(
                f"> {line}" if not line.startswith(">") else line
                for line in reasoning_content.splitlines()
            )
            
            html_block = f"""<details type="reasoning" done="true" duration="{duration}">
<summary>Thought for {duration} second{'s' if duration != 1 else ''}</summary>
{formatted_reasoning}
</details>"""
            
            html_parts.append(html_block)
        
        # Add main content
        if processed_data["main_content"]:
            html_parts.append(processed_data["main_content"])
        
        return "\n\n".join(html_parts)


def demo_examples():
    """
    Demonstrate various thinking token examples.
    """
    processor = ThinkingTokenProcessor()
    
    examples = [
        {
            "title": "Basic Thinking Example",
            "content": """<thinking>
The user is asking about quantum computing. I should explain it in simple terms first, then gradually introduce more complex concepts. Let me structure this clearly:
1. Basic definition
2. Key principles  
3. Current applications
4. Future potential
</thinking>

Quantum computing is a revolutionary approach to computation that leverages the principles of quantum mechanics. Unlike classical computers that use bits (0 or 1), quantum computers use quantum bits or "qubits" that can exist in multiple states simultaneously through a property called superposition."""
        },
        
        {
            "title": "Multiple Reasoning Sections",
            "content": """<thinking>
First, I need to understand what the user wants to know about machine learning.
</thinking>

Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience.

<reasoning>
Now I should explain the different types of machine learning:
- Supervised learning (with labeled data)
- Unsupervised learning (finding patterns)  
- Reinforcement learning (learning through rewards)
I'll give examples for each.
</reasoning>

There are three main types of machine learning:

1. **Supervised Learning**: Uses labeled training data
2. **Unsupervised Learning**: Finds patterns in unlabeled data  
3. **Reinforcement Learning**: Learns through trial and error"""
        },
        
        {
            "title": "Complex Reasoning with Code",
            "content": """<think>
The user wants to understand how to implement a binary search algorithm. Let me think through this:

1. Binary search requires a sorted array
2. We compare the target with the middle element
3. If target is smaller, search the left half
4. If target is larger, search the right half
5. Repeat until found or search space is empty

I should provide both recursive and iterative implementations.
</think>

Here's how to implement binary search:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found
```"""
        },
        
        {
            "title": "Nested and Complex Content",
            "content": """<reasoning>
This is a complex question about climate change. I need to:

1. Explain the greenhouse effect
2. Discuss human contributions
3. Mention feedback loops
4. Address potential solutions

I should be careful to present scientific consensus while acknowledging uncertainties where they exist.
</reasoning>

Climate change refers to long-term shifts in global temperatures and weather patterns. While climate variations are natural, scientific evidence shows that human activities have been the primary driver since the 1950s.

**Key factors include:**
- Greenhouse gas emissions (CO₂, methane, etc.)
- Deforestation reducing carbon absorption  
- Industrial processes and energy consumption

**Feedback loops** amplify these effects - for example, melting ice reduces surface reflection, causing more warming."""
        }
    ]
    
    print("🧠 Thinking Tokens Demo - Open WebUI")
    print("=" * 50)
    
    for i, example in enumerate(examples, 1):
        print(f"\n📖 Example {i}: {example['title']}")
        print("-" * 40)
        
        print("🔤 Raw Model Output:")
        print(example['content'])
        
        print("\n🔄 Processing...")
        processed = processor.process_content(example['content'])
        
        print(f"   • Found {len(processed['reasoning_blocks'])} reasoning section(s)")
        print(f"   • Total thinking time: {processed['total_reasoning_time']} seconds")
        
        print("\n🎨 Generated HTML:")
        html_output = processor.generate_html_output(processed)
        print(html_output)
        
        print("\n" + "="*50)


def interactive_demo():
    """
    Interactive demo allowing users to test their own content.
    """
    processor = ThinkingTokenProcessor()
    
    print("\n🎮 Interactive Thinking Tokens Demo")
    print("Enter content with thinking tags (or 'quit' to exit)")
    print("Supported tags:", ", ".join([tag[0] for tag in processor.DEFAULT_REASONING_TAGS]))
    print("-" * 50)
    
    while True:
        print("\nEnter your content (press Enter twice to process):")
        
        lines = []
        while True:
            try:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                if line.lower() == 'quit':
                    return
                lines.append(line)
            except KeyboardInterrupt:
                print("\nExiting...")
                return
        
        content = "\n".join(lines[:-1])  # Remove the extra empty line
        
        if not content.strip():
            continue
            
        print("\n🔄 Processing your content...")
        processed = processor.process_content(content)
        
        print(f"📊 Analysis:")
        print(f"   • Reasoning sections found: {len(processed['reasoning_blocks'])}")
        print(f"   • Total thinking time: {processed['total_reasoning_time']} seconds")
        
        if processed['reasoning_blocks']:
            print(f"   • Tags detected: {[block['start_tag'] for block in processed['reasoning_blocks']]}")
        
        print(f"\n🎨 Formatted Output:")
        html_output = processor.generate_html_output(processed)
        print(html_output)


if __name__ == "__main__":
    print("Welcome to the Thinking Tokens Demo!")
    print("This demonstrates how Open WebUI processes reasoning content.")
    
    while True:
        print("\nChoose an option:")
        print("1. View demo examples")
        print("2. Interactive demo")
        print("3. Exit")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                demo_examples()
            elif choice == "2":
                interactive_demo()
            elif choice == "3":
                print("Thanks for trying the demo! 🚀")
                break
            else:
                print("Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\nThanks for trying the demo! 🚀")
            break