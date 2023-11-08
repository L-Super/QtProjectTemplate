# configure version
configure_file(version.h.in ${CMAKE_CURRENT_SOURCE_DIR}/version.h @ONLY)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS
        Core
        Gui
        Widgets
)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)

add_executable(QtProjectTemplate main.cpp)

target_link_libraries(QtProjectTemplate
        Qt${QT_VERSION_MAJOR}::Core
        Qt${QT_VERSION_MAJOR}::Gui
        Qt${QT_VERSION_MAJOR}::Widgets
)
