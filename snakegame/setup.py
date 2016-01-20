import cx_Freeze
executables = [cx_Freeze.Executable("firstgame.py")]

cx_Freeze.setup(
	name = "Slither",
	options = {"build_exe" : {"packages" : ["pygame"], "include_files" : ["snakeimage.jpg","appleimage.jpg"]}},
	description = "Slither Game",
	executables = executables
	)