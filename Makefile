IPADDR := $(shell ip -f inet addr show docker0 | grep -Po 'inet \K[\d.]+')
PROXYBIND := "http://$(IPADDR):1081"
USER := $(shell whoami)

all:
	sudo docker build --build-arg http_proxy=$(PROXYBIND) \
		--build-arg https_proxy=$(PROXYBIND) \
		-t ssfdust/yt-media .

services:
	sudo systemctl start postgresql rabbitmq redis

services-off:
	sudo systemctl stop postgresql rabbitmq redis

pull:
	podman-compose pull

up:
	podman unshare chown 1000 -R .
	podman-compose up -d

down:
	sudo chown $(USER) -R .
	podman-compose down

stop:
	sudo chown $(USER) -R .
	podman-compose stop

start:
	podman unshare chown 1000 -R .
	podman-compose start
