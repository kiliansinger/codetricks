!install with: 
!linux/win:     sudo apt update
!               sudo apt install gfortran gdb
!osx:          brew install gcc gdb
!compile with:  gfortran -o hellof95 hellof95.f95
Program Hello
    Print *, "Hello World!"
End Program