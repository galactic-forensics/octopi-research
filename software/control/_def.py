import os
import glob
import numpy as np
from pathlib import Path

class TriggerMode:
    SOFTWARE = 'Software Trigger'
    HARDWARE = 'Hardware Trigger'
    CONTINUOUS = 'Continuous Acqusition'

class Acquisition:
    CROP_WIDTH = 3000
    CROP_HEIGHT = 3000
    NUMBER_OF_FOVS_PER_AF = 3
    IMAGE_FORMAT = 'bmp'
    IMAGE_DISPLAY_SCALING_FACTOR = 0.25
    DX = 0
    DY = 0
    DZ = 0

class PosUpdate:
    INTERVAL_MS = 25

class MicrocontrollerDef:
    MSG_LENGTH = 24
    CMD_LENGTH = 8
    N_BYTES_POS = 4

class CMD_SET:
    MOVE_X = 0
    MOVE_Y = 1
    MOVE_Z = 2
    MOVE_THETA = 3
    HOME_OR_ZERO = 5
    TURN_ON_ILLUMINATION = 10
    TURN_OFF_ILLUMINATION = 11
    SET_ILLUMINATION = 12
    SET_ILLUMINATION_LED_MATRIX = 13
    ACK_JOYSTICK_BUTTON_PRESSED = 14
    MOVETO_X = 6
    MOVETO_Y = 7
    MOVETO_Z = 8

BIT_POS_JOYSTICK_BUTTON = 0
BIT_POS_SWITCH = 1

class HOME_OR_ZERO:
    HOME_NEGATIVE = 1 # motor moves along the negative direction (MCU coordinates)
    HOME_POSITIVE = 0 # motor moves along the negative direction (MCU coordinates)
    ZERO = 2

class AXIS:
    X = 0
    Y = 1
    Z = 2
    THETA = 3
    XY = 4

class ILLUMINATION_CODE:
    ILLUMINATION_SOURCE_LED_ARRAY_FULL = 0;
    ILLUMINATION_SOURCE_LED_ARRAY_LEFT_HALF = 1
    ILLUMINATION_SOURCE_LED_ARRAY_RIGHT_HALF = 2
    ILLUMINATION_SOURCE_LED_ARRAY_LEFTB_RIGHTR = 3
    ILLUMINATION_SOURCE_LED_EXTERNAL_FET = 20
    ILLUMINATION_SOURCE_405NM = 11
    ILLUMINATION_SOURCE_488NM = 12
    ILLUMINATION_SOURCE_638NM = 13
    ILLUMINATION_SOURCE_561NM = 14

class CAMERA:
    ROI_OFFSET_X_DEFAULT = 0
    ROI_OFFSET_Y_DEFAULT = 0
    ROI_WIDTH_DEFAULT = 3000
    ROI_HEIGHT_DEFAULT = 3000

class VOLUMETRIC_IMAGING:
    NUM_PLANES_PER_VOLUME = 20

class CMD_EXECUTION_STATUS:
    COMPLETED_WITHOUT_ERRORS = 0
    IN_PROGRESS = 1
    CMD_CHECKSUM_ERROR = 2
    CMD_INVALID = 3
    CMD_EXECUTION_ERROR = 4
    ERROR_CODE_EMPTYING_THE_FLUDIIC_LINE_FAILED = 100

###########################################################
#### machine specific configurations - to be overridden ###
###########################################################
ROTATE_IMAGE_ANGLE = None
FLIP_IMAGE = None # 'Horizontal', 'Vertical', 'Both'

# change the following so that "backward" is "backward" - towards the single sided hall effect sensor
STAGE_MOVEMENT_SIGN_X = -1
STAGE_MOVEMENT_SIGN_Y = 1
STAGE_MOVEMENT_SIGN_Z = 1
STAGE_MOVEMENT_SIGN_THETA = 1

STAGE_POS_SIGN_X = STAGE_MOVEMENT_SIGN_X
STAGE_POS_SIGN_Y = STAGE_MOVEMENT_SIGN_Y
STAGE_POS_SIGN_Z = STAGE_MOVEMENT_SIGN_Z
STAGE_POS_SIGN_THETA = STAGE_MOVEMENT_SIGN_THETA

TRACKING_MOVEMENT_SIGN_X = 1
TRACKING_MOVEMENT_SIGN_Y = 1
TRACKING_MOVEMENT_SIGN_Z = 1
TRACKING_MOVEMENT_SIGN_THETA = 1

USE_ENCODER_X = False
USE_ENCODER_Y = False
USE_ENCODER_Z = False
USE_ENCODER_THETA = False

ENCODER_POS_SIGN_X = 1
ENCODER_POS_SIGN_Y = 1
ENCODER_POS_SIGN_Z = 1
ENCODER_POS_SIGN_THETA = 1

ENCODER_STEP_SIZE_X_MM = 100e-6
ENCODER_STEP_SIZE_Y_MM = 100e-6
ENCODER_STEP_SIZE_Z_MM = 100e-6
ENCODER_STEP_SIZE_THETA = 1

FULLSTEPS_PER_REV_X = 200
FULLSTEPS_PER_REV_Y = 200
FULLSTEPS_PER_REV_Z = 200
FULLSTEPS_PER_REV_THETA = 200

SCREW_PITCH_X_MM = 1
SCREW_PITCH_Y_MM = 1
SCREW_PITCH_Z_MM = 0.012*25.4

MICROSTEPPING_DEFAULT_X = 8
MICROSTEPPING_DEFAULT_Y = 8
MICROSTEPPING_DEFAULT_Z = 8
MICROSTEPPING_DEFAULT_THETA = 8

SCAN_STABILIZATION_TIME_MS_X = 160
SCAN_STABILIZATION_TIME_MS_Y = 160
SCAN_STABILIZATION_TIME_MS_Z = 20

HOMING_ENABLED_X = True
HOMING_ENABLED_Y = True
HOMING_ENABLED_Z = False

SLEEP_TIME_S = 0.005

LED_MATRIX_R_FACTOR = 0
LED_MATRIX_G_FACTOR = 0
LED_MATRIX_B_FACTOR = 1

DEFAULT_SAVING_PATH = str(Path.home()) + "/Downloads"

class PLATE_READER:
    NUMBER_OF_ROWS = 8
    NUMBER_OF_COLUMNS = 12
    ROW_SPACING_MM = 9
    COLUMN_SPACING_MM = 9
    OFFSET_COLUMN_1_MM = 20
    OFFSET_ROW_A_MM = 20

DEFAULT_DISPLAY_CROP = 50 # value ranges from 1 to 100 - image display crop size 

CAMERA_PIXEL_SIZE_UM = {'IMX226':1.85,'IMX250':3.45,'IMX252':3.45,'PYTHON300':4.8}
OBJECTIVES = {'2x':{'magnification':2, 'NA':0.10, 'tube_lens_f_mm':180}, 
                '4x':{'magnification':4, 'NA':0.13, 'tube_lens_f_mm':180}, 
                '10x':{'magnification':10, 'NA':0.25, 'tube_lens_f_mm':180}, 
                '10x (Mitutoyo)':{'magnification':10, 'NA':0.25, 'tube_lens_f_mm':200},
                '20x (Boli)':{'magnification':20, 'NA':0.4, 'tube_lens_f_mm':180}, 
                '20x (Nikon)':{'magnification':20, 'NA':0.45, 'tube_lens_f_mm':200}, 
                '40x':{'magnification':40, 'NA':0.6, 'tube_lens_f_mm':180}}
TUBE_LENS_MM = 50
CAMERA_SENSOR = 'IMX226'
DEFAULT_OBJECTIVE = '10x (Mitutoyo)'
TRACKERS = ['csrt', 'kcf', 'mil', 'tld', 'medianflow','mosse','daSiamRPN']
DEFAULT_TRACKER = 'csrt'

ENABLE_TRACKING = False
TRACKING_SHOW_MICROSCOPE_CONFIGURATIONS = False # set to true when doing multimodal acquisition
if ENABLE_TRACKING:
    DEFAULT_DISPLAY_CROP = 100

class AF:
    STOP_THRESHOLD = 0.85
    CROP_WIDTH = 800
    CROP_HEIGHT = 800

class Tracking:
    SEARCH_AREA_RATIO = 10 #@@@ check
    CROPPED_IMG_RATIO = 10 #@@@ check
    BBOX_SCALE_FACTOR = 1.2
    DEFAULT_TRACKER = "csrt"
    INIT_METHODS = ["roi"]
    DEFAULT_INIT_METHOD = "roi"

##########################################################
#### start of loading machine specific configurations ####
##########################################################
config_files = glob.glob('.' + '/' + 'configuration*.txt')
if config_files:
    print('load machine-specific configuration')
    exec(open(config_files[0]).read())
##########################################################
##### end of loading machine specific configurations #####
##########################################################