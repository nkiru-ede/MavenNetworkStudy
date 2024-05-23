# Initialize the project by installing dependencies
init:
    pip install -r requirements.txt

# Execute the main Python script
run:
    python dataanalysis.py

# Run unit tests
test:
    python -m unittest discover -s tests -p 'test_*.py'

# Clean up temporary files and directories
clean:
    rm -rf __pycache__

# Mark targets as phony (non-file targets)
.PHONY: init test run clean

