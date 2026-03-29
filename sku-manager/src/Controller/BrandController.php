<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Entity\Brand;
use App\Entity\User;
use App\Event\BrandManagement\AddBrandEvent;
use App\Event\BrandManagement\AddBrandValidEvent;
use App\Event\BrandManagement\DeleteBrandEvent;
use App\Event\BrandManagement\DeleteBrandValidEvent;
use App\Event\BrandManagement\UpdateBrandEvent;
use App\Event\BrandManagement\UpdateBrandValidEvent;
use App\Form\BrandType;
use App\Service\BrandManager;
use App\Validation\ErrorCodes;
use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\Annotations as Rest;
use Nelmio\ApiDocBundle\Annotation\Model;
use Nelmio\ApiDocBundle\Annotation\Security;
use Swagger\Annotations as SWG;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

/**
 * Class BrandController.
 *
 * @method User getUser()
 */
class BrandController extends AbstractDomainController
{
    /**
     * @Rest\Get("/brand/")
     *
     * @SWG\Get(
     *     summary="List product brands",
     *     tags={"Brand"},
     *     @SWG\Response(
     *          response=200,
     *          description="Product brand",
     *          @SWG\Schema(
     *              type="array",
     *              @Model(type=Brand::class, groups={"list"})
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
     * @Security(name="Bearer")
     *
     * @param BrandManager $brandManager
     *
     * @return Response
     */
    public function list(BrandManager $brandManager): Response
    {
        $view = $this->view($brandManager->getBrands($this->getUser()->getSystem()));

        $context = new Context();
        $context->setGroups(['list']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Post("/brand/")
     *
     * @SWG\Post(
     *     summary="Create brand",
     *     tags={"Brand"},
     *     @SWG\Response(
     *          response=201,
     *          description="Created product brand details",
     *          @Model(type=Brand::class)
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *              @SWG\Property(property="form", type="object")
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
     *     name="data",
     *     in="body",
     *     description="Product brand creation parameters",
     *     @Model(type=BrandType::class)
     * )
     *
     * @param Request                  $request
     * @param EventDispatcherInterface $eventDispatcher
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function create(Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $addEvent = new AddBrandEvent($request, $this->getUser()->getSystem());
        $eventDispatcher->dispatch($addEvent);
        if ($addEvent->getResponseData()) {
            return $this->handleEventResponseData($addEvent->getResponseData());
        }

        $addValidEvent = new AddBrandValidEvent($request, $this->getUser()->getSystem());
        $addValidEvent->setBrand($addEvent->getBrand());

        $eventDispatcher->dispatch($addValidEvent);
        if ($addValidEvent->getResponseData()) {
            return $this->handleEventResponseData($addValidEvent->getResponseData());
        }

        $view = $this->view($addValidEvent->getBrand(), Response::HTTP_CREATED);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Get("/brand/{id}")
     *
     * @SWG\Get(
     *     summary="Get brand details",
     *     tags={"Brand"},
     *     @SWG\Response(
     *          response=200,
     *          description="Brand details",
     *          @Model(type=Brand::class)
     *     ),
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
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @param int          $id
     * @param BrandManager $brandManager
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function show(int $id, BrandManager $brandManager): Response
    {
        $brand = $brandManager->getBrand($id, $this->getUser()->getSystem());
        if (!$brand) {
            return $this->handleView(
                $this->view(
                    ['message' => 'Brand not found'],
                    Response::HTTP_NOT_FOUND
                )
            );
        }

        $view = $this->view($brand);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Patch("/brand/{id}")
     *
     * @SWG\Patch(
     *     summary="Update brand",
     *     tags={"Brand"},
     *     @SWG\Response(
     *          response=200,
     *          description="Updated brand details",
     *          @Model(type=Brand::class)
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *              @SWG\Property(property="form", type="object")
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     description="Product brand creation parameters",
     *     @Model(type=BrandType::class)
     * )
     *
     * @param int     $id
     * @param Request $request
     *
     * @Security(name="Bearer")
     *
     * @return Response
     */
    public function update(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $updateEvent = new UpdateBrandEvent($request, $this->getUser()->getSystem());
        $updateEvent->setId($id);
        $eventDispatcher->dispatch($updateEvent);
        if ($updateEvent->getResponseData()) {
            return $this->handleEventResponseData($updateEvent->getResponseData());
        }

        $updateValidEvent = new UpdateBrandValidEvent($request, $this->getUser()->getSystem());
        $updateValidEvent->setBrand($updateEvent->getBrand());

        $eventDispatcher->dispatch($updateValidEvent);
        if ($updateValidEvent->getResponseData()) {
            return $this->handleEventResponseData($updateValidEvent->getResponseData());
        }

        $view = $this->view($updateValidEvent->getBrand(), Response::HTTP_OK);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Delete("/brand/{id}")
     *
     * @SWG\Delete(
     *     summary="Delete brand",
     *     tags={"Brand"},
     *     @SWG\Response(
     *          response=200,
     *          description="Brand deleted",
     *     ),
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
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @param int                      $id
     * @param Request                  $request
     * @param EventDispatcherInterface $eventDispatcher
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function delete(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $deleteEvent = new DeleteBrandEvent($request, $this->getUser()->getSystem());
        $deleteEvent->setId($id);
        $eventDispatcher->dispatch($deleteEvent);
        if ($deleteEvent->getResponseData()) {
            return $this->handleEventResponseData($deleteEvent->getResponseData());
        }

        $deleteValidEvent = new DeleteBrandValidEvent($request, $this->getUser()->getSystem());
        $deleteValidEvent->setBrand($deleteEvent->getBrand());

        $eventDispatcher->dispatch($deleteValidEvent);
        if ($deleteValidEvent->getResponseData()) {
            $this->handleEventResponseData($deleteValidEvent->getResponseData());
        }

        $view = $this->view(['message' => 'Brand deleted', Response::HTTP_OK]);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
