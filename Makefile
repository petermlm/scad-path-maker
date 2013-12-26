all:
	cd src && ./test_path_maker.py ../testfiles/img1.in
	cd src && ./test_path_maker.py ../testfiles/img2.in
	cd src && ./test_path_maker.py ../testfiles/img3.in

clean:
	cd src && rm parser.out parsetab.py *.pyc

