remove_itemfolder_zips:
	find . -name \*-ItemFolder.zip -type f -delete

clear:
	rm build/ -rf

tarballs:
	python -c "import packaging; packaging.tarballs(zipped=False)"

tarballs_zipped:
	python -c "import packaging; packaging.tarballs(zipped=True)"
