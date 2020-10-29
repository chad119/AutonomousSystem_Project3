; Auto-generated. Do not edit!


(cl:in-package motion_plan-msg)


;//! \htmlinclude reference_point.msg.html

(cl:defclass <reference_point> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0)
   (theta
    :reader theta
    :initarg :theta
    :type cl:float
    :initform 0.0)
   (mode
    :reader mode
    :initarg :mode
    :type cl:fixnum
    :initform 0))
)

(cl:defclass reference_point (<reference_point>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <reference_point>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'reference_point)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_plan-msg:<reference_point> is deprecated: use motion_plan-msg:reference_point instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <reference_point>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_plan-msg:x-val is deprecated.  Use motion_plan-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <reference_point>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_plan-msg:y-val is deprecated.  Use motion_plan-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'theta-val :lambda-list '(m))
(cl:defmethod theta-val ((m <reference_point>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_plan-msg:theta-val is deprecated.  Use motion_plan-msg:theta instead.")
  (theta m))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <reference_point>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_plan-msg:mode-val is deprecated.  Use motion_plan-msg:mode instead.")
  (mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <reference_point>) ostream)
  "Serializes a message object of type '<reference_point>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'theta))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let* ((signed (cl:slot-value msg 'mode)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <reference_point>) istream)
  "Deserializes a message object of type '<reference_point>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'theta) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mode) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<reference_point>)))
  "Returns string type for a message object of type '<reference_point>"
  "motion_plan/reference_point")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'reference_point)))
  "Returns string type for a message object of type 'reference_point"
  "motion_plan/reference_point")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<reference_point>)))
  "Returns md5sum for a message object of type '<reference_point>"
  "25fe4ce9c6c513804d777b4bfd749dc0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'reference_point)))
  "Returns md5sum for a message object of type 'reference_point"
  "25fe4ce9c6c513804d777b4bfd749dc0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<reference_point>)))
  "Returns full string definition for message of type '<reference_point>"
  (cl:format cl:nil "float32 x~%float32 y~%float32 theta~%int16 mode~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'reference_point)))
  "Returns full string definition for message of type 'reference_point"
  (cl:format cl:nil "float32 x~%float32 y~%float32 theta~%int16 mode~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <reference_point>))
  (cl:+ 0
     4
     4
     4
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <reference_point>))
  "Converts a ROS message object to a list"
  (cl:list 'reference_point
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':theta (theta msg))
    (cl:cons ':mode (mode msg))
))
