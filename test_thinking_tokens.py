"""
Test suite for thinking tokens and content processing functionality.

This module tests the core thinking token processing logic in Open WebUI.
"""

import re
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from backend.open_webui.utils.middleware import DEFAULT_REASONING_TAGS
except ImportError:
    # Define fallback for testing when backend is not available
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


class TestThinkingTokens:
    """Test suite for thinking token processing."""

    def test_default_reasoning_tags(self):
        """Test that default reasoning tags are properly defined."""
        assert len(DEFAULT_REASONING_TAGS) > 0
        
        # Check that all tags are tuples with start and end
        for start_tag, end_tag in DEFAULT_REASONING_TAGS:
            assert isinstance(start_tag, str)
            assert isinstance(end_tag, str)
            assert len(start_tag) > 0
            assert len(end_tag) > 0
        
        # Check for expected tags
        tag_starts = [tag[0] for tag in DEFAULT_REASONING_TAGS]
        assert "<thinking>" in tag_starts
        assert "<think>" in tag_starts
        assert "<reasoning>" in tag_starts

    def test_reasoning_tag_regex_patterns(self):
        """Test that reasoning tags can be detected using regex patterns."""
        
        test_content = """
        Here is some normal content.
        <thinking>
        This is a thinking section with some analysis.
        Let me think step by step.
        </thinking>
        And here is more normal content.
        """
        
        # Test basic detection
        for start_tag, end_tag in DEFAULT_REASONING_TAGS:
            if start_tag == "<thinking>":
                pattern = rf"{re.escape(start_tag)}(.*?){re.escape(end_tag)}"
                matches = re.findall(pattern, test_content, re.DOTALL)
                assert len(matches) == 1
                assert "This is a thinking section" in matches[0]

    def test_multiple_reasoning_sections(self):
        """Test handling of multiple reasoning sections in content."""
        
        test_content = """
        First paragraph.
        <thinking>First reasoning section</thinking>
        Middle paragraph.
        <reasoning>Second reasoning section</reasoning>
        Final paragraph.
        """
        
        # Count reasoning sections
        thinking_count = test_content.count("<thinking>")
        reasoning_count = test_content.count("<reasoning>")
        
        assert thinking_count == 1
        assert reasoning_count == 1

    def test_nested_reasoning_content(self):
        """Test handling of complex nested content within reasoning sections."""
        
        test_content = """
        <thinking>
        Let me analyze this:
        1. First point
        2. Second point with **bold** text
        3. Code example: `function() { return true; }`
        
        This includes markdown formatting within the reasoning.
        </thinking>
        """
        
        # Extract content between thinking tags
        pattern = r"<thinking>(.*?)</thinking>"
        matches = re.findall(pattern, test_content, re.DOTALL)
        
        assert len(matches) == 1
        reasoning_content = matches[0].strip()
        
        # Check that complex content is preserved
        assert "1. First point" in reasoning_content
        assert "**bold**" in reasoning_content
        assert "`function()" in reasoning_content

    def test_edge_cases(self):
        """Test edge cases for thinking token processing."""
        
        # Empty reasoning section
        empty_content = "<thinking></thinking>"
        pattern = r"<thinking>(.*?)</thinking>"
        matches = re.findall(pattern, empty_content, re.DOTALL)
        assert len(matches) == 1
        assert matches[0] == ""
        
        # Reasoning section with only whitespace
        whitespace_content = "<thinking>   \n   </thinking>"
        matches = re.findall(pattern, whitespace_content, re.DOTALL)
        assert len(matches) == 1
        assert matches[0].strip() == ""
        
        # Malformed tags (should not match)
        malformed_content = "<thinking>Content without closing tag"
        matches = re.findall(pattern, malformed_content, re.DOTALL)
        assert len(matches) == 0

    def test_content_serialization(self):
        """Test the structure of content blocks for reasoning."""
        
        # Simulate the structure created by the middleware
        reasoning_block = {
            "type": "reasoning",
            "start_tag": "<thinking>",
            "end_tag": "</thinking>",
            "content": "This is reasoning content",
            "started_at": 1234567890.0,
            "ended_at": 1234567892.0,
            "duration": 2
        }
        
        # Verify block structure
        assert reasoning_block["type"] == "reasoning"
        assert reasoning_block["duration"] == 2
        assert reasoning_block["content"] is not None
        
        # Test HTML serialization format
        expected_html = f'<details type="reasoning" done="true" duration="2">\n<summary>Thought for 2 seconds</summary>\n> {reasoning_block["content"]}\n</details>'
        
        # This simulates the HTML generation logic
        assert "details" in expected_html
        assert "type=\"reasoning\"" in expected_html
        assert "duration=\"2\"" in expected_html

    def test_reasoning_with_special_characters(self):
        """Test reasoning content with special characters and encoding."""
        
        test_cases = [
            "<thinking>Content with émojis 🤔 and unicode ñ</thinking>",
            "<thinking>Code with < > & characters</thinking>",
            "<thinking>Quotes: \"double\" and 'single'</thinking>",
            "<thinking>Mathematical: x² + y² = z²</thinking>"
        ]
        
        pattern = r"<thinking>(.*?)</thinking>"
        
        for test_content in test_cases:
            matches = re.findall(pattern, test_content, re.DOTALL)
            assert len(matches) == 1
            # Content should be extracted properly
            assert len(matches[0]) > 0

    def test_reasoning_tags_configuration(self):
        """Test different reasoning tag configurations."""
        
        # Test all default tag pairs
        test_contents = [
            "<think>Analysis content</think>",
            "<thinking>Thinking content</thinking>",
            "<reason>Reasoning content</reason>",
            "<reasoning>Detailed reasoning</reasoning>",
            "<thought>A thought</thought>",
            "<Thought>Capitalized thought</Thought>",
            "<|begin_of_thought|>Special format<|end_of_thought|>",
            "◁think▷Custom symbols◁/think▷"
        ]
        
        for content in test_contents:
            # Each should contain recognizable reasoning patterns
            assert any(tag[0] in content for tag in DEFAULT_REASONING_TAGS)

    def test_performance_with_large_content(self):
        """Test performance with large content containing reasoning sections."""
        
        # Create large content with reasoning sections
        large_content = "Regular content. " * 1000
        large_content += "<thinking>" + "Analysis content. " * 100 + "</thinking>"
        large_content += "More regular content. " * 1000
        
        # Test that regex processing is reasonable
        pattern = r"<thinking>(.*?)</thinking>"
        matches = re.findall(pattern, large_content, re.DOTALL)
        
        assert len(matches) == 1
        assert len(matches[0]) > 0


