all: clean test build

test:
	-python -m unittest tests/test_pyslack.py 

build:
	@mkdir -p dist/python
	@cp libpyslack/core.py dist/python/libpyslack.py
	@cd dist && \
	zip -r libpyslack.zip python

clean:
	-rm -rf ./dist

.PHONY: clean test build
