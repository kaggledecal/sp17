# Docker Cheatsheet
This a cheatsheet that will cover most of the commands/situation you will encounter in this class!





## Starting a jupyter container
**Start a jupyter notebook container without mounting a directory**

`docker run -d -p 8888:8888 jupyter/scipy-notebook`

**Start a jupyter container with your current directory mounted**

`docker run -d -p 8888:8888 -v "$(pwd)":/home/jovyan/work jupyter/scipy-notebook`

*Notes*
* Do not change `/home/jovyan/work`. This is a setting for the container

## Stopping a container
To stop a container, you'll first need to figure out the container name. To find a list of running containers simply run: 

`docker ps`

and you'll get output that looks like this 
```
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                    NAMES
a564ee08a199        jupyter/scipy-notebook   "tini -- start-notebo"   2 hours ago         Up 2 hours          0.0.0.0:8888->8888/tcp   sharp_dijkstra
```

Got to the NAMES column, copy the name (sharp_dijkstra in this case), then paste it in this command

`docker stop <image-name>`

For the example this would be `docker stop sharp_dijkstra`.

## Restarting a stopped Image
Using the same image name, 

`docker start <image-name>`

## Removing a stopped Image
Using the same image name as before

`docker rm <image-name>`

*Notes* 
* Usually you'll want to remove an image way after it's been stopped. To get a list of all stopped containers, you'll want to add the `-a` flag to `docker ps` as so
`docker ps -a`


# FAQs
* ```docker: Error response from daemon: driver failed programming external connectivity on endpoint modest_turing (96452e3e228f072c778ba9c91d7c95c232ad166cae85f14d44efa43c57363bcf): Bind for 0.0.0.0:8888 failed: port is already allocated.```

This usually means you already have a jupyter container running (or are running a jupyter server separately that is already serving port 8888). All you need to do is stop the previous container to start a new one.

* ```docker: Error parsing reference: "\u00add" is not a valid repository/tag See 'docker run --help'. ```

Our apologies for this! This is what happens when PDFs encode hyphens apparently. All you need to do for this is copy the start container command from above and this issue will disappear

* I am on windows and `X` keeps happening.
You can find us during office hours or take the easy way out and [install anaconda](https://www.continuum.io/downloads)

![Windoze troll](https://i.imgflip.com/1amtdy.jpg)
