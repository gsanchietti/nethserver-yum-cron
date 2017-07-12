<?php
/* @var $view Nethgui\Renderer\Xhtml */
echo $view->header()->setAttribute('template', $T('YumCron_header'));

echo $view->panel()
->insert($view->fieldsetSwitch('status', 'enabled', $view::FIELDSETSWITCH_CHECKBOX | $view::FIELDSETSWITCH_EXPANDABLE)->setAttribute('uncheckedValue', 'disabled')
    ->insert($view->textArea('customParam', $view::LABEL_ABOVE)->setAttribute('dimensions', '5x30'))
//    ->insert($view->literal('<div class="labeled-control generated-url-title">'.$T('UseWildCard').'</div>'))
    ->insert($view->selector('yumAction', $view::SELECTOR_DROPDOWN))
    ->insert($view->textArea('customMail', $view::LABEL_ABOVE)->setAttribute('dimensions', '5x30'))
);

echo $view->buttonList($view::BUTTON_SUBMIT | $view::BUTTON_HELP);
