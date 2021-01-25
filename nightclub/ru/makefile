.PHONY: all clean

MO_DIR = locale\ru\LC_MESSAGES
MO = $(MO_DIR)\messages.mo
PO = $(MO_DIR)\messages.po

DEL = @del /F /Q

all: $(MO)

$(MO): $(PO)
	msgfmt --output-file=$(MO) $(PO)
clean:
	@if exist $(MO) $(DEL) $(MO) >nul
