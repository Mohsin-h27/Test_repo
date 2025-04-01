import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.helloworld import hello_world

class TestHelloWorld(unittest.TestCase):

    @patch('builtins.print')
    def test_hello_world(self, mock_print):
        # Call the hello_world function
        hello_world()
        
        # Check if print was called with the correct argument
        mock_print.assert_called_with('hello World!')

if __name__ == '__main__':
    unittest.main()