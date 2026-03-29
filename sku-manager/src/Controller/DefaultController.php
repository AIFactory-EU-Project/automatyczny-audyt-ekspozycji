<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\Annotations as Rest;
use Symfony\Component\HttpFoundation\Response;

/**
 * Class DefaultController.
 */
class DefaultController extends AbstractDomainController
{
    /**
     * @Rest\Get("/")
     *
     * @return Response
     */
    public function index()
    {
        $view = $this->view(['system' => 'SKU Manager Service Api'], Response::HTTP_OK);

        $context = new Context();
        $context->setGroups(['list']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
