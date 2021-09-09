import sys

from os.path import join
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment, COMMAND_LINE_TARGETS

env = DefaultEnvironment()

env.Append(
    ARFLAGS=["..."],

    ASFLAGS=["flag1", "flag2", "flagN"],
    CCFLAGS=["flag1", "flag2", "flagN"],
    CXXFLAGS=["flag1", "flag2", "flagN"],
    LINKFLAGS=["flag1", "flag2", "flagN"],

    CPPDEFINES=["DEFINE_1", "DEFINE=2", "DEFINE_N"],

    LIBS=["additional", "libs", "here"],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"]),
            suffix=".bin"
        )
    )
)

env.Replace(
    AR="ar",
    AS="gcc",
    CC="gcc",
    CXX="g++",
    OBJCOPY="objcopy",
    RANLIB="ranlib",

    UPLOADER=join("$PIOPACKAGES_DIR", "tool-bar", "uploader"),
    UPLOADCMD="$UPLOADER $SOURCES"
)

#target_elf = env.BuildProgram()
#target_bin = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)


#if "uploadble" in COMMAND_LINE_TARGETS:
#    sys.stdeff.write("Error: Function not implemented")
#    env.Exit(1)
