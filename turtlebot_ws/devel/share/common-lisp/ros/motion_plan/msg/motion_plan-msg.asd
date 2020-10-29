
(cl:in-package :asdf)

(defsystem "motion_plan-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "reference_point" :depends-on ("_package_reference_point"))
    (:file "_package_reference_point" :depends-on ("_package"))
  ))