import unittest
from unittest.mock import patch, mock_open
from main import PlaylistManager


class TestPlaylistManager(unittest.TestCase):
    @patch('main.pandas.read_csv')
    def setUp(self, mock_read_csv):
        # Set up a fake dataframe
        mock_read_csv.return_value = {
            'Artist Name(s)': ['Artist1', 'Artist2'],
            'Track Name': ['Song1', 'Song2']
        }

        self.manager = PlaylistManager(
            playlist_path='example.csv',
            clarifying_question='Add this? '
        )
        # Set fixed test data
        self.manager.songs = {('Artist1', 'Song1'), ('Artist2', 'Song2')}

    @patch('builtins.input', side_effect=['y', 'n'])
    def test_sort_playlist(self, mock_input):
        self.manager.sort_playlist()
        self.assertIn(('Artist1', 'Song1'), self.manager._songs_to_keep)
        self.assertIn(('Artist2', 'Song2'), self.manager._songs_to_remove)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_results(self, mock_file):
        self.manager._songs_to_keep = [('Artist1', 'Song1')]
        self.manager._songs_to_remove = [('Artist2', 'Song2')]

        self.manager.save_results('keep.txt', 'remove.txt')

        # Check if open was called correctly
        calls = [((('keep.txt', 'w'),),), ((('remove.txt', 'w'),),)]
        mock_file.assert_any_call('keep.txt', 'w')
        mock_file.assert_any_call('remove.txt', 'w')

        # Check write calls
        handle = mock_file()
        handle.write.assert_any_call("Artist1, Song1\n")
        handle.write.assert_any_call("Artist2, Song2\n")


if __name__ == '__main__':
    unittest.main()
