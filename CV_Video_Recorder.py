import cv2 as cv
import numpy as np

# 카메라 영상 받아오기
video = cv.VideoCapture(0)

# 녹화 상태 초기 설정
record = False

if video.isOpened():
    # 영상 저장 경로 설정
    path_m = 'C:\\Users\\isw33\\camera.avi' # 카메라 영상
    path_r = 'C:\\Users\\isw33\\record.avi' # 녹화 영상
    
    # 카메라 화면 가로, 세로 길이 받아오기
    w = video.get(cv.CAP_PROP_FRAME_WIDTH)
    h = video.get(cv.CAP_PROP_FRAME_HEIGHT)
    size = (int(w), int(h))

    # 영상 저장을 위한 코덱 설정
    fourcc = cv.VideoWriter_fourcc(*'XVID')

    # fps 값, 밀리초 단위의 대기 시간값 계산
    fps = video.get(cv.CAP_PROP_FPS)
    wait_msec = int(1 / fps * 1000)

    # 저장 기능 추가를 위한 VideoWriter 선언
    out_m = cv.VideoWriter(path_m, fourcc, fps, size) # 카메라 영상
    out_r = cv.VideoWriter(path_r, fourcc, fps, size) # 녹화 영상

    # 대비, 밝기와 증가, 감소값 기본 설정
    contrast = 1
    contrast_step = 0.1
    brightness = 0
    brightness_step = 1

    while True:
        # 영상으로부터 이미지 읽기
        valid, img = video.read()
        if not valid:
            break
        
        # 받아온 이미지에 밝기, 대비 기능 추가
        img_tran = contrast * img + brightness
        img_tran[img_tran < 0] = 0
        img_tran[img_tran > 255] = 0
        img_tran = img_tran.astype(np.uint8)

        # 화면에 밝기, 대비 수치 표시
        info = f'Contrast: {contrast:.1f}, Brightness: {brightness:.0f}'
        cv.putText(img_tran, info, (335, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))

        if record == True: # 녹화 중일 때
            # [필수 기능 3-1] Record 모드 시 화면에 표시 -> 화면 좌상단에 'Recording...' 텍스트 표시
            cv.putText(img_tran, 'Recording...', (10, 25), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

            # 녹화 시작
            out_r.write(img_tran)

        # [필수 기능 1] 화면에 현재 카메라 영상 표시
        cv.imshow('Video Recorder', img_tran)

        # [필수 기능 2] 카메라 영상을 동영상 파일로 저장
        out_m.write(img_tran)

        # 키 설정
        key = cv.waitKey(wait_msec)
        if key == 27: # [필수 기능 3-3] ESC 키에 프로그램 종료
            break
        elif key == ord(' '): # [필수 기능 3-2] Space 키에 모드 변환
            if record == False:
                record = True
            else:
                record = False
        
        # 대비 조절
        elif key == ord('+') or key == ord('='):
            contrast += contrast_step
        elif key == ord('-') or key == ord('_'):
            contrast -= contrast_step
        
        # 밝기 조절
        elif key == ord(']') or key == ord('}'):
            brightness += brightness_step
        elif key == ord('[') or key == ord('{'):
            brightness -= brightness_step

    cv.destroyAllWindows()
