remove_itemfolder_zips:
	find . -name \*-ItemFolder.zip -type f -delete

clear:
	rm build/ -rf

tarballs:
	python -c "import packaging; packaging.tarballs(zipped=False)"

tarballs_zipped:
	python -c "import packaging; packaging.tarballs(zipped=True)"

webpage:
	cd build; \
	find ./ -type f -print0  | xargs -0 sha256sum > checksums.txt; \
	tree -H '.' -P "*.tar|*.zip|*.txt" \
		-L 4 --noreport --charset utf-8 \
		-T "Packages ($(shell date))" > index.html
