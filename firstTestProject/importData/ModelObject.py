class ModelObject:
    """
    Class to handle all parameters for training a simple model and find best fit
    for all hyper parameters.
    """
    def __init__(self):
        # used for training
        self.trainX = None
        self.trainY = None
        # used for testing to find best fit
        self.testX = None
        self.testY = None
        # used to validate model to prevent overfitting.
        self.validX = None
        self.validY = None

        # Scikit-learn scalar to normalize data
        self.Scalar = None

        # keras/tensorflow model
        self.model = None

        # measured error
        self.validError = None

    def saveModelObject(self):
        return

    def loadModelObject(self):
        return