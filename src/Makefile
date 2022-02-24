PORT = /dev/ttyUSB0
AMPY = ampy -p $(PORT)
MPYCROSS = mpy-cross

SRC = \
	mpu6050.py \
	constants.py \
	cfilter.py \
	DS3231.py \
	sdcard.py \
	logger.py \
	filters.py \
	deltat.py \
	fusion.py

OBJ = $(SRC:.py=.mpy)

STATIC = main.py boot.py

%.mpy: %.py
	$(MPYCROSS) -o $@ $<

all: $(OBJ)

install: .lastbuild

.lastbuild: $(OBJ) $(STATIC)
	set -x; for src in $?; do $(AMPY) put $$src; done
	date > .lastbuild
	$(AMPY) reset


.PHONY: reset clean

reset:
	$(AMPY) reset

clean:
	rm -f .lastbuild $(OBJ)
