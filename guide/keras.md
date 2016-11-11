# Keras Installation Guide
## The Docker Way
If you're one of the many students we got to install Docker at the beginning of the semester, you're in luck! Installing Keras can be as simple as running a single command.

In your terminal, all you need to run is
```
docker run -d -p 8888:8888 ermaker/keras-jupyter
```
If you want to mount the current directory, use 
```
docker run -d -p 8888:8888 -v $(pwd):/notebook ermaker/keras-jupyter
```
and you're done! The docker daemon will install the keras container, and all you need is to load up localhost:8888 to open it with the jupyter notebook server!

## The other way
Now setting up Keras without Docker is a little more involved. Fortunately, the python package management system makes things a little easier.

Before you go and pip install, however, you'll want to configure the "backend" for Keras. The great thing about Keras' setup is that you have the option to use two different deep learning backends: Tensorflow or Theano.
### Mac/Linux
You'll want to install TensorFlow before you install Keras. As long as you have pip installed, all you need to do is find the matching binary to install, and run the appropriate command.

I've added a list of relevant lines here, however there's also instructions for other [hardwares and python versions](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html).
```
# Ubuntu/Linux 64-bit, CPU only, Python 3.4
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0rc2-cp34-cp34m-linux_x86_64.whl

# Ubuntu/Linux 64-bit, CPU only, Python 3.5
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0rc2-cp35-cp35m-linux_x86_64.whl

# Mac OS X, CPU only, Python 3.4 or 3.5:
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.11.0rc2-py3-none-any.whl
```

After running this command, then simply run
```
pip install tensorflow keras
```
So if I were installing this on my Mac OS w/o a CPU, the set of commands would simply be
```
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.11.0rc2-py3-none-any.whl
pip install tensorflow keras
```

### Windows
```
sudo pip install keras
```
If you're on windows, unfortunately you'll not be able to use Tensorflow on your machine. However, you can still install the docker container above!

Even then, Theano will still install and will be perfectly fine for the work we'll be doing. However in the future you'll probably want to switch over to Tensorflow because it's benchmarks are significantly faster than Theano's.
