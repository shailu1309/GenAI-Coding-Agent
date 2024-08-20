from pathlib import Path
from unittest import mock

from genai_coding_agent.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from genai_coding_agent.dataset import main

# Assuming the test file is located at /Users/sjr11/Work/SelfLearning/GenAI Coding Agent/tests/test_dataset.py

def test_process_dataset_with_default_paths():
    # Mock the logger info and success methods
    with mock.patch('genai_coding_agent.dataset.logger.info') as mock_info, \
            mock.patch('genai_coding_agent.dataset.logger.success') as mock_success:
        # Call the main function with default paths
        main()

        # Verify that the logger info and success methods were called with the expected messages
        mock_info.assert_any_call("Processing dataset...")
        mock_info.assert_any_call("Something happened for iteration 5.")
        mock_success.assert_called_once_with("Processing dataset complete.")

        # Verify that the default paths were used
        assert main.input_path == RAW_DATA_DIR / "dataset.csv"
        assert main.output_path == PROCESSED_DATA_DIR / "dataset.csv"from pathlib import Path
        from unittest import mock
        
        from genai_coding_agent.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
        from genai_coding_agent.dataset import main
        
def test_process_dataset_with_valid_input_data():
    """
    This function tests the main dataset processing function with valid input data.

    Parameters:
    input_path (Path): The path to the input dataset file. Default is RAW_DATA_DIR / "dataset.csv".
    output_path (Path): The path to the output processed dataset file. Default is PROCESSED_DATA_DIR / "dataset.csv".

    Returns:
    None. The function is expected to perform the dataset processing and assert the expected outcomes.
    """
    # Mock the logger info and success methods
    with mock.patch('genai_coding_agent.dataset.logger.info') as mock_info, \
            mock.patch('genai_coding_agent.dataset.logger.success') as mock_success:
        # Call the main function with valid input data
        main(input_path=RAW_DATA_DIR / "valid_dataset.csv", output_path=PROCESSED_DATA_DIR / "valid_processed_dataset.csv")

        # Verify that the logger info and success methods were called with the expected messages
        mock_info.assert_any_call("Processing dataset...")
        mock_info.assert_any_call("Something happened for iteration 5.")
        mock_success.assert_called_once_with("Processing dataset complete.")

        # Verify that the valid input paths were used
        assert main.input_path == RAW_DATA_DIR / "valid_dataset.csv"
        assert main.output_path == PROCESSED_DATA_DIR / "valid_processed_dataset.csv"