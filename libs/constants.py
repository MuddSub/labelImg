####################################
SERVER_IP = 'http://134.173.43.20'  # exclude slash at the end
SERVER_PORT = '8080'
## Make sure to navigate to the compData directory on the server and run
## python -m http.server 8080
## to start the python webserver
####################################
####################################
baseServerUrl = SERVER_IP + ':' + SERVER_PORT + '/'
# baseLabelFolderUrl = baseServerUrl + 'labels/'
compDataUrl = baseServerUrl + 'compData/'
closingImgUrl = baseServerUrl + 'closingImg.png'
####################################

SETTING_FILENAME = 'filename'
SETTING_RECENT_FILES = 'recentFiles'
SETTING_WIN_SIZE = 'window/size'
SETTING_WIN_POSE = 'window/position'
SETTING_WIN_GEOMETRY = 'window/geometry'
SETTING_LINE_COLOR = 'line/color'
SETTING_FILL_COLOR = 'fill/color'
SETTING_ADVANCE_MODE = 'advanced'
SETTING_WIN_STATE = 'window/state'
SETTING_SAVE_DIR = 'savedir'
SETTING_PAINT_LABEL = 'paintlabel'
SETTING_LAST_OPEN_DIR = 'lastOpenDir'
SETTING_AUTO_SAVE = 'autosave'
SETTING_SINGLE_CLASS = 'singleclass'
FORMAT_PASCALVOC = 'PascalVOC'
FORMAT_YOLO = 'YOLO'
SETTING_DRAW_SQUARE = 'draw/square'
DEFAULT_ENCODING = 'utf-8'
