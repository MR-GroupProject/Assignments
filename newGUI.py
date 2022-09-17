"""
Glooey widget example. Only runs with python>=3.6 (because of Glooey).
"""

from cgitb import text
from ctypes.wintypes import SIZE
import io
import pathlib

from tkinter import *
from tkinter import ttk

from turtle import color, onclick

import glooey
import numpy as np

import pyglet
import trimesh
import trimesh.viewer
import trimesh.transformations as tf
import PIL.Image


here = pathlib.Path(__file__).resolve().parent


def create_scene():
    """
    Create a scene with a Fuze bottle, some cubes, and an axis.
    Returns
    ----------
    scene : trimesh.Scene
      Object with geometry
    """
    scene = trimesh.Scene()

    # fuze
    geom = trimesh.load(str(here / './model.off'))
    transform = tf.translation_matrix([-0.1, -0.1, 0])
    scene.add_geometry(geom, transform=transform)

    return scene

class MyLabel(glooey.Label):
    custom_color = '#babdb6'
    custom_font_size = 10
    custom_alignment = 'center'

# If we want another kind of text, for example a bigger font for section
# titles, we just have to derive another class:

class MyTitle(glooey.Label):
    custom_color = '#eeeeec'
    custom_font_size = 12
    custom_alignment = 'center'
    custom_bold = True


class MyButton(glooey.Button):
    Foreground = MyLabel
    custom_alignment = 'fill'

    # More often you'd specify images for the different rollover states, but
    # we're just using colors here so you won't have to download any files
    # if you want to run this code.

    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#3465a4'

    class Down(glooey.Background):
        custom_color = '#729fcff'

    # Beyond just setting class variables in our widget subclasses, we can
    # also implement new functionality.  Here we just print a programmed
    # response when the button is clicked.

    def __init__(self, text, response):
        super().__init__(text)
        self.response = response

    def on_click(self, widget):
        print(self.response)


class Application:

    """
    Example application that includes moving camera, scene and image update.
    """

    def __init__(self):
        # create window with padding
        self.width, self.height = 1920, 1080
        window = self._create_window(width=self.width, height=self.height)

        gui = glooey.Gui(window)

        hbox = glooey.HBox()
        hbox.set_padding(5)

        # scene widget for changing camera location
        scene = create_scene()
        self.scene_widget1 = trimesh.viewer.SceneWidget(scene)
        # self.scene_widget1._angles = [np.deg2rad(45), 0, 0]
        hbox.add(self.scene_widget1)

        # scene widget for changing scene
        #
        '''
        scene = trimesh.Scene()
        geom = trimesh.path.creation.box_outline((0.6, 0.6, 0.6))
        scene.add_geometry(geom)
        self.scene_widget2 = trimesh.viewer.SceneWidget(scene)
        hbox.add(self.scene_widget2)
        '''
        # integrate with other widget than SceneWidget
        '''
        self.image_widget = glooey.Image()
        hbox.add(self.image_widget)
        '''
        note = glooey.Label(text='Note:\nRotate the view: Click mouse and drag.\nMove model: Click mouse and CTL, drag.\n Zoom in and out: Mouse wheel')
        control_pad = glooey.Grid(5,5)
        control_pad.custom_alignment = 'left'

        buttons = [
            MyButton('open','open'),
            MyButton('clean', 'clean'),
            MyButton('quit', 'quit'),
        ]

        i = 0
        for button in buttons:
            control_pad.add(i, 0, button)
            i+=1
        
        log_and_pad = glooey.VBox()
        hbox.add(log_and_pad)

        log_and_pad.add(note)
        log_and_pad.add(control_pad)

        gui.add(hbox)

        pyglet.clock.schedule_interval(self.callback, 1. / 20)
        pyglet.app.run()

    def callback(self, dt):
        # change camera location
        #self.scene_widget1._angles[2] += np.deg2rad(1)
        #self.scene_widget1.scene.set_camera(self.scene_widget1._angles)

        # change scene
        '''
        if len(self.scene_widget2.scene.graph.nodes) < 100:
            geom = trimesh.creation.icosphere(radius=0.01)
            geom.visual.face_colors = np.random.uniform(0, 1, (3,))
            geom.apply_translation(np.random.uniform(-0.3, 0.3, (3,)))
            self.scene_widget2.scene.add_geometry(geom)
            self.scene_widget2._draw()
        '''

        # change image
        '''
        image = np.random.randint(0,
                                  255,
                                  (self.height - 10, self.width // 3 - 10, 3),
                                  dtype=np.uint8)
        with io.BytesIO() as f:
            PIL.Image.fromarray(image).save(f, format='JPEG')
            self.image_widget.image = pyglet.image.load(filename=None, file=f)
        '''
    def _create_window(self, width, height):
        try:
            config = pyglet.gl.Config(sample_buffers=1,
                                      samples=4,
                                      depth_size=24,
                                      double_buffer=True)
            window = pyglet.window.Window(config=config,
                                          width=width,
                                          height=height)
        except pyglet.window.NoSuchConfigException:
            config = pyglet.gl.Config(double_buffer=True)
            window = pyglet.window.Window(config=config,
                                          width=width,
                                          height=height)

        @window.event
        def on_key_press(symbol, modifiers):
            if modifiers == 0:
                if symbol == pyglet.window.key.Q:
                    window.close()

        return window


if __name__ == '__main__':
    np.random.seed(0)
    Application()