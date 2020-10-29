;; Auto-generated. Do not edit!


(when (boundp 'motion_plan::reference_point)
  (if (not (find-package "MOTION_PLAN"))
    (make-package "MOTION_PLAN"))
  (shadow 'reference_point (find-package "MOTION_PLAN")))
(unless (find-package "MOTION_PLAN::REFERENCE_POINT")
  (make-package "MOTION_PLAN::REFERENCE_POINT"))

(in-package "ROS")
;;//! \htmlinclude reference_point.msg.html


(defclass motion_plan::reference_point
  :super ros::object
  :slots (_x _y _theta _mode ))

(defmethod motion_plan::reference_point
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:theta __theta) 0.0)
    ((:mode __mode) 0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _theta (float __theta))
   (setq _mode (round __mode))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:theta
   (&optional __theta)
   (if __theta (setq _theta __theta)) _theta)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
  (:serialization-length
   ()
   (+
    ;; float32 _x
    4
    ;; float32 _y
    4
    ;; float32 _theta
    4
    ;; int16 _mode
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _x
       (sys::poke _x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y
       (sys::poke _y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _theta
       (sys::poke _theta (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; int16 _mode
       (write-word _mode s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _x
     (setq _x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y
     (setq _y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _theta
     (setq _theta (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; int16 _mode
     (setq _mode (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get motion_plan::reference_point :md5sum-) "25fe4ce9c6c513804d777b4bfd749dc0")
(setf (get motion_plan::reference_point :datatype-) "motion_plan/reference_point")
(setf (get motion_plan::reference_point :definition-)
      "float32 x
float32 y
float32 theta
int16 mode

")



(provide :motion_plan/reference_point "25fe4ce9c6c513804d777b4bfd749dc0")


