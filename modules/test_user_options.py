import unittest
from unittest.mock import MagicMock, patch, Mock
from user_options import GymTracker
from find_exercise import all_lifts

class TestGymTracker(unittest.TestCase):

    @patch('find_exercise.all_lifts')  
    def test_find_lift(self, mock_all_lifts):
        # Create a MagicMock for the weight_option method
        with patch('user_options.GymTracker.weight_option', MagicMock()) as mock_weight_option:
            # Set up the mock return value for all_lifts
            lift= {'exercise_name': 'Seated Calves raise', 'exercise_id': 1}
            # Call the method you want to test
            result = GymTracker().find_lift(lift)
            # Assert that all_lifts was called
            # mock_all_lifts.assert_called_once()
            # Assert that weight_option was called with the expected arguments
            mock_weight_option.assert_called_once_with('Seated Calves raise', 1)
            # Assert the return value of find_lift
            self.assertEqual(result, "Loop")

    

if __name__ == '__main__':
    unittest.main()
