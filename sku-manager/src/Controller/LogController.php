<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Entity\AppLog;
use App\Validation\ErrorCodes;
use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\Annotations as Rest;
use Nelmio\ApiDocBundle\Annotation\Model;
use Nelmio\ApiDocBundle\Annotation\Security;
use Swagger\Annotations as SWG;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Class LogController.
 */
class LogController extends AbstractDomainController
{
    /**
     * @Rest\Get("/log/")
     *
     * @SWG\Get(
     *     summary="Get application log",
     *     tags={"Log"},
     *     @SWG\Response(
     *          response=200,
     *          description="Log",
     *          @SWG\Schema(
     *              type="array",
     *              @Model(type=AppLog::class, groups={"list"})
     *          )
     *      ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=409, description="Conflict errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::CONFLICT_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     * )
     *
     * @SWG\Parameter(
     *     name="dateFrom",
     *     in="query",
     *     description="date in format: 2018-06-07T00:00",
     *     type="string"
     * )
     *
     * @SWG\Parameter(
     *     name="dateTo",
     *     in="query",
     *     description="date in format: 2018-06-07T00:00",
     *     type="string"
     * )
     *
     * @Security(name="Bearer")
     *
     * @param Request $request
     *
     * @return Response
     */
    public function list(Request $request)
    {
        $view = $this->view(['data']);

        $context = new Context();
        $context->setGroups(['list']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
