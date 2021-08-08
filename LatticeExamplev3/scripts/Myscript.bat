copy C:\Users\nshah5\source\repos\LatticeAutoGen\LatticeAutoGen.py C:\NNS\Backup\VmVare\LatticeExamplev3\LatticeExamplev3\AutoGen\LatticeAutoGen.py

pushd C:\NNS\Backup\VmVare\LatticeExamplev3\LatticeExamplev3\AutoGen

C:\Users\nshah5\AppData\Local\Programs\Python\Python39\python.exe LatticeAutoGen.py C:\NNS\Backup\VmVare\LatticeExamplev3\LatticeExamplev3\lib\lattice.h

popd

pause

rmdir /q /s C:\NNS\Backup\VmVare\LatticeExamplev3\LatticeExamplev3\build

pushd C:\NNS\Backup\VmVare\LatticeExamplev3\LatticeExamplev3

mkdir build
pushd build

"C:\Program Files\CMake\bin\cmake.exe" ..
"C:\Program Files\CMake\bin\cmake.exe" --build .
bin\Debug\latticeexample.exe

popd
popd


