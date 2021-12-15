# run on windows
runw:
	DB_PATH="C:\\Users\\auppal\\dev\\pfin2\\pfin-input-data\\sqlite_db\\lnkmngr.db" \
	.venv/Scripts/python lnkmngr/app.py 

run:
	.venv/bin/python lnkmngr/app.py

genexew:
	rm -rf lnkmngr/build lnkmngr/dist lnkmngr/app.spec; \
	cd lnkmngr; \
	../.venv/Scripts/pyinstaller -w -F \
	--add-data "templates;templates" --add-data "static;static" \
	--runtime-tmpdir ./ app.py

clean:
	rm -rf lnkmngr/build lnkmngr/dist lnkmngr/app.spec
