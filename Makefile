all:
	cd src && ./path_maker.py ../testfiles/img1.svg
	cd src && ./path_maker.py ../testfiles/img2.svg

clean:
	cd src && rm parser.out parsetab.py parsetab.pyc

