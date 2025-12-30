#!/usr/bin/env python3
"""
Quick test script for LLM integration
Run this to verify your LLM setup is working
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.models.llm_service import get_llm_service


def test_llm(backend: str = "ollama"):
    """Test LLM service"""
    print(f"\n🧪 Testing {backend.upper()} LLM backend...")
    print("=" * 50)
    
    try:
        llm = get_llm_service(backend)
        
        # Test 1: Prompt enhancement
        print("\n1️⃣ Testing prompt enhancement...")
        user_desc = "dinosaur in clouds"
        enhanced = llm.enhance_prompt(user_desc)
        print(f"   Input:  {user_desc}")
        print(f"   Output: {enhanced}")
        
        # Test 2: Hint generation
        print("\n2️⃣ Testing hint generation...")
        hints = llm.generate_hints("dinosaur", num_hints=3)
        print(f"   Generated {len(hints)} hints:")
        for i, hint in enumerate(hints, 1):
            print(f"   {i}. {hint}")
        
        # Test 3: Description understanding
        print("\n3️⃣ Testing description understanding...")
        understanding = llm.understand_description("a fierce dragon in the shadows")
        print(f"   Parsed: {understanding}")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test LLM integration")
    parser.add_argument(
        "--backend",
        choices=["ollama", "openai", "huggingface"],
        default="ollama",
        help="LLM backend to test"
    )
    
    args = parser.parse_args()
    
    success = test_llm(args.backend)
    sys.exit(0 if success else 1)

