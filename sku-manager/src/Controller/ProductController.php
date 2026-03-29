<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Entity\Product;
use App\Entity\User;
use App\Event\ProductManagement\AddProductEvent;
use App\Event\ProductManagement\AddProductValidEvent;
use App\Event\ProductManagement\DeleteProductEvent;
use App\Event\ProductManagement\DeleteProductValidEvent;
use App\Event\ProductManagement\UpdateProductEvent;
use App\Event\ProductManagement\UpdateProductValidEvent;
use App\Form\ProductType;
use App\Service\ProductManager;
use App\Validation\ErrorCodes;
use Exception;
use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\Annotations as Rest;
use Nelmio\ApiDocBundle\Annotation\Model;
use Nelmio\ApiDocBundle\Annotation\Security;
use Swagger\Annotations as SWG;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

/**
 * Class ProductController.
 *
 * @method User getUser()
 */
class ProductController extends AbstractDomainController
{
    /**
     * @Rest\Get("/product/")
     *
     * @SWG\Get(
     *     summary="List products",
     *     tags={"Product"},
     *     @SWG\Response(
     *          response=200,
     *          description="Products",
     *          @SWG\Schema(
     *              type="array",
     *              @Model(type=Product::class, groups={"list"})
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
     * @return Response
     */
    public function list(ProductManager $productManager): Response
    {
        $view = $this->view($productManager->getProducts($this->getUser()->getSystem()));
        $context = new Context();
        $context->setGroups(['list']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Post("/product/")
     *
     * @SWG\Post(
     *     summary="Create product",
     *     tags={"Product"},
     *     @SWG\Response(
     *          response=201,
     *          description="Created product details",
     *          @Model(type=Product::class)
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
     *     description="Product creation parameters",
     *     @Model(type=ProductType::class)
     * )
     *
     * @param Request $request
     *
     * @Security(name="Bearer")
     *
     * @return Response
     *
     * @throws Exception
     */
    public function create(Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $addEvent = new AddProductEvent($request, $this->getUser()->getSystem());
        $eventDispatcher->dispatch($addEvent);
        if ($addEvent->getResponseData()) {
            return $this->handleEventResponseData($addEvent->getResponseData());
        }

        $addValidEvent = new AddProductValidEvent($request, $this->getUser()->getSystem());
        $addValidEvent->setProduct($addEvent->getProduct());

        $eventDispatcher->dispatch($addValidEvent);
        if ($addValidEvent->getResponseData()) {
            $this->handleEventResponseData($addValidEvent->getResponseData());
        }

        $view = $this->view($addValidEvent->getProduct(), Response::HTTP_CREATED);
        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Get("/product/{id}")
     *
     * @SWG\Get(
     *     summary="Get product details",
     *     tags={"Product"},
     *     @SWG\Response(
     *          response=200,
     *          description="Product details",
     *          @SWG\Items(@Model(type=Product::class))
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
     * @param int            $id
     * @param ProductManager $productManager
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function show(int $id, ProductManager $productManager): Response
    {
        $product = $productManager->getProduct($id, $this->getUser()->getSystem());
        if (!$product) {
            return $this->handleView(
                $this->view(
                    ['message' => 'Product not found'],
                    Response::HTTP_NOT_FOUND
                )
            );
        }

        $view = $this->view($product);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Patch("/product/{id}")
     *
     * @SWG\Patch(
     *     summary="Update product",
     *     tags={"Product"},
     *     @SWG\Response(
     *          response=200,
     *          description="Updated product details",
     *          @Model(type=Product::class)
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
     *     description="Product creation parameters",
     *     @Model(type=ProductType::class)
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
        $updateEvent = new UpdateProductEvent($request, $this->getUser()->getSystem());
        $updateEvent->setId($id);
        $eventDispatcher->dispatch($updateEvent);
        if ($updateEvent->getResponseData()) {
            return $this->handleEventResponseData($updateEvent->getResponseData());
        }

        $updateValidEvent = new UpdateProductValidEvent($request, $this->getUser()->getSystem());
        $updateValidEvent->setProduct($updateEvent->getProduct());

        $eventDispatcher->dispatch($updateValidEvent);
        if ($updateValidEvent->getResponseData()) {
            $this->handleEventResponseData($updateValidEvent->getResponseData());
        }

        $view = $this->view($updateValidEvent->getProduct(), Response::HTTP_OK);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Delete("/product/{id}")
     *
     * @SWG\Delete(
     *     summary="Delete product",
     *     tags={"Product"},
     *     @SWG\Response(
     *          response=200,
     *          description="Product deleted",
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
     * @param int $id
     *
     * @Security(name="Bearer")
     *
     * @return Response
     */
    public function delete(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $deleteEvent = new DeleteProductEvent($request, $this->getUser()->getSystem());
        $deleteEvent->setId($id);
        $eventDispatcher->dispatch($deleteEvent);
        if ($deleteEvent->getResponseData()) {
            return $this->handleEventResponseData($deleteEvent->getResponseData());
        }

        $deleteValidEvent = new DeleteProductValidEvent($request, $this->getUser()->getSystem());
        $deleteValidEvent->setProduct($deleteEvent->getProduct());

        $eventDispatcher->dispatch($deleteValidEvent);
        if ($deleteValidEvent->getResponseData()) {
            return $this->handleEventResponseData($deleteValidEvent->getResponseData());
        }

        $view = $this->view(['message' => 'User deleted', Response::HTTP_OK]);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
