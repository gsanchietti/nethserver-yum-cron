<?php

namespace NethServer\Module;

use Nethgui\System\PlatformInterface as Validate;

/**
 * @author Stephane de Labrusse <stephdl@de-labrusse.fr> 2017
 */
class YumCron extends \Nethgui\Controller\Collection\AbstractAction //implements \Nethgui\Component\DependencyConsumer
{


    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $attributes)
    {
        return \Nethgui\Module\SimpleModuleAttributesProvider::extendModuleAttributes($attributes, 'Administration', 16);
    }


    public function initialize()
    {
        parent::initialize();
     $validation = $this->createValidator()->memberOf('checkOnly','downloadOnly','installUpdate');
     $this->declareParameter('yumAction', $validation, array('configuration', 'yum-cron', 'yumAction'));
     $this->declareParameter('customMail', Validate::ANYTHING, array('configuration', 'yum-cron', 'customMail'));
     $this->declareParameter('status', Validate::SERVICESTATUS, array('configuration', 'yum-cron', 'status'));
     $this->declareParameter('customParam', Validate::ANYTHING, array('configuration', 'yum-cron', 'customParam'));


    }


    public function bind(\Nethgui\Controller\RequestInterface $request)
    {
        parent::bind($request);
        if($request->isMutation() && $request->hasParameter('customMail')) {
            $this->parameters['customMail'] = implode(",", self::splitLines($request->getParameter('customMail')));
        }
        if($request->isMutation() && $request->hasParameter('customParam')) {
            $this->parameters['customParam'] = implode(",", self::splitLines($request->getParameter('customParam')));
        }
    }


    public static function splitLines($text)
    {
        return array_filter(preg_split("/[,;\s]+/", $text));
    }


    public function validate(\Nethgui\Controller\ValidationReportInterface $report)
    {
        parent::validate($report);
            $forwards = $this->parameters['customMail'];
            if($forwards) {
                $emailValidator = $this->createValidator(Validate::EMAIL);
                foreach(explode(',', $forwards) as $email) {
                    if( !$emailValidator->evaluate($email)) {
                        $report->addValidationErrorMessage($this, 'customMail',
                            'valid_mailforward_address', array($email));
                    }
                }
            }

            $forwards = $this->parameters['customParam'];
            if($forwards) {
                $paramValidator = $this->createValidator()->regexp('/^[\?\*A-Za-z0-9][-\.\?\*\+\w]*$/');
                foreach(explode(',', $forwards) as $param) {
                    if( !$paramValidator->evaluate($param)) {
                        $report->addValidationErrorMessage($this, 'customParam',
                            'valid_Custom_Package_Exclusion', array($param));
                    }
                }
            }
    }

    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        parent::prepareView($view);

        if(isset($this->parameters['customMail'])) {
            $view['customMail'] = implode("\r\n", explode(',', $this->parameters['customMail']));
        }
        if(isset($this->parameters['customParam'])) {
            $view['customParam'] = implode("\r\n", explode(',', $this->parameters['customParam']));
        }
        $view['yumActionDatasource'] = \Nethgui\Renderer\AbstractRenderer::hashToDatasource(array(
                 'checkOnly' => $view->translate('Check_Only'),
                 'downloadOnly' => $view->translate('Download_Only'),
                 'installUpdate' => $view->translate('Automatic_Update'),
                 ));
    }

    public function onParametersSaved($changes)
    {
        $this->getPlatform()->signalEvent('nethserver-yum-cron-save@post-process');
    }
}

