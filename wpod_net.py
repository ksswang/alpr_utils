import mxnet as mx


class ResBlock(mx.gluon.nn.Block):
    def __init__(self, channels, **kwargs):
        super(ResBlock, self).__init__(**kwargs)
        self._block = mx.gluon.nn.Sequential()
        with self.name_scope():
            self._block.add(
                mx.gluon.nn.Conv2D(channels, 3, 1, 1),
                mx.gluon.nn.BatchNorm(1, 0.99, 0.001),
                mx.gluon.nn.Activation("relu"),
                mx.gluon.nn.Conv2D(channels, 3, 1, 1),
                mx.gluon.nn.BatchNorm(1, 0.99, 0.001),
            )

    def forward(self, x):
        return mx.nd.relu(self._block(x) + x)


class Detection(mx.gluon.nn.Block):
    def __init__(self, **kwargs):
        super(Detection, self).__init__(**kwargs)
        with self.name_scope():
            self._classify = mx.gluon.nn.Conv2D(2, 3, 1, 1)
            self._affine = mx.gluon.nn.Conv2D(6, 3, 1, 1)

    def forward(self, x):
        return mx.nd.concat(
            mx.nd.softmax(self._classify(x), axis=1),
            self._affine(x),
            dim=1
        )


class WpodNet(mx.gluon.nn.Block):
    def __init__(self, **kwargs):
        super(WpodNet, self).__init__(**kwargs)
        self._block = mx.gluon.nn.Sequential()
        with self.name_scope():
            self._block.add(
                mx.gluon.nn.Conv2D(16, 3, 1, 1),
                mx.gluon.nn.BatchNorm(1, 0.99, 0.001),
                mx.gluon.nn.Activation("relu"),
                mx.gluon.nn.Conv2D(16, 3, 1, 1),
                mx.gluon.nn.BatchNorm(1, 0.99, 0.001),
                mx.gluon.nn.Activation("relu"),
                mx.gluon.nn.MaxPool2D(2),
                mx.gluon.nn.Conv2D(32, 3, 1, 1),
                mx.gluon.nn.BatchNorm(1, 0.99, 0.001),
                mx.gluon.nn.Activation("relu"),
                ResBlock(32),
                mx.gluon.nn.MaxPool2D(2),
                mx.gluon.nn.Conv2D(64, 3, 1, 1),
                mx.gluon.nn.BatchNorm(1, 0.99, 0.001),
                mx.gluon.nn.Activation("relu"),
                ResBlock(64),
                ResBlock(64),
                mx.gluon.nn.MaxPool2D(2),
                ResBlock(64),
                ResBlock(64),
                mx.gluon.nn.MaxPool2D(2),
                mx.gluon.nn.Conv2D(128, 3, 1, 1),
                mx.gluon.nn.BatchNorm(1, 0.99, 0.001),
                mx.gluon.nn.Activation("relu"),
                ResBlock(128),
                ResBlock(128),
                Detection()
            )

    def forward(self, x):
        return self._block(x).transpose((0, 2, 3, 1))


def wpod_loss(pred, label):
    obj_pred = pred[:, :, :, 0]
    obj_label = label[:, :, :, 0]
    bg_pred = pred[:, :, :, 1]
    bg_label = 1 - obj_label
    log_loss = mx.gluon.loss.LogisticLoss(label_format="binary")
    classify_L = log_loss(obj_pred, obj_label) + log_loss(bg_pred, bg_label)
    affine = mx.nd.concat(
        mx.nd.concat(
            mx.nd.relu(pred[:, :, :, 2:3]),
            pred[:, :, :, 3:4],
            pred[:, :, :, 4:5],
            dim=3
        ).expand_dims(3),
        mx.nd.concat(
            pred[:, :, :, 5:6],
            mx.nd.relu(pred[:, :, :, 6:7]),
            pred[:, :, :, 7:8],
            dim=3
        ).expand_dims(3),
        dim=3
    )
    unit = mx.nd.array(
        [[-0.5, -0.5, 1], [0.5, -0.5, 1], [0.5, 0.5, 1], [-0.5, 0.5, 1]],
        ctx=pred.context
    ).T.reshape((1, 1, 1, 3, 4)).tile(pred.shape[:3] + (1, 1))
    points_pred = mx.nd.batch_dot(
        affine.reshape((-1, 2, 3)),
        unit.reshape((-1, 3, 4))
    ).reshape(pred.shape[:3] + (-1,))
    points_label = label[:, :, :, 1:]
    mask = obj_label.expand_dims(3)
    l1_loss = mx.gluon.loss.L1Loss()
    affine_L = l1_loss(points_pred * mask, points_label * mask)
    return classify_L + affine_L


if __name__ == "__main__":
    net = WpodNet()
    net.initialize(mx.init.Xavier())
    print(net)
    pred = net(mx.nd.random_uniform(shape=(4, 3, 256, 256)))
    print(pred)
    print(wpod_loss(pred, mx.nd.random_uniform(shape=(4, 16, 16, 9))))