# hello
#g
cmake_minimum_required(VERSION 3.10)
project(hello CXX)
add_executable(hello)
target_sources(hello PRIVATE hello.cpp)
target_compile_features(hello PRIVATE cxx_std_20)
