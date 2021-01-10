from app import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Intro')
        Text('Scene 0', pos=(10, 20))
        Text('Introduction screen the app', pos=(20, 20))

        Scene(bg=Color('yellow'), caption='Options')
        Text('Scene 1', pos=(10, 20))
        Text('Option screen of the app', pos=(20, 20))

        Scene(bg=Color('green'), caption='Main')
        Text('Scene 2', pos=(10, 20))
        Text('Main screen of the app', pos=(20, 20))

        App.scene = App.scenes[0]



if __name__ == '__main__':
    Demo().run()