from transformers import MgpstrConfig, MgpstrForSceneTextRecognition

# Initializing a Mgpstr mgp-str-base style configuration
configuration = MgpstrConfig()

# Initializing a model (with random weights) from the mgp-str-base style configuration
model = MgpstrForSceneTextRecognition(configuration)

# Accessing the model configuration
configuration = model.config