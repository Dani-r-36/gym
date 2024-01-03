import unittest
from unittest.mock import MagicMock, patch, Mock
from user_options import GymTracker
from whatsapp_commands import send_message

class TestGymTracker(unittest.TestCase):

    @patch('find_exercise.all_lifts')  
    def test_find_lift(self, mock_all_lifts):
        # Create a MagicMock for the weight_option method
        print("running patch")
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

    @patch('user_options.ExerciseDetails.number_muscles', return_value=2)
    @patch('user_options.ExerciseDetails.sub_muscle_groups', return_value=(['Muscle1', 'Muscle2'], 'MuscleGroup'))
    @patch('user_options.ExerciseDetails.get_new_exercise_details', return_value=(True, 'UserRequest'))
    @patch('user_options.insert_new_exercise')
    def test_inserting(self, mock_insert_new_exercise, mock_get_new_exercise_details, mock_sub_muscle_groups, mock_number_muscles):
        with patch('user_options.send_message', MagicMock()) as mock_send_message:
            # Create an instance of GymTracker
            gym_tracker = GymTracker()

            # Call the inserting method
            result = gym_tracker.inserting()

            # Assert that the mocked functions were called
            mock_number_muscles.assert_called_once()
            mock_sub_muscle_groups.assert_called_once_with(2)
            mock_get_new_exercise_details.assert_called_once_with(['Muscle1', 'Muscle2'], 'MuscleGroup')
            mock_insert_new_exercise.assert_called_once_with(True, 'UserRequest')

            # Assert the return value of inserting
            self.assertEqual(result, "Loop")
    
    @patch('user_options.fuzz.partial_ratio', return_value=80)  # Mock the partial_ratio function
    @patch('whatsapp_commands.send_message', MagicMock())  # Mock the send_message function
    def test_choice_end_session(self, mock_partial_ratio):
        with patch('user_options.send_and_wait', side_effect=["Loop"]):
            # Create an instance of GymTracker
            gym_tracker = GymTracker()

            # Set the return_message to trigger the "End session" condition
            gym_tracker.return_message = "End session"

            # Call the choice method
            result = gym_tracker.choice()

            # Assert that the mocked functions were called
            mock_partial_ratio.assert_called_once_with("End session", "End session")
            gym_tracker.send_and_wait.assert_called_once_with("You look bigger than you think <3")

            # Assert the return value of choice
            self.assertEqual(result, "End")

if __name__ == '__main__':
    unittest.main()
