sudo mount /kolos

xhost +local: # (optional) for displaying images with cv.imshow()

args=(
    --name=ocr                          # Unique container name
    --device=/dev/video0                # Forward camera stream
    --gpus=all                          # Enable cuda
    --env QT_X11_NO_MITSHM=1            # Required for X forwarding
    -v /tmp/.X11-unix:/tmp/.X11-unix    # Required for X frowarding
    -e DISPLAY=$DISPLAY                 # Required for X forwarding
    -v /kolos:/kolos                    # Mount /kolos
    -w /root                            # Initial directory
    ocr/dev-1.4 bash                    # Image name and command to run
)

sudo docker run -it "${args[@]}"
