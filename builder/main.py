import sys

from os.path import join
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment, COMMAND_LINE_TARGETS

env = DefaultEnvironment()

env.Append(
    BUILDERS=dict(
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "$SOURCES",
                "$TARGET"
            ]), "Buidling $TARGET"),
            suffix=".hex"
        ),
        # step 2
        #SetLinkerFiles=Builder(
        #    action=env.VerboseAction("$CC -CC -E -P -x c -I$MICROAPPS_INCLUDE $MICROAPPS_SYMBOLS_INPUT -o $MICROAPPS_SYMBOLS_OUTPUT",
        #     "Building"),
        #    suffix=".tmp"
        #),
        # step 3
        #CompileWithoutHeaders=Builder(
        #    action=env.VerboseAction(
        #    "",
        #     "Buidling $TARGET"),
        #    suffix=".elf.tmp"
        #),
        MergeHex=Builder(
            action=env.VerboseAction(" ".join([
                join(platform.get_package_dir("tool-sreccat") or "",
                     "srec_cat"),
                "$SOFTDEVICEHEX",
                "-intel",
                "$SOURCES",
                "-intel",
                "-o",
                "$TARGET",
                "-intel",
                "--line-length=44"
            ]), "Building $TARGET"),
            suffix=".hex"
        )


    )
)

env.Replace(
    AR="ar",
    AS="gcc",
    CC="gcc",
    CXX="g++",
    OBJCOPY="objcopy",
)

env.Replace(
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy",
)

#################
# Building steps
################

# Set linker files
env.VerboseAction(
    "$CC -CC -E -P -x c -I$MICROAPPS_INCLUDE $MICROAPPS_SYMBOLS_INPUT -o $MICROAPPS_SYMBOLS_OUTPUT",
    "Building linker files"
) 

# Build elf file
target_elf = env.BuildProgram()

#################
# Uploader
#################

upload_protocol = env.subst("$UPLOAD_PROTOCOL")

if upload_protocol == "microapp":
    env.Replace(
        UPLOADER="nrfjprog",
        UPLOADERFLAGS=[
            "--sectorerase" if "DFUBOOTHEX" in env else "--chiperase",
        ],
        UPLOADCMD="$UPLOADER -f nrf52 --program $SOURCE --sectorerase --reset"
    )
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]
else:
    print("Unknown upload protocol")

Default(target_elf)
