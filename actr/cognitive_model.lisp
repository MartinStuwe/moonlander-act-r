(clear-all)
(define-model compas-model

(chunk-type goal decision-state vision-state)
(chunk-type obstacle pos-x pos-y)
(chunk-type agent pos-x pos-y)

(add-dm
    (goal isa goal decision-state start vision-state idle)
)

(check-act-r-command "add-visicon-features")
(defun my-custom-press-key-monitor ()
  ;; Assume 'key' contains information about which key was pressed
  (model-output "Key has been pressed."))
(monitor-act-r-command "press-key" "(my-custom-press-key-monitor)")
(install-device '("motor" "keyboard"))

(goal-focus goal)

(p init-agent
    =goal>
        decision-state start
        vision-state idle
==>
    =goal>
        decision-state find-obstacles
        vision-state searching
)

(p find-obstacles
    =goal>
        decision-state find-obstacles
        vision-state searching
==>
    =goal>
        decision-state avoid-obstacles
)

(p move
    =goal>
        decision-state avoid-obstacles
==>
    +manual>
        cmd press-key
        key "z"
    ;!eval! (model-output "TEST")
    ;!eval! (my-custom-press-key-monitor)
    

    ;(evaluate-act-r-command "move-left")
    ;!eval! (model-output (format "~a" (local-or-remote-function-p t)))
    ;!eval! (model-output (local-or-remote-function-p t))
    !safe-eval! (model-output "Starting move-left command")
    !eval! (evaluate-act-r-command "moveleft")

)
)