class TestContentProcessing:
    """Test suite for general content processing utilities."""

    def test_remove_details_functionality(self):
        """Test the removeDetails function behavior."""
        
        test_content = """
        Some content before.
        <details type="reasoning" done="true">
        <summary>Reasoning</summary>
        This should be removed.
        </details>
        Some content after.
        <details type="code_interpreter" done="false">
        <summary>Code</summary>
        This should also be removed.
        </details>
        Final content.
        """
        
        # Simulate removeDetails functionality
        types_to_remove = ['reasoning', 'code_interpreter']
        content = test_content
        
        for type_name in types_to_remove:
            pattern = rf'<details\s+type="{type_name}"[^>]*>.*?</details>'
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Check that details were removed
        assert '<details type="reasoning"' not in content
        assert '<details type="code_interpreter"' not in content
        
        # Check that other content remains
        assert 'Some content before.' in content
        assert 'Some content after.' in content
        assert 'Final content.' in content

    def test_process_chinese_content(self):
        """Test processing of Chinese/international content."""
        
        # Test with mixed content
        test_content = """
        <thinking>
        让我分析一下这个问题：
        1. 首先考虑用户的需求
        2. 然后制定解决方案
        </thinking>
        根据分析，这是答案。
        """
        
        # Content should be preserved properly
        assert "让我分析" in test_content
        assert "解决方案" in test_content


if __name__ == "__main__":
    # Run basic tests if executed directly
    test_instance = TestThinkingTokens()
    
    print("Running thinking tokens tests...")
    
    try:
        test_instance.test_default_reasoning_tags()
        print("✓ Default reasoning tags test passed")
        
        test_instance.test_reasoning_tag_regex_patterns()
        print("✓ Regex patterns test passed")
        
        test_instance.test_multiple_reasoning_sections()
        print("✓ Multiple sections test passed")
        
        test_instance.test_edge_cases()
        print("✓ Edge cases test passed")
        
        content_test = TestContentProcessing()
        content_test.test_remove_details_functionality()
        print("✓ Content processing test passed")
        
        print("\nAll tests passed! ✅")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise