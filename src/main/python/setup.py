from cx_Freeze import setup, Executable

import sys

path = sys.path  # .append(os.path.join("..", "..", "biblio"))
# options d'inclusion/exclusion des modules
includes = []
excludes = []

# option d'inclusion des packages
packages = [
    "Modules/MM",
    "Modules/arduinoComm",
    "Modules/fileUtility",
    "Modules/imageFunctions",
    "Modules/pyTracer",
    "Modules/threads",
    "GUI/autoFocusUI",
    "GUI/counterControlUI",
    "GUI/countGraphUI",
    "GUI/experimentControlUI",
    "GUI/guiMain",
    "GUI/lasersControlUI",
    "GUI/viewerUI",
    "GUI/Widgets/acquisitionControl",
    "GUI/Widgets/acquisitionControlPALM",
    "GUI/Widgets/autoFocus",
    "GUI/Widgets/batchPopUp",
    "GUI/Widgets/cameraSettings",
    "GUI/Widgets/counterControl",
    "GUI/Widgets/counterGraph",
    "GUI/Widgets/histCommands",
    "GUI/Widgets/histPlot",
    "GUI/Widgets/imageDisplay",
    "GUI/Widgets/imageViewerUI",
    "GUI/Widgets/lasersControl",
    "GUI/Widgets/microscopeSettings"
]

# copier les fichiers non-py et non-pyw et/ou repertoires et leur contenu:
includefiles = []

# pour que certaines bibliotheques "systeme" soient recopiees aussi
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes
           }

# pour inclure sous Windows les dll system necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True

#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    # base = "Win32GUI"  # pour des programmes graphiques sous Windows
    base = "Console" # pour des programmes en console sous Windows

icone = None
if sys.platform == "win32":
    icone = None  # mettre ici le fichier de l' icone .ico pour integration a l'exe

target = Executable(
    script="main.py",
    base=base,
    icon=icone
)

#############################################################################
# creation du setup
setup(
    name = "CryoPALM",
    version = "1.0",
    description = "",
    author = "William Magrini",
    options = {"build_exe": options},
    executables = [target]
    )