"""
Test runner for the Publication Assistant system
"""

import unittest
import sys
from pathlib import Path
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Suppress logging during tests
logging.getLogger().setLevel(logging.ERROR)


def run_tests():
    """Run all tests."""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent / "tests"
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print(f"\\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if result.skipped:
        print(f"\\nSkipped:")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\\n{'✅ All tests passed!' if success else '❌ Some tests failed'}")
    
    return success


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
