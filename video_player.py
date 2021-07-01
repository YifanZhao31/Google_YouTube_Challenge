"""A video player class."""


from video_library import VideoLibrary
from video_playlist import Playlist
import random
import operator

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:", )      
        video_info = []
        for video in self._video_library.get_all_videos():
            tag = ' '.join(map(str,(video._tags)))
            if video._flagged:
                if bool(self._flag_reason):
                    info = video._title + ' (' + video._video_id + ') ' + '[' + tag + '] - FLAGGED (reason: ' + self._flag_reason + ')'  
                else:
                    info = video._title + ' (' + video._video_id + ') ' + '[' + tag + '] - FLAGGED (reason: Not supplied)'
            else: 
                info = video._title + ' (' + video._video_id + ') ' + '[' + tag + '] '           
            video_info.append(info)
        sorted_videos = sorted(video_info)           
        print('\n'.join(sorted_videos))       

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        i = 0
        video = self._video_library.get_video(video_id)
        if video == None:
            i = 1
            print('Cannot play video: Video does not exist')
        elif video._flagged and bool(video._flag_reason):
            i = 1
            print('Cannot play video: Video is currently flagged (reason: ' + video._flag_reason + ')')
        elif video._flagged and not bool(video._flag_reason):
            i = 1
            print('Cannot play video: Video is currently flagged (reason: Not supplied)')
        else:
            for vid in self._video_library.get_all_videos():
                if vid._playing:
                    i = 1
                    setattr(vid, '_playing', False)
                    setattr(vid, '_paused', False)
                    print('Stopping video: ' + vid._title)
                    setattr(video, '_playing', True)
                    setattr(video, '_paused', False)
                    print('Playing video: ' + video._title)
                    break
        
        if i == 0:
            setattr(video, '_playing', True) 
            setattr(video, '_paused', False)              
            print('Playing video: ' + video._title) 

    def stop_video(self):
        """Stops the current video."""
        i = 0
        for video in self._video_library.get_all_videos():
            if video._playing:
                i = 1
                setattr(video, '_playing', False)
                setattr(video, '_paused', False)
                print('Stopping video: ' + video._title)
                break      
        if i == 0:
            print('Cannot stop video: No video is currently playing')

    def play_random_video(self):
        """Plays a random video from the video library."""
        i = 0
        videos = self._video_library.get_all_videos()
        for video in videos:
            if video._flagged:
                videos.remove(video)
        
        if len(videos) == 0:
            print('No videos available')
        else:
            rand = random.choice(videos)
            for video in videos:
                if video._playing:
                    i = 1
                    setattr(video, '_playing', False)
                    setattr(video, '_paused', False)
                    print('Stopping video: ' + video._title)
                    setattr(rand, '_playing', True)
                    setattr(rand, '_paused', False)
                    print('Playing video: ' + rand._title)
                    break
            if i == 0:
                setattr(rand, '_playing', True)
                setattr(rand, '_paused', False)
                print('Playing video: ' + rand._title)

    def pause_video(self):
        """Pauses the current video."""
        i = 0
        videos = self._video_library.get_all_videos()
        for video in videos:
            if video._playing:
                i = 1
                if video._paused:
                    print('Video already paused: ' + video._title)
                else:
                    setattr(video, '_paused', True)
                    print('Pausing video: ' + video._title)
                break
        if i == 0:
            print('Cannot pause video: No video is currently playing')
            

    def continue_video(self):
        """Resumes playing the current video."""
        i = 0
        videos = self._video_library.get_all_videos()
        for video in videos:
            if video._playing:
                i = 1
                if video._paused:
                    setattr(video, '_paused', False)
                    print('Continuing video: ' + video._title)
                else:
                    print('Cannot continue video: Video is not paused')
                break
        if i == 0:
            print('Cannot continue video: No video is currently playing')
        
    def show_playing(self):
        """Displays video currently playing."""
        i = 0
        videos = self._video_library.get_all_videos()
        for video in videos:
            if video._playing:
                i = 1
                tag = ' '.join(map(str,(video._tags)))
                info = video._title + ' (' + video._video_id + ') ' + '[' + tag + ']'
                if video._paused:
                    print('Currently playing: ' + info + ' - PAUSED')
                else:
                    print('Currently playing: ' + info)
                break
        if i == 0:
            print('No video is currently playing')

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if playlist_name.lower() not in Playlist.playlists_dict:
            print('Successfully created new playlist: ' + playlist_name)
            Playlist(playlist_name, [])
        else:
            print('Cannot create playlist: A playlist with the same name already exists')


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        name = playlist_name.lower()
        playlist = Playlist.playlists_dict.get(name)       
        if name not in Playlist.playlists_dict:
            print('Cannot add video to ' + playlist_name + ': Playlist does not exist')
        elif video == None:
            print('Cannot add video to ' + playlist_name + ': Video does not exist')
        elif video._flagged and bool(video._flag_reason):
            print('Cannot add video to ' + playlist_name +': Video is currently flagged (reason: ' + self._flag_reason + ')')
        elif video._flagged and not bool(video._flag_reason):
            print('Cannot add video to ' + playlist_name + ': Video is currently flagged (reason: Not supplied)')
        elif video in playlist._contents:
            print('Cannot add video to ' + playlist_name + ': Video already added')
        else:
            print('Added video to ' + playlist_name + ': ' + video._title)
            playlist._contents.append(video)


    def show_all_playlists(self):
        """Display all playlists."""
        lists = Playlist.playlists_dict.values()
        if len(lists) == 0:
            print('No playlists exist yet')
        else:
            print('Showing all playlists:')
            names = []
            for playlist in lists:
                names.append(playlist._name)
            sorted_playlists = sorted(names)
            print('\n'.join(sorted_playlists))

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        playlist = Playlist.playlists_dict.get(name)
        if name not in Playlist.playlists_dict:
            print('Cannot show playlist ' + playlist_name + ': Playlist does not exist')
        elif len(playlist._contents) == 0:
            print('Showing playlist: ' + playlist_name)
            print('No videos here yet') 
        else:
            print('Showing playlist: ' + playlist_name)
            for video in playlist._contents:
                tag = ' '.join(map(str,(video._tags)))
                if video._flagged:
                    if bool(video._flag_reason):
                        print(video._title + ' (' + video._video_id + ') ' + '[' + tag + '] - FLAGGED (reason: ' + video._flag_reason + ')')  
                    else:
                        print(video._title + ' (' + video._video_id + ') ' + '[' + tag + '] - FLAGGED (reason: Not supplied)')
            else: 
                print(video._title + ' (' + video._video_id + ') ' + '[' + tag + ']')

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        name = playlist_name.lower()
        video = self._video_library.get_video(video_id)
        playlist = Playlist.playlists_dict.get(name)
        if name not in Playlist.playlists_dict:
            print('Cannot remove video from ' + playlist_name + ': Playlist does not exist')
        elif video == None:
            print('Cannot remove video from ' + playlist_name + ': Video does not exist')
        elif video not in playlist._contents:
            print('Cannot remove video from ' + playlist_name + ': Video is not in playlist')
        else:
            playlist._contents.remove(video)
            print('Removed video from ' + playlist_name + ': ' + video._title)
            
    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        playlist = Playlist.playlists_dict.get(name)
        if name not in Playlist.playlists_dict:
            print('Cannot clear playlist ' + playlist_name + ': Playlist does not exist')
        else:
            playlist._contents.clear()
            print('Successfully removed all videos from ' + playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        if name not in Playlist.playlists_dict:
            print('Cannot delete playlist ' + playlist_name + ': Playlist does not exist')
        else:
            Playlist.playlists_dict.pop(name)
            print('Deleted playlist ' + playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        i = 0
        titles = []
        term = str(search_term).lower()
        sort = sorted(self._video_library.get_all_videos(), key=operator.attrgetter('_title'))
        for video in sort:
            if video._flagged:
                sort.remove(video)
                
        for video in sort:
            if term in video._title.lower():
                i += 1
        if i != 0:
            print('Here are the results for ' + str(search_term) + ':')
        
        i = 0
        for video in sort:
            if term in video._title.lower():
                i += 1
                titles.append(video._title)
                tag = ' '.join(map(str,(video._tags)))
                print(str(i) + ') ' + video._title + ' (' + video._video_id + ') ' + '[' + tag + ']')
        if i != 0:
            print('Would you like to play any of the above? If yes, specify the number of the video.')
            print('If your answer is not a valid number, we will assume it\'s a no.')
            ans = input()
            try:
                x = int(ans)
                if 0 < x < (i+1):
                    print('Playing video: ' + titles[x - 1])
            except ValueError:
                pass
            
        else:
            print('No search results for ' + str(search_term))
        

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        i = 0
        titles = []
        tag = str(video_tag).lower()
        sort = sorted(self._video_library.get_all_videos(), key=operator.attrgetter('_title'))
        for video in sort:
            if video._flagged:
                sort.remove(video)
        
        for video in sort:
            for t in video._tags:
                if tag == t:
                    i += 1
        if i != 0:
            print('Here are the results for ' + str(video_tag) + ':')
        
        i = 0            
        for video in sort:
            for t in video._tags:
                if tag == t:
                    i += 1
                    titles.append(video._title)
                    vid_tag = ' '.join(map(str,(video._tags)))
                    print(str(i) + ') ' + video._title + ' (' + video._video_id + ') ' + '[' + vid_tag + ']')
        if i != 0:
            print('Would you like to play any of the above? If yes, specify the number of the video.')
            print('If your answer is not a valid number, we will assume it\'s a no.')
            ans = input()
            try:
                x = int(ans)
                if 0 < x < (i+1):
                    print('Playing video: ' + titles[x - 1])
            except ValueError:
                pass
        else:
            print('No search results for ' + str(video_tag))

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        self._flag_reason = flag_reason
        video = self._video_library.get_video(video_id)
        if video != None:
            setattr(video, '_flag_reason', flag_reason)
        if video!= None and video._playing:
            print('Stopping video: ' + video._title)
            
        if video == None:
            print('Cannot flag video: Video does not exist')
        elif video._flagged:
            print('Cannot flag video: Video is already flagged')
        elif bool(flag_reason):
            setattr(video, '_flagged', True)
            setattr(video, '_playing', False)
            print('Successfully flagged video: ' + video._title + ' (reason: ' + flag_reason + ')')
        else:
            setattr(video, '_flagged', True)
            setattr(video, '_playing', False)
            print('Successfully flagged video: ' + video._title + ' (reason: Not supplied)')

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        
        if video == None:
            print('Cannot remove flag from video: Video does not exist')
        elif video._flagged:
            setattr(video, '_flagged', False)
            print('Successfully removed flag from video: ' + video._title)
        else:
            print('Cannot remove flag from video: Video is not flagged')
            
            
        
