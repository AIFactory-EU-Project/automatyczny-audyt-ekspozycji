<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Dto\ResponseDataDto;
use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\AbstractFOSRestController;

class AbstractDomainController extends AbstractFOSRestController
{
    protected function handleEventResponseData(ResponseDataDto $responseData)
    {
        $view = $this->view($responseData->getContent(), $responseData->getCode());

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
