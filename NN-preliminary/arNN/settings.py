settings = {
  "leaky_super_overfit" : {
    "hiddens": [50, 30, 30, 30, 30, 30, 50],
    "activations": ["leaky_relu", "leaky_relu", "leaky_relu", "leaky_relu", "leaky_relu", "leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 128,
    "patience": 500,
    "dropout_rate": 0      
  },
  "leaky_basic" : { 
    "hiddens": [30, 30, 30, 30],
    "activations": ["leaky_relu", "leaky_relu", "leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 32,
    "patience": 200,
    "dropout_rate": 0.1
  },
  "leaky_basic_2" : { 
    "hiddens": [30, 30, 30],
    "activations": ["leaky_relu", "leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 64,
    "patience": 200,
    "dropout_rate": 0.1
  },
  "leaky_basic_3" : {
    "hiddens": [20, 20],
    "activations": ["leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 64,
    "patience": 200,
    "dropout_rate": 0.1
  },
  "leaky_basic_4" : {
    "hiddens": [15, 15],
    "activations": ["leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1000,
    "batch_size": 64,
    "patience": 200,
    "dropout_rate": 0.1
  },
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
  "leaky_basic_6" : {
    "hiddens": [5, 5],
    "activations": ["leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1500,
    "batch_size": 64,
    "patience": 200,
    "dropout_rate": 0.1
  },
  "leaky_basic_7" : {
    "hiddens": [7, 7],
    "activations": ["leaky_relu", "leaky_relu"],
    "learning_rate": 0.001,
    "random_seed": 57,
    "max_epochs": 1500,
    "batch_size": 64,
    "patience": 200,
    "dropout_rate": 0.1
  }
}
