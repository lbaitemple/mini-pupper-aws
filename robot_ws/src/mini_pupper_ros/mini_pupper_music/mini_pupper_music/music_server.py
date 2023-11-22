#!/usr/bin/env python3
#
# Copyright 2023 MangDang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# @Author  : Cullen SUN

import rclpy
from rclpy.node import Node
from mini_pupper_interfaces.srv import MusicCommand
import threading
from pydub import AudioSegment
from pydub.playback import play
from pydub.playback import _play_with_simpleaudio

import os
from ament_index_python.packages import get_package_share_directory
from os import listdir

class MusicServiceNode(Node):
    def __init__(self):
        super().__init__('mini_pupper_music_service')
        self.playback = None
        self.service = self.create_service(
            MusicCommand,
            'music_command',
            self.play_music_callback
        )


        if 'MUSIC_CONFIG' in os.environ:
            music_config_path=os.environ["MUSIC_CONFIG"]
            isExist = os.path.exists(music_config_path)
        else:
            isExist = False        
    
        if (isExist):
            self.music_config_path = music_config_path
        else:
            self.declare_parameter('music_config_path', rclpy.Parameter.Type.STRING) 
            self.music_config_path = self.get_parameter('music_config_path').get_parameter_value().string_value
            
        self.get_logger().info(self.music_config_path)
        self.get_logger().info(str(self.music_config_path))

        
        sound_dir = self.music_config_path
        files = [f for f in os.listdir(sound_dir) if os.path.isfile(os.path.join(sound_dir, f))]
        self.song_pool =  set(files) #{'robot1.mp3', 'robot1.wav', 'how.wav', 'how.mp3'}
        self.playing_lock = threading.Lock()

    def play_music_callback(self, request, response):
        self.get_logger().info(f'play command at {request.command}')
        if request.command == 'play':
            if request.file_name in self.song_pool:
                if not self.playing_lock.locked():
                    self.play_sound_file(request.file_name,
                                         request.start_second,
                                         request.duration)
                    response.success = True
                    response.message = 'Sound playback started.'
                else:
                    response.success = False
                    response.message = 'Another sound is already playing.'
            else:
                response.success = False
                response.message = f'File {request.file_name} is not found.'
        elif request.command == 'stop':
            if self.playback:
                self.playback.stop() 
                response.success = True
                response.message = f'Command {request.command} the music.'            
        else:
            response.success = False
            response.message = f'Command {request.command} is not supported.'

        return response

    def play_sound_file(self, file_name, start_second, duration):
        # Create a new thread for playing the sound
        thread = threading.Thread(
            target=self.play_sound_in_background,
            args=(file_name, start_second, duration)
        )
        # Set the thread as a daemon (will exit when the main program ends)
        thread.daemon = True
        thread.start()

    def play_sound_in_background(self, file_name, start_second, duration):
        with self.playing_lock:
            package_name = 'mini_pupper_music'
#            package_path = get_package_share_directory(package_name)
            sound_dir = self.music_config_path
            sound_path = os.path.join(sound_dir, file_name)
            file_extension = file_name.split(".")[-1]
            self.get_logger().info(f'Play music at {sound_path}')

            # ROS2 might automatically make the duration 0.0 if it's not passed
            # Make it None to avoid program mistakes
            if duration == 0.0:
                duration = None

            audio = AudioSegment.from_file(
                file=sound_path,
                format=file_extension,
                start_second=start_second,
                duration=duration
            )

#            play(audio)
            self.playback = _play_with_simpleaudio(audio)
            

def main(args=None):
    rclpy.init(args=args)
    music_service_node = MusicServiceNode()
    rclpy.spin(music_service_node)
    music_service_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
