remove_embedded_packages:
	find . -name \*-ItemFolder.zip -type f -delete
	find . -name \*-qti.zip -type f -delete
	find . -name \*-tv.zip -type f -delete
	find . -name \*.html -type f -delete

clean:
	rm build/ -rf

tarballs:
	python -c "import packaging; packaging.tarballs(zipped=False)"

tarballs_zipped:
	python -c "import packaging; packaging.tarballs(zipped=True)"

compile:
	python -c "import packaging; packaging.compilation_csv()"
	Rscript packaging/compile.R

webpage:
	cd build; \
	find ./ -type f -print0  | xargs -0 sha256sum > checksums.txt; \
	tree -H '.' -P "*.log|*.txt" \
		-L 1 --noreport --charset utf-8 \
		-T "Packages ($(shell date))" > index.html
