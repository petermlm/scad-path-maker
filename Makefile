all:
	cd src && ./path_maker.py ../testfiles/img1.svg ../testfiles/img1.out
	cd src && ./path_maker.py ../testfiles/img2.svg ../testfiles/img2.out
	cd src && ./path_maker.py ../testfiles/img3.svg ../testfiles/img3.out

clean:
	cd src && rm parser.out parsetab.py parsetab.pyc
	cd testfiles && rm *.out

