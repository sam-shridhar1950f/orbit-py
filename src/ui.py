from guizero import *

app = App(title='test')
message = Text(app, text='test orbit ui', size=40)
def earth_preset():
    print('Earth Preset Picked')

presetButton = PushButton(master=app, command=earth_preset, text='Earth')


app.display()
