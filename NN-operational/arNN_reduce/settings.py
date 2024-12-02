settings = {
  "leaky_basic_5" : {
    "hiddens": [10, 10],
    "activations": ["leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 64,
    "patience": 200,
    "dropout_rate": 0.1
  },
  "leaky_5_long" : {
    "hiddens": [10, 10],
    "activations": ["leaky_relu", "leaky_relu"],
    "learning_rate": 0.01,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 64,
    "patience": 200,
    "dropout_rate": 0.1
  },
  "leaky_5_batch" : {
    "hiddens": [10, 10],
    "activations": ["leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 128,
    "patience": 200,
    "dropout_rate": 0.2
  }
}
