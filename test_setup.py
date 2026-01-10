"""
Setup Test Script
Run this to verify your entire LLM Council setup is working correctly.
"""

import requests
import sys
from typing import Dict, Any

# Configuration - Edit these to match your setup
PC1_CHAIRMAN_URL = "http://localhost:5002"
PC2_COUNCIL_URL = "http://localhost:5001"
FRONTEND_URL = "http://localhost:5000"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text: str):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def test_endpoint(name: str, url: str) -> bool:
    """Test if an endpoint is accessible."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print_success(f"{name} is accessible")
            data = response.json()
            print(f"  Response: {data}")
            return True
        else:
            print_error(f"{name} returned HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"{name} - Connection refused (is the server running?)")
        return False
    except requests.exceptions.Timeout:
        print_error(f"{name} - Request timeout")
        return False
    except Exception as e:
        print_error(f"{name} - Error: {str(e)}")
        return False

def test_ollama(url_base: str, name: str) -> bool:
    """Test if Ollama is accessible."""
    try:
        # Try to reach Ollama API directly
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print_success(f"Ollama is running on {name}")
            models = response.json().get('models', [])
            print(f"  Available models: {len(models)}")
            for model in models:
                print(f"    - {model['name']}")
            return True
        else:
            print_error(f"Ollama responded with HTTP {response.status_code}")
            return False
    except Exception as e:
        print_warning(f"Cannot reach Ollama on {name} (this is OK if testing remotely)")
        return None

def main():
    """Run all tests."""
    print_header("LLM COUNCIL SETUP TEST")

    print("Testing configuration:")
    print(f"  PC1 Chairman: {PC1_CHAIRMAN_URL}")
    print(f"  PC2 Council:  {PC2_COUNCIL_URL}")
    print(f"  Frontend:     {FRONTEND_URL}")

    results = {}

    # Test Ollama (only works if running locally)
    print_header("Test 1: Ollama Availability")
    ollama_result = test_ollama("http://localhost:11434", "localhost")
    if ollama_result:
        print_success("Ollama is accessible")
    elif ollama_result is None:
        print_warning("Skipping Ollama test (remote setup)")
    else:
        print_error("Ollama is not running - start it first!")

    # Test PC2 Council
    print_header("Test 2: PC2 Council Server")
    results['pc2_health'] = test_endpoint(
        "PC2 /health",
        f"{PC2_COUNCIL_URL}/health"
    )

    if results['pc2_health']:
        results['pc2_models'] = test_endpoint(
            "PC2 /models",
            f"{PC2_COUNCIL_URL}/models"
        )

        results['pc2_test'] = test_endpoint(
            "PC2 /test",
            f"{PC2_COUNCIL_URL}/test"
        )

    # Test PC1 Chairman
    print_header("Test 3: PC1 Chairman Server")
    results['pc1_health'] = test_endpoint(
        "PC1 /health",
        f"{PC1_CHAIRMAN_URL}/health"
    )

    if results['pc1_health']:
        results['pc1_model'] = test_endpoint(
            "PC1 /model",
            f"{PC1_CHAIRMAN_URL}/model"
        )

        results['pc1_test'] = test_endpoint(
            "PC1 /test",
            f"{PC1_CHAIRMAN_URL}/test"
        )

    # Test Frontend
    print_header("Test 4: Frontend Coordinator")
    results['frontend_health'] = test_endpoint(
        "Frontend /health",
        f"{FRONTEND_URL}/health"
    )

    if results['frontend_health']:
        results['frontend_config'] = test_endpoint(
            "Frontend /config",
            f"{FRONTEND_URL}/config"
        )

    # Test Full Workflow (optional - takes time)
    print_header("Test 5: Full Council Workflow (Optional)")
    print("This test will submit a query to the full council pipeline.")
    print("It may take 30-60 seconds to complete.")
    print()

    user_input = input("Run full workflow test? (y/n): ")

    if user_input.lower() == 'y':
        try:
            print("\nSubmitting test query...")
            response = requests.post(
                f"{FRONTEND_URL}/council",
                json={"query": "What is 2+2?"},
                timeout=180
            )

            if response.status_code == 200:
                data = response.json()
                print_success("Full workflow completed!")
                print(f"  Answers: {len(data.get('stage1_answers', []))}")
                print(f"  Reviews: {len(data.get('stage2_reviews', []))}")
                print(f"  Final answer length: {len(data.get('stage3_final', ''))} chars")
                results['full_workflow'] = True
            else:
                print_error(f"Workflow failed with HTTP {response.status_code}")
                results['full_workflow'] = False
        except Exception as e:
            print_error(f"Workflow error: {str(e)}")
            results['full_workflow'] = False
    else:
        print("Skipping full workflow test")
        results['full_workflow'] = None

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)

    print(f"Passed:  {Colors.GREEN}{passed}{Colors.END}")
    print(f"Failed:  {Colors.RED}{failed}{Colors.END}")
    print(f"Skipped: {Colors.YELLOW}{skipped}{Colors.END}")

    if failed == 0 and passed > 0:
        print_success("\nAll tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Open your browser to: " + FRONTEND_URL)
        print("2. Submit a test query")
        print("3. Verify all 3 stages work correctly")
        return 0
    elif failed > 0:
        print_error("\nSome tests failed. Check the output above.")
        print("\nTroubleshooting:")
        print("1. Make sure all servers are running")
        print("2. Check firewall settings")
        print("3. Verify IP addresses in configuration")
        print("4. Check that Ollama is running and models are pulled")
        return 1
    else:
        print_warning("\nNo tests were run. Check your configuration.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
