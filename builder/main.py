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


target_elf = env.BuildProgram()
target_hex = env.ElfToHex(join("$BUILD_DIR", "firmware"), target_elf)

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

Default(target_hex)
