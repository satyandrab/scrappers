Requirements
python27
lxml

Download zip folder, extract it at known location,

--Open terminal

--Reach to project directory

-- two scripts available which need to run
	-Run following command to extract all games ids
	python extract_game_id.py
	after running command please verify file "id_file.txt" to confirm that it contains all games id from 358 pages of https://steamdb.info/apps
	
	-Run folloing command to get data from all ids in file "id_file.txt"
	python steampowered.py
	--It will ask you to enter file name, data will be saved in entered file which can be find in "imported_data" folder
	--After entering file name it will pick ids from file and start extracting data for games.

Point to remember
-Internet should be connected
-Website should up and running
-URL should be correct
-Don't close terminal until script complete