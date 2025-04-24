import pandas
from concurrent.futures import ThreadPoolExecutor


class PlaylistManager:
    def __init__(
        self,
        playlist_path: str,
        clarifying_question: str
    ):
        self.clarifying_question = clarifying_question + 'y/n? | '
        self.question = lambda song : str(clarifying_question + "| " + " ".join(song) + " | y/n? : ")

        self.songs: set[tuple[str, str]] = self._load_playlist(playlist_path) # set to avoid duplicates

        self._songs_to_keep = []
        self._songs_to_remove = []

    @staticmethod
    def _load_playlist(playlist_path: str, number_of_rows: int = 2) -> set[tuple[str, str]]:
        # for testing purposes. Just hardcode an int for number_of_rows
        df = pandas.read_csv(playlist_path, nrows=number_of_rows) if number_of_rows else pandas.read_csv(playlist_path)
        return set(zip(df['Artist Name(s)'], df['Track Name']))

    def sort_playlist(self, songs=None):
        """
        Sorts the playlist by asking the user if each song belongs to the playlist.
        :param songs: For recursion purposes. Do not pass a value.
        """
        songs = self.songs if songs is None else songs

        for index, song in enumerate(songs):
            question = str(self.clarifying_question + "".join(song))

            user_choice = input(self.question(song=song)).lower().strip()

            if user_choice == 'y':
                self._songs_to_keep.append(song)
            elif user_choice == 'n':
                self._songs_to_remove.append(song)
            else:
                print('Invalid input. Please enter "y" or "n".')
                return self.sort_playlist(songs=self.songs[index:])

    def save_results(self, songs_to_keep_path='songs_to_keep.txt', songs_to_remove_path='songs_to_remove.txt'):
        def save_to_file(file_path, songs):
            with open(file_path, 'w') as file:
                for song in songs:
                    file.write(f"{song[0]}, {song[1]}\n")

        tasks = [
            (save_to_file, songs_to_keep_path, self._songs_to_keep),
            (save_to_file, songs_to_remove_path, self._songs_to_remove)
        ]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(callback, path, songs) for callback, path, songs in tasks]
            for future in futures:
                future.result()

        print('Results saved successfully.')

if __name__ == '__main__':
    playlist_manager = PlaylistManager(
        playlist_path='tests/example.csv',
        clarifying_question='Does the song belong to this playlist? '
    )
    playlist_manager.sort_playlist()
    playlist_manager.save_results()

