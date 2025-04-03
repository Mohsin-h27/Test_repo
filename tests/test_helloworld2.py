import pytest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.helloworld import hello_world, hello_world2

# Use pytest markers
@pytest.mark.Read
def test_hello_world2():
    with patch('builtins.print') as mock_print:
        # Call the hello_world2 function
        hello_world2()
        
        # Check if print was called with the correct argument
        mock_print.assert_called_with('hello world2')
