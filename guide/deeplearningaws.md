# Deep Learning on AWS
8 January, 2017

In this article you're going to learn how to setup a Deep Learning Server on Amazon so that you can run all of your favorite Neural Network models on the hardware you need. Not only that, I'll also show you how to setup a Jupyter Notebook Server to make neural network development much easier with a nice graphical interface.

This is an excellent alternative to buying your own GPU because it requires a fraction of the cost and you'll not have to deal with the headache of setting up a deep learning machine from scratch.

Furthermore, if you're a student in high school or college, you can easily get a bunch of free AWS credits from [AWS Educate](http://www.awseducate.com/)

This guide will use the AMI managed by Github user [Miej](https://github.com/Miej) which he calls [GoDeeper](https://github.com/Miej/GoDeeper). It has a bunch of really useful packages ranging from Tensorflow, Keras, Torch and even OpenCV so that you can run all of the cool researchy deep learning repos you desire with ease. Go to the repo link if you'd like to learn what else is in the document.

Now let's move on with the meat of this problem. If you were to go straight to running p2 instance in Northern Oregon, you'll start to burn through your AWS money quickly. However, there is a better method than simply launching instances. I typically use these things called spot requests. Basically, you bid for server time and the cost becomes significantly lower than the set pricing of regular instances. There's certainly a risk that setting a maximum bid will eventually cause you to be kicked off at any one moment, but I have never had this issue in the past and by setting a reasonably high max price you shouldn't run into this problem.

Amazon publishes the [current pricing](https://aws.amazon.com/ec2/spot/pricing/). For me in the US, the two closest regions that have p2 instances are North Virginia and Oregon. I've found that the cheaper region is never consistent, so you should definitely research the cheaper pricing if that's a concern for you or if you live in another regioin of the world. You can use the spot pricing tool to see whether any region has a p2 instance. If you see an N/A next to the p2 instance, that means this type of machine is not available in that region.

Now let's get onwards with it. To get started, you'll need to login to the AWS console. Here you'll want to
click Services, then EC2. At the top left you'll want to confirm that you are in a region that has gpu instances. I'll be using the Oregon region because it was the cheapest when I checked the spot pricing. On the left panel, navigate to Spot Requests and then click the Big Blue `Request Spot Instances`.

In the wizard, you'll want to go down to the AMI drop down and click Select. You'll be met with a window. Change the dropdown to `Community AMIs`. Now go to the [GoDeeper repo](https://github.com/Miej/GoDeeper) and find the specific ami id for the region you are in. Since I am using Oregon, I will use `ami-da3096ba
`.

Now you'll want to select the correct instance type. You'll want to remove the default instance type so that you have no conflicts and click the select button. Scroll down to the p2.xlarge option and select it.

Everything else should be set as default except the Maximum Price if you want to put a limit on how much you'll bid for an instance. I'll typically set the max price to the maximum price of the past week + a few cents of leeway. You can determine this price by clicking on the price history button that appears after you select `Set max price per hour`.

Click Next. You don't really need to worry about the size of the EBS volume here as the AMI already comes with 100GB. So change the volume as you please, note that larger volumes cost slightly more money.

Next you'll want to make a key-pair if you haven't already. Make sure that you save this somewhere you'll find later. However, make sure you don't add it to any publicly hosted git repos for privacy purposes. I typically save my keys in the `~/.ssh/` directory. Once you've moved the key you'll want to change the permissions to make the key safe. Simply run
```
sudo chmod ~/.ssh/<key-name> 400
```

Now you'll want to create a security group called Jupyter that has 3 inbound rules-
1. SSH
2. HTTPS
3. Custom TCP Rule - 8888

After you've set those, you'll want to make sure that you change the source to Anywhere for each option. Now maybe you'll want to set the exact source, however, this can be problematic if you plan to switch networks or you don't have a static ip on your network.

Return to the wizard, refresh the security groups panel and you should see your security group up. Select the checkbox next to it.

Finally, I'll set a timeout limit for the duration that the instance is valid until. This is just to make sure I don't accidentally leave the instance running for weeks on end, wracking up a bunch of charges on my account. I'll set mine to tomorrow because I won't be using this instance for very long today.

Click Next, then Launch Instance.

Now you'll want to confirm that the instance worked. Go to the instances tab in the left tab and you should see an instance up an running. In the bottom tab you'll see a description. Copy the public dns that you see in the description and navigate to your terminal.

You'll want to run the command
```
ssh -i /path/to/key.pem icarus@<amazon-dns>
```
it'll prompt you for the password, which is `changetheworld`
And you should finally have access!

## Setting up Jupyter
Now here comes the fun part, let's setup a Jupyter notebook for our server. I found this answer in a [Quora post](https://www.quora.com/How-do-I-create-Jupyter-notebook-on-AWS) a while back.

The steps here are simply run
```
git clone https://gist.github.com/philkuz/4b7fda8bc2eba4f9a1ba71c54321c126 nb
. nb/jupyter_notebook_ec2.sh
```
From this you'll be prompted to enter a password. Then you'll be given a series of questions about the certs. I just leave them as default as they are not important for our purposes.

Now run these commands
```
cd;mkdir notebook;cd notebook
tmux new -s nb
jupyter notebook --certfile=~/certs/mycert.pem --keyfile ~/certs/mycert.key
```

And with that setup, all you need to do is navigate to ```https://<ec2-public-dns>:8888``` and you'll have your notebook up and running and accessible! *Don't forget the `https` part of the url otherwise it wont' work*.

You'll be met with a self-signed cert error. You should be able to find a way past this with some sort of link on the page that comes up.

As a test of whether this works, I'll try to clone my repo [Neural Network Zoo](https://github.com/philkuz/Neural-Network-Zoo).

Start a new terminal, then enter
```
git clone https://github.com/philkuz/Neural-Network-Zoo
```
Once you see a success signal, close the window you are in, and you should see a new folder called `Neural-Network-Zoo`. Enter the folder and open any notebook you'd like, try running the cells and seeing if they work. On initial runs, it'll take some more time because the gpus have to be instantiated first, but you'll have no problems on later runs.
