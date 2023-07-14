remove_itemfolder_zips:
	find . -name \*-ItemFolder.zip -type f -delete

item_folder:
	python3 scripts/make_item_folder.py