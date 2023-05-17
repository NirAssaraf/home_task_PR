import cv2 

class ComputerVisionTasks:

    def rotate_image(self,image):
        # Perform image rotation (90 degrees clockwise) using cv2
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return rotated_image


    def dilate_image(self,image):
        # Perform dilation (5x5) using cv2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated_image = cv2.dilate(image, kernel)
        return dilated_image


    def erode_image(self,image):
        # Perform erosion (5x5) using cv2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        eroded_image = cv2.erode(image, kernel)
        return eroded_image


    def perform_canny_edge_detection(self,image):
        # Perform Canny edge detection using cv2
        edges = cv2.Canny(image, 100, 200)
        return edges


    def resize_image(self,image):
        # Perform resizing (downsample by 4 - INTER_CUBIC) using cv2
        resized_image = cv2.resize(image, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
        return resized_image