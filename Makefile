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
	 find lnkmngr -name "*.pyc" -exec rm -rf {} \;
	 find lnkmngr -name "__pycache__" -exec rm -rf {} \;
	 rm -rf  .pytest_cache

setup:
	rm -rf .venv
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

setupw:
	rm -rf .venv
	python -m venv .venv
	.venv/Scripts/pip install -r requirements.txt
