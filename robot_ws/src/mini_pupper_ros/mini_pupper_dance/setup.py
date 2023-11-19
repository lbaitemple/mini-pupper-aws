from setuptools import setup
import os
from glob import glob

package_name = 'mini_pupper_dance'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'routines'), glob('routines/*.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mangdang',
    maintainer_email='mangdang@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'service = mini_pupper_dance.dance_server:main',
            'client = mini_pupper_dance.dance_client:main',
            'dance = mini_pupper_dance.dance:main',
            'refine_dance = mini_pupper_dance.refine_dance:main',
            'enhanced_dance = mini_pupper_dance.enhanced_dance:main',
            'pose_controller = mini_pupper_dance.pose_controller:main'
        ],
    },
)
