from PyQt5.QtWidgets import QCheckBox, QFrame

from frames.group import Ui_FrameGroup


class QFrameGroup(QFrame, Ui_FrameGroup):
    def __init__(self, parent, values):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        Ui_FrameGroup.setupUi(self, self)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.values = values
        self.cbs = []
        for idx, value in enumerate(values):
            cb = QCheckBox(value, self)
            cb.setChecked(1)
            cb.stateChanged.connect(self.state_changed)
            self.cbs.append(cb)
            self.scroll_contents.layout().insertWidget(idx, cb)

        self.signal_func = None

    def get_turned(self):
        pressed = [cb.isChecked() for cb in self.cbs]
        values_pressed = []
        for p, v in zip(pressed, self.values):
            if p:
                values_pressed.append(v)
        return values_pressed

    def state_changed(self, state):
        if self.signal_func is not None:
            self.signal_func(self.get_turned())
