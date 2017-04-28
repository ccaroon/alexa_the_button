test: secrets clean
	python -m unittest discover -v -s tests

secrets: secrets.py

secrets.py:
	echo "Looks like you need to create the secrets.py file."
	exit 1

package: alexa_button_package.zip

alexa_button_package.zip: secrets.py the_button.py
	rm -f alexa_button_package.zip
	mkdir package
	cp secrets.py the_button.py package
	cp -a venv/lib/python2.7/site-packages/requests package
	cd package && zip -r ../alexa_button_package.zip * && cd ..
	rm -rf package/

clean:
	rm -rf package/
	rm -f alexa_button_package.zip
	rm -f *.pyc
