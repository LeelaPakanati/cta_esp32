DEVICE := /dev/ttyUSB1
DIRS := train_api/
FILES := $(wildcard *.py) $(wildcard train_api/*.py)
TARGETS := $(FILES:.py=)

all : $(TARGETS)

% : %.py
	echo $^
	#sudo mpremote connect $(DEVICE) cp $^:$^

dirs :
	for DIR in $(DIRS); do  \
		sudo mpremote connect $(DEVICE) mkdir $$DIR ;\
	done

flash :
	sudo ./utils/flash_fw.sh $(DEVICE)
