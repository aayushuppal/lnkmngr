run:
	.venv/bin/python lnkmngr/app.py

# run on windows
runw:
	.venv/Scripts/python lnkmngr/app.py 

genexe:
	rm -rf lnkmngr/build lnkmngr/dist lnkmngr/app.spec; \
	cd lnkmngr; \
	../.venv/Scripts/pyinstaller -F \
	--add-data "templates;templates" --add-data "static;static" \
	--runtime-tmpdir ./ app.py; \
	mv dist/app.exe ../exe/lnkmngr.exe; \
	cp ../exe/lnkmngr.exe ~/apps/lnkmngr.exe

genmac:
	rm -rf lnkmngr/build lnkmngr/dist lnkmngr/app.spec; \
	cd lnkmngr; \
	../.venv/bin/pyinstaller --windowed -F \
	--add-data "templates:templates" --add-data "static:static" \
	--runtime-tmpdir ./ app.py

clean:
	rm -rf lnkmngr/build lnkmngr/dist lnkmngr/app.spec

setup:
	rm -rf .venv
	python3.7 -m venv .venv
	.venv/bin/pip install -r requirements.txt
