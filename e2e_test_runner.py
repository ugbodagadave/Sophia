import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.receipt_processing_flow import process_slack_file_url

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: python e2e_test_runner.py <file_url>")
		sys.exit(1)
	url = sys.argv[1]
	print(f"Processing URL: {url}")
	result = process_slack_file_url(url)
	print("\n--- Result ---")
	print(result)
	print("----------------") 