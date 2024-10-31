# this script installs python and creates a python environment to run the Herbie
# downloads using RStudio

library(reticulate)

# activate conda env or create conda env and modules for the venv
tryCatch(use_condaenv(file.path(getwd(), 'herbie_env')),
         warning = function(w){
           print("conda environment activated")
         },
         error = function(e) {
           # install miniconda if necessary
           try(install_miniconda())
           #create a conda environment named 'herbie_env' with the packages you need
           conda_create(envname = file.path(getwd(), 'herbie_env'), 
                        python_version = 3.11)
           conda_install(envname = 'herbie_env/', 
                         packages = c('pandas', 'herbie-data', 'matplotlib', 
                                      'toolbox', 'numpy', 'xarray'))
           # set the new python environment
           use_condaenv(file.path(getwd(), "herbie_env/"))
           print("conda environment created and activated")
         }
)

