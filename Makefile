remove_embedded_packages:
	find . -name \*-ItemFolder.zip -type f -delete
	find . -name \*-qti.zip -type f -delete
	find . -name \*-tv.zip -type f -delete
	find . -name \*.html -type f -delete

clean:
	rm packages/ -rf

tarballs:
	python -c "import packaging; packaging.tarballs(zipped=False)"

tarballs_zipped:
	python -c "import packaging; packaging.tarballs(zipped=True)"

compile: packages/compl.instr
	Rscript packaging/compile.R

packages/compl.instr: # compilation instruction
	python -c "import packaging; packaging.compilation_file()"

webpage:
	cd packages; \
	rm compl.instr -f; \
	find ./ -type f -print0  | xargs -0 sha256sum > checksums.txt; \
	tree -H '.' \
		-L 2 --noreport --charset utf-8 \
		-T "Packages ($(shell date))" > index.html
