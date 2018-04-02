from neural_network import NeuralNetwork

def smoothen(prev_angle, curr_angle):
    diff_angle = curr_angle - prev_angle
    smoothed_angle = prev_angle + 0.2 * pow(abs(diff_angle), 2.0 / 3.0) * diff_angle / abs(diff_angle)
    return smoothed_angle

class LaneKeepingAssist(object):

    def __init__(self):
        self.network = NeuralNetwork()
        self.prev_angle = 0

    def predict_angle(self, frame):
        angle = network.predict(frame)
        angle = smoothen(angle)
        self.prev_angle = angle
        return angle

