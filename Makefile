run:
	.venv/bin/python lnkmngr/app.py

# run on windows
runw:
	DB_PATH="C:\\Users\\auppal\\dev\\pfin2\\pfin-input-data\\sqlite_db\\lnkmngr.db" \
	.venv/Scripts/python lnkmngr/app.py 

genexew:
	rm -rf lnkmngr/build lnkmngr/dist lnkmngr/app.spec; \
	cd lnkmngr; \
	../.venv/Scripts/pyinstaller -F \
	--add-data "templates;templates" --add-data "static;static" \
	--runtime-tmpdir ./ app.py; \
	mv dist/app.exe ../exe/lnkmngr.exe

genexewau:
	cp tmp/consts_au.py lnkmngr/utils/consts.py; \
	rm -rf lnkmngr/build lnkmngr/dist lnkmngr/app.spec; \
	cd lnkmngr; \
	../.venv/Scripts/pyinstaller -F \
	--add-data "templates;templates" --add-data "static;static" \
	--runtime-tmpdir ./ app.py; \
	mv dist/app.exe ../exe/au/lnkmngr.exe; \
	git checkout utils/consts.py; \
	cp ../exe/au/lnkmngr.exe ~/apps/lnkmngr.exe

genexe: genexewau genexew

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
