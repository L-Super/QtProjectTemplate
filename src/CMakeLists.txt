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

get_target_property(QMakeExecutable Qt${QT_VERSION_MAJOR}::qmake IMPORTED_LOCATION)
get_filename_component(QtBinDir "${QMakeExecutable}" DIRECTORY)
find_program(QT_DEPLOY_EXECUTABLE windeployqt macdeployqt HINTS "${QtBinDir}")

message(STATUS "Qt deployment tool: ${QT_DEPLOY_EXECUTABLE}")

qt_add_resources(QRC_FILES resources.qrc)

set(SRC_FILES MainWindow.cpp MainWindow.h MainWindow.ui)

if (WIN32)
    if (MSVC)
        # set MSVC utf-8 build
        add_compile_options(/utf-8)
    endif ()

    set(SRC_FILES ${SRC_FILES} resources/app.rc)

    if (CMAKE_BUILD_TYPE STREQUAL "Debug")
        message(STATUS "Running ${CMAKE_BUILD_TYPE} mode")
        set(CONSOLE "")
    else ()
        message(STATUS "Running ${CMAKE_BUILD_TYPE} mode")
        # Remove the terminal display
        set(CONSOLE WIN32)
    endif ()
endif ()

add_executable(QtProjectTemplate
        ${CONSOLE}
        main.cpp
        ${QRC_FILES}
        ${SRC_FILES}
)

if (APPLE)
    set_target_properties(QtProjectTemplate PROPERTIES MACOSX_BUNDLE TRUE)
endif ()

target_link_libraries(QtProjectTemplate
        Qt${QT_VERSION_MAJOR}::Core
        Qt${QT_VERSION_MAJOR}::Gui
        Qt${QT_VERSION_MAJOR}::Widgets
)

if (WIN32)
    add_custom_command(TARGET ${PROJECT_NAME}
            POST_BUILD
            # Deploy the Qt Application
            COMMAND ${QT_DEPLOY_EXECUTABLE}
            # --no-translations
            "$<TARGET_FILE:${PROJECT_NAME}>"
    )
elseif (APPLE)
    # TODO:
    # configure_file(${CMAKE_SOURCE_DIR}/Info.plist.in ${CMAKE_BINARY_DIR}/Info.plist)
    # set_target_properties(${PROJECT_NAME} PROPERTIES MACOSX_BUNDLE_INFO_PLIST ${CMAKE_BINARY_DIR}/Info.plist)

    add_custom_command(TARGET ${PROJECT_NAME}
            POST_BUILD
            COMMAND ${QT_DEPLOY_EXECUTABLE}
            $<TARGET_BUNDLE_DIR:${PROJECT_NAME}>
            # -dmg
    )
endif ()