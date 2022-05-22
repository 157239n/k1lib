
# Regression testing over multiple Python versions

To run a test, execute `./build.sh`. This will:
- Remove every previous test outputs from folder `test-outputs/`
- Build the common base container
- Go into each `py3.*` folder, executes `./build.sh` in there. This will:
	- Install specific python versions
	- Install pytorch compatible with that python version. Usually containers are cached up until here
	- Install k1lib
	- Run test (file `test.py`) and dumps output to file `test-outputs/Python 3.9.7` and such

After that is done, you can inspect the outputs in folder `test-outputs/`. If there's something wrong, you can execute `py3.*/enter.sh` to go into the specific container. A log file at `/base/log` should tell you what went wrong.

If everything is perfect, you can execute `./down.sh` to shutdown all containers, to save resources.

For quick debugging, you can also do `./build.sh 1` to execute just the first stage.

